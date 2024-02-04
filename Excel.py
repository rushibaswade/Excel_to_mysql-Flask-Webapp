from flask import Flask, render_template, request, jsonify
import pandas as pd
import mysql.connector
import logging

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Rushikesh@123',
}

logging.basicConfig(level=logging.DEBUG)

def create_mysql_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"USE {db_name}")

def create_mysql_table(cursor, df, table_name):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY unique,
        {', '.join([f'{col} VARCHAR(255)' for col in df.columns])}
    )
    """
    cursor.execute(create_table_query)

# def create_mysql_database(cursor, db_name):
#     cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
#     cursor.execute(f"USE {db_name}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        db_name = request.form['dbname']
        table_name = request.form['tablename']
        uploaded_file = request.files['file']

        if not uploaded_file.filename.endswith(('.xls', '.xlsx')):
            return jsonify({'status': 'error', 'message': 'Invalid file format. Please upload an Excel file.'}), 400

        df = pd.read_excel(uploaded_file)

        # Update database configuration with user-provided database name
        db_config['database'] = None  # No initial database specified

        # Connect to the MySQL server without specifying the database
        with mysql.connector.connect(pool_name="excel_pool", pool_size=5, **db_config) as conn:
            with conn.cursor() as cursor:
                try:
                    # Check if the database exists, and if not, create it
                    create_mysql_database(cursor, db_name)
                    print(f"Database '{db_name}' created or already exists.")

                    # Create MySQL table with user-provided table name
                    create_mysql_table(cursor, df, table_name)
                    print(f"Table '{table_name}' created or already exists.")

                    for index, row in df.iterrows():
                        insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s']*len(df.columns))})"
                        cursor.execute(insert_query, tuple(row))

                    conn.commit()
                    return jsonify({'status': 'success', 'message': 'Data has been updated successfully'})

                except mysql.connector.Error as err:
                    print(f"MySQL Error: {err}")
                    return jsonify({'status': 'error', 'message': f"MySQL Error: {err}"}), 500

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': f"Error: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
