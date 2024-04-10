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
                    client_id INT NOT NULL REFERENCES client_info(id)
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

def update_name(conn, id, name):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE client_info SET name=%s WHERE id=%s
        RETURNING id, name, surname, email;
        """, (name, id))
        print(cur.fetchone())

def update_surname(conn, id, surname):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE client_info SET surname=%s WHERE id=%s
        RETURNING id, name, surname, email;
        """, (surname, id))
        print(cur.fetchone())

def update_email(conn, id, email):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE client_info SET email=%s WHERE id=%s
        RETURNING id, name, surname, email;
        """, (email, id))
        print(cur.fetchone())

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
                   SELECT * FROM phone_numbers;
                   """)
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

def find_clients_name(conn, name):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM client_info WHERE name=%s;
        """, (name,))
        print(cur.fetchall())

def find_clients_surname(conn, surname):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM client_info WHERE surname=%s;
        """, (surname,))
        print(cur.fetchall())

def find_clients_email(conn, email):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM client_info WHERE email=%s;
        """, (email,))
        print(cur.fetchall())

def find_clients_phone_number(conn, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM phone_numbers WHERE phone_number=%s;
        """, (phone_number,))
        print(cur.fetchone())

with psycopg2.connect(database='client_db', user='postgres',
                      password=password) as conn:
    create_db(conn)
    add_client(conn, 1, 'Kimura',
               'Tatsunari', 'kimuratatsunari@gmail.com')
    add_client(conn, 3, 'Naruto',
               'Uzumaki', 'narutouzumaki@gmail.com')
    add_client_phone(conn,'99999999999', 1)
    add_client_phone(conn,'99999999998', 2)
    add_client_phone(conn, '99999999990', 3)
    update_name(conn, 1, 'Togawa')
    update_surname(conn, 1, 'Unknown')
    update_email(conn, 1, 'togawaunkown@gmail.com')
    update_phone_number(conn, 1,'99999999997')
    delete_phone_number(conn, 3)
    delete_client(conn, 3)
    find_clients_surname(conn, 'Unknown')
    find_clients_email(conn, 'togawaunkown@gmail.com')
    find_clients_phone_number(conn, '99999999997')
conn.close()