import socket
import struct
import os
import json
import pymysql
import io
from config import PORT_FOR_SERVER, HOST, PORT_FOR_DB, PASSWORD, DB_NAME, NAME_TABLE, USER

def receive_file_size(sck: socket.socket):
    fmt = "<Q"
    expected_bytes = struct.calcsize(fmt)
    received_bytes = 0
    stream = bytes()

    while received_bytes < expected_bytes:
        chunk = sck.recv(expected_bytes - received_bytes)
        stream += chunk
        received_bytes += len(chunk)

    filesize = struct.unpack(fmt, stream)[0]

    return filesize

def receive_file(sck: socket.socket, filename):
    filesize = receive_file_size(sck)

    with open(filename, "wb") as f:
        received_bytes = 0

        while received_bytes < filesize:
            chunk = sck.recv(1024)

            if chunk:
                f.write(chunk)
                received_bytes += len(chunk)
    
    return read_json(filename)

def send_file(sck: socket.socket, filename):
    filesize = os.path.getsize(filename)

    sck.sendall(struct.pack("<Q", filesize))
    
    with open(filename, "rb") as f:
        while read_bytes := f.read(1024):
            sck.sendall(read_bytes)

def create_json(from_name: str, to_name: str, command: str, date: dict):
    to_json = {
        "from": from_name,
        "to": to_name,
        "command": command,
        "date": date
    }

    with open("new.json", 'w') as file:
        json.dumps(to_json, file)

        return file

def read_json(filename: str):
    with io.open(filename, encoding="utf-8") as file:
        l = json.load(file)



    if type(l) is list: ###this is json from check
        print("chek")
        
        
        new_l = []

        for elem in l[0]["ticket"]["document"]["receipt"]["items"]: 
            new_d = {elem["name"]: elem["quantity"]} 
            new_l.append(new_d) 

        return new_l
        
    else: ###this is our struct json
        print("our")

        return l

def update_date_from_check(date: list):
    try:
        connection = pymysql.connect(
            host=HOST,
            port=PORT_FOR_DB,
            user=USER,
            password=PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )

        print("Connection open...\n\n")

        try:
            with connection.cursor() as cursor:
                for elem in date:
                    name = list(elem.keys())[0]
                    colvo = elem.setdefault(list(elem.keys())[1])

                    insert_query = f"INSERT INTO {NAME_TABLE} (name, colvo) VALUES ('{name}, {colvo}');"
                    cursor.excecute(insert_query)
                connection.commit()

        finally:
            connection.close()
            print("Connection close...\n\n")

    except Exception as ex:
        print("Connection error")
        print(ex)
        


if __name__ == '__main__':
    server = socket.create_server((HOST, PORT_FOR_SERVER))

    colvo = 0

    while True:
        try:
            connection = pymysql.connect(
                host=HOST,
                port=PORT_FOR_DB,
                user=USER,
                password=PASSWORD,
                database=DB_NAME,
                cursorclass=pymysql.cursors.DictCursor
            )

            print("Connection open...\n\n")

            try:
                print("goood blait")

            finally:
                connection.close()
                print("Connection close...\n\n")

        except Exception as ex:
            print("Connection error")
            print(ex)


        # conn, addres = server.accept()
        # print("Тип подключен")
        # colvo += 1

        # list_or_dict = receive_file(conn, f"try{colvo}.json")

        # if type(list_or_dict) is list:
        #     update_date_from_check(list_or_dict)
        # else:
        #     l = []


        # conn.close()