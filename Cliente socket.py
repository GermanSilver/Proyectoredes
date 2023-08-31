import socket

HOST = "127.0.0.1"  # dominio  o IP del servidor
PORT = 54321  # el puerto del servidor

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"/Hola soy el cliente")
    
    data = s.recv(1024)
if b'/' in data:
    print(f"Comando recibido cliente {data!r}")
else:
    print(f"Sin Comando cliente {data!r}")


