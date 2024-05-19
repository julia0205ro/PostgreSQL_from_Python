import psycopg2
from config import password

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phone_numbers;
        DROP TABLE client_info;
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client_info(
            id SERIAL PRIMARY KEY,
            name VARCHAR(30) NOT NULL,
            surname VARCHAR(60) NOT NULL,
            email VARCHAR(80) NOT NULL
        );
        """)
        cur.execute("""
                CREATE TABLE IF NOT EXISTS phone_numbers(
                    phone_number VARCHAR(11) PRIMARY KEY,
                    client_id INT NOT NULL REFERENCES client_info(id) ON DELETE CASCADE
                );
                """)
        conn.commit()

def add_client(conn, id, name, surname, email):
    with conn.cursor() as cur:
        insert_with_param = """
        INSERT INTO client_info(id, name, surname, email) 
        VALUES(%s, %s, %s, %s)
        RETURNING id, name, surname, email; 
        """
        data_tuple = (id, name, surname, email)
        cur.execute(insert_with_param, data_tuple)
        print(cur.fetchone())

def add_client_phone(conn, phone_number_value, client_id_value):
    with conn.cursor() as cur:
        cur.execute("""SELECT id FROM client_info;""")
        id_list = cur.fetchall()
        for id in id_list:
            if client_id_value == id[0]:
                cur.execute("""
                INSERT INTO phone_numbers(phone_number, client_id)
                VALUES(%s, %s)
                RETURNING phone_number, client_id;
                """, (phone_number_value, client_id_value))
                print(cur.fetchone())

def update_data(conn, id, name=None, surname=None, email=None):
    with conn.cursor() as cur:
        if name is not None:
            cur.execute("""
            UPDATE client_info SET name=%s WHERE id=%s
            RETURNING id, name, surname, email;
            """, (name, id))
        else:
            pass
        if surname is not None:
            cur.execute("""
            UPDATE client_info SET surname=%s WHERE id=%s
            RETURNING id, name, surname, email;
            """, (surname, id))
        else:
            pass
        if email is not None:
            cur.execute("""
                UPDATE client_info SET email=%s WHERE id=%s
                RETURNING id, name, surname, email;
                """, (email, id))
        else:
            pass
        print(cur.fetchall())

def update_phone_number(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
        ALTER TABLE phone_numbers DROP CONSTRAINT phone_numbers_pkey;
        """)
        cur.execute("""
                UPDATE phone_numbers SET phone_number=%s WHERE client_id=%s;
                """, (phone_number, client_id))
        cur.execute("""
        ALTER TABLE phone_numbers ADD PRIMARY KEY (phone_number);
        """)
        cur.execute("""
                   SELECT * FROM phone_numbers
                   WHERE phone_number=%s;
                   """, (phone_number,))
        print(cur.fetchall())

def delete_phone_number(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_numbers WHERE client_id=%s;
        """, (client_id,))
        cur.execute("""
        SELECT * FROM phone_numbers;
        """)
        print(cur.fetchall())

def delete_client(conn, id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client_info WHERE id=%s;
        """, (id,))
        cur.execute("""
        SELECT * FROM client_info;
        """)
        print(cur.fetchall())

def find_clients_info(conn, *argv):
    with conn.cursor() as cur:
        for arg in argv:
            cur.execute("""
                    SELECT * FROM client_info WHERE name=%s OR
                    surname=%s OR
                    email=%s;
                    """, (arg, arg, arg))
        print(cur.fetchall())

def find_clients_phone_number(conn, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM phone_numbers WHERE phone_number=%s;
        """, (phone_number,))
        print(cur.fetchone())