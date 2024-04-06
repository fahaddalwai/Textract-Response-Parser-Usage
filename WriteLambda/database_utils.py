import pymysql

def insert_data_table(conn, row_data):
    try:
        table_name = 'YOUR TABLE'  # Replace with your actual table name
        column_names = ['ALL', 'YOUR', 'COLUMNS']


        with conn.cursor() as cur:
            # Check if the table exists; if not, create it
            cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, {', '.join([f'{col} VARCHAR(255)' for col in column_names])})")

            # Create the INSERT INTO SQL statement
            insert_row_sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(['%s']*len(column_names))})"
            
            # Insert the row into the table
            cur.execute(insert_row_sql, tuple(row_data))
            
            # Commit the changes
            conn.commit()
            print()
    except pymysql.MySQLError as e:
        # Handle exceptions, log errors, or raise as needed
        print(f"Error: {e}")
        
def select_all_from_table(conn, table_name):
    try:
        with conn.cursor() as cur:
            # Fetch and print all rows from the specified table
            cur.execute(f"SELECT * FROM {table_name}")
            rows = cur.fetchall()

            print(f"Table: {table_name}")
            for row in rows:
                print(row)

    except pymysql.MySQLError as e:
        # Handle exceptions, log errors, or raise as needed
        print(f"Error: {e}")
