import socket

class ClienteCotizacion:
    def __init__(self):
        self.servidor_host = '127.0.0.1'  # Cambia esto con la dirección IP del servidor
        self.servidor_puerto = 2345

    def conectar_servidor(self):
        # Crea un socket para la conexión con el servidor
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conecta al servidor
        cliente.connect((self.servidor_host, self.servidor_puerto))

        return cliente

    def obtener_cotizacion(self, fecha):
        # Conecta con el servidor
        cliente = self.conectar_servidor()

        try:
            # Envía la fecha al servidor
            cliente.sendall(fecha.encode())

            # Recibe la respuesta del servidor
            cotizacion = cliente.recv(1024).decode()
            return cotizacion
        finally:
            # Cierra la conexión
            cliente.close()

if __name__ == "__main__":
    cliente = ClienteCotizacion()
    print("\n(Verifique que la consulta corresponda a un día hábil)")
    fecha = input("Ingrese la fecha en formato YYYY-MM-DD: ")

    # Obtiene la cotización del servidor
    cotizacion = cliente.obtener_cotizacion(fecha)
    print(f"La cotización para la fecha {fecha} es: {cotizacion}")
