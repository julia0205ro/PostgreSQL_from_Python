from PostgreSQL_from_Python import *

if __name__ == '__main__':
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
        update_data(conn, 1, name='Togawa')
        update_data(conn, 1, surname='Unknown')
        update_data(conn, 1, email='togawaunkown@gmail.com')
        update_phone_number(conn, 1,'99999999997')
        delete_phone_number(conn, 3)
        delete_client(conn, 3)
        find_clients_phone_number(conn, '99999999997')
        find_clients_info(conn, 'Unknown')
        find_clients_info(conn, 'togawaunkown@gmail.com', 'Togawa')
    conn.close()