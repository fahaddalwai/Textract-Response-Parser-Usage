import pymysql

def insert_data_table2(conn, row_data):
    try:
        table_name = 'table2'  # Replace with your actual table name
        column_names = ['Words_Practiced1', 'MT1', 'DT1', 'RR1', 'REV1', 'Words_Practiced2', 'MT2', 'DT2', 'RR2', 'REV2', 'Distractors']


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
        
def insert_data_prompts(conn, row_data):
    try:
        table_name = 'prompts'  # Replace with your actual table name
        column_names = ['Trial', 'column_one ', 'column_two ', 'column_three', 'column_four', 'column_five', 'column_six', 'column_seven', 'column_eight', 'column_nine', 'column_ten']


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

def insert_data_table1(conn, row_data):
    try:
        table_name = 'table1'  # Replace with your actual table name
        column_names = ['Prompt_code_short1', 'Prompt_code_long1', 'Prompt_code_short2', 'Prompt_code_long2', 'Trial_type_short', 'Trial_type_long']


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
        

def insert_data_vocab_based_lesson(conn, row_data):
    try:
        table_name = 'vocab_based_lesson'  # Replace with your actual table name
        column_names = ["DATE", "LESSONS_TITLE", "LESSON_NUMBER", "STUDENTS_NAME"]


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