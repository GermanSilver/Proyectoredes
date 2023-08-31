import socket

HOST = '127.0.0.1'
PORT = 54321  

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Conestado desde {addr}")
        
        while True:
            data = conn.recv(1024)
            if b'/' in data:
                conn.send(b"Comando recibido")
            if not data:
                break
            conn.sendall(data)

