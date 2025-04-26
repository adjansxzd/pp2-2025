import psycopg2
from psycopg2 import Error
import csv

def create_connection():
    return psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='BBJN1227',
        host='localhost',
        port='5432'
    )

def create_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Phonebooklab (
                id SERIAL PRIMARY KEY,
                fname TEXT NOT NULL,
                phone TEXT NOT NULL UNIQUE
            );
        """)
        conn.commit()

def import_from_csv(conn, filename):
    with conn.cursor() as cursor, open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cursor.execute(
                "INSERT INTO Phonebooklab (fname, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                row
            )
        conn.commit()

def manual_input(conn):
    num = int(input("How many contacts to add: "))
    with conn.cursor() as cursor:
        for _ in range(num):
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            cursor.execute(
                "INSERT INTO Phonebooklab (fname, phone) VALUES (%s, %s) ON CONFLICT (phone) DO UPDATE SET fname = EXCLUDED.fname",
                (name, phone)
            )
        conn.commit()

def update_record(conn):
    option = input("Update (1-name, 2-phone): ")
    with conn.cursor() as cursor:
        if option == '1':
            phone = input("Enter phone: ")
            new_name = input("Enter new name: ")
            cursor.execute("UPDATE Phonebooklab SET fname = %s WHERE phone = %s", (new_name, phone))
        else:
            name = input("Enter name: ")
            new_phone = input("Enter new phone: ")
            cursor.execute("UPDATE Phonebooklab SET phone = %s WHERE fname = %s", (new_phone, name))
        conn.commit()

def query_records(conn):
    option = input("Filter by (1-name, 2-phone, 3-all): ")
    with conn.cursor() as cursor:
        if option == '1':
            name = input("Enter name: ")
            cursor.execute("SELECT * FROM Phonebooklab WHERE fname = %s", (name,))
        elif option == '2':
            phone = input("Enter phone: ")
            cursor.execute("SELECT * FROM Phonebooklab WHERE phone = %s", (phone,))
        else:
            cursor.execute("SELECT * FROM Phonebooklab")
        for row in cursor.fetchall():
            print(row)

def delete_record(conn):
    option = input("Delete by (1-name, 2-phone): ")
    with conn.cursor() as cursor:
        if option == '1':
            name = input("Enter name: ")
            cursor.execute("DELETE FROM Phonebooklab WHERE fname = %s", (name,))
        else:
            phone = input("Enter phone: ")
            cursor.execute("DELETE FROM Phonebooklab WHERE phone = %s", (phone,))
        conn.commit()

def paginated_query(conn):
    limit = int(input("Enter LIMIT: "))
    offset = int(input("Enter OFFSET: "))
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Phonebooklab ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
        for row in cursor.fetchall():
            print(row)

def main():
    conn = create_connection()
    create_table(conn)

    while True:
        print("""
        1 - Import from CSV
        2 - Manual input
        3 - Update record
        4 - Query records
        5 - Delete record
        6 - Paginated query
        0 - Exit
        """)
        
        choice = input("Select option: ")
        
        try:
            if choice == '1':
                filename = input("Enter CSV filename: ")
                import_from_csv(conn, filename)
            elif choice == '2':
                manual_input(conn)
            elif choice == '3':
                update_record(conn)
            elif choice == '4':
                query_records(conn)
            elif choice == '5':
                delete_record(conn)
            elif choice == '6':
                paginated_query(conn)
            elif choice == '0':
                break
        except Error as e:
            print(f"Error: {e}")
            conn.rollback()

    conn.close()

if __name__ == "__main__":
    main()