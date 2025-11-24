"""
Execute SQL Queries Script
Runs all queries from queries.sql and displays results
"""

import sqlite3
import sys

def execute_queries(db_path='integration_database.db', queries_file='queries.sql'):
    """Execute SQL queries from file and display results"""
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Enable column names in results
        cursor.row_factory = sqlite3.Row
        
        # Read queries file
        with open(queries_file, 'r', encoding='utf-8') as f:
            queries = f.read()
        
        print("=" * 80)
        print("Executing SQL Queries from queries.sql")
        print("=" * 80)
        
        # Parse queries - split by semicolon but handle comments
        query_blocks = []
        current_block = []
        in_comment = False
        
        for line in queries.split('\n'):
            stripped = line.strip()
            
            # Handle block comments
            if '/*' in stripped:
                in_comment = True
            if '*/' in stripped:
                in_comment = False
                continue
            if in_comment:
                continue
            
            # Skip single-line comments
            if stripped.startswith('--'):
                # If it's a section header (contains ===), print it
                if '=' in stripped and len(stripped) > 10:
                    if current_block:
                        query_blocks.append('\n'.join(current_block))
                        current_block = []
                    query_blocks.append(('HEADER', stripped))
                continue
            
            # Add non-empty lines to current block
            if stripped:
                current_block.append(line)
            elif current_block:
                # Empty line - end of query block
                query_blocks.append('\n'.join(current_block))
                current_block = []
        
        # Add last block if exists
        if current_block:
            query_blocks.append('\n'.join(current_block))
        
        # Execute queries
        query_num = 0
        for block in query_blocks:
            if isinstance(block, tuple) and block[0] == 'HEADER':
                print(f"\n{block[1]}")
                print("=" * 80)
                continue
            
            query_text = block.strip()
            if not query_text or not query_text.rstrip(';'):
                continue
            
            query_num += 1
            
            try:
                # Execute query
                cursor.execute(query_text)
                
                # Fetch results
                results = cursor.fetchall()
                
                if results:
                    # Get column names
                    columns = [description[0] for description in cursor.description]
                    
                    # Print header
                    print(f"\n[Query Result {query_num}]")
                    print("-" * 80)
                    
                    # Determine column width based on content
                    col_widths = []
                    for col in columns:
                        max_len = len(col)
                        for row in results[:10]:  # Sample first 10 rows
                            val_len = len(str(row[col]))
                            if val_len > max_len:
                                max_len = val_len
                        col_widths.append(min(max_len + 2, 25))  # Cap at 25
                    
                    # Print column headers
                    header_parts = []
                    for i, col in enumerate(columns[:8]):  # Limit to 8 columns
                        header_parts.append(f"{col:<{col_widths[i]}}")
                    print(" | ".join(header_parts))
                    print("-" * 80)
                    
                    # Print rows (limit to 15 for readability)
                    for row in results[:15]:
                        row_parts = []
                        for i, col in enumerate(columns[:8]):
                            val = str(row[col])
                            if len(val) > col_widths[i] - 2:
                                val = val[:col_widths[i] - 5] + "..."
                            row_parts.append(f"{val:<{col_widths[i]}}")
                        print(" | ".join(row_parts))
                    
                    if len(results) > 15:
                        print(f"... ({len(results) - 15} more rows)")
                    
                    print(f"Total rows returned: {len(results)}")
                else:
                    print(f"\n[Query {query_num}] - No results returned")
                    
            except sqlite3.Error as e:
                print(f"\n[Query {query_num}] Error: {e}")
                # Print first line of query for context
                first_line = query_text.split('\n')[0].strip()[:80]
                print(f"Query: {first_line}...")
        
        conn.close()
        print("\n" + "=" * 80)
        print("All queries executed successfully!")
        print("=" * 80)
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        print("\nMake sure you have:")
        print("1. Run 'python data_integration.py' first to create the database")
        print("2. The queries.sql file exists in the current directory")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    execute_queries()

