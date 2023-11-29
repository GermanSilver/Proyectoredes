import requests
from requests import Session
from lxml import etree, html
from DatabaseHelper import DatabaseHelper
from datetime import datetime, timedelta

class Cotizaciones:
    def __init__(self):
        self.session = Session()
        self.monedas = [
            {"nombre": "Dolar US", "codigo": 2},
            {"nombre": "Peso Argento", "codigo": 80},
            {"nombre": "Real", "codigo": 12},
            {"nombre": "Peso chileno", "codigo": 11}
        ]
        self.dbh = DatabaseHelper()

                    
    def historico(self):
        self.dbh.DBQuery("Delete from cotizacion_historico")
        for moneda in self.monedas:
            payload = {
                "Fecha": "2023.10.01",
                "Moneda": moneda['codigo'],
                "Nomoneda": moneda['nombre']
            }
            response = self.session.post(url="http://www.bcra.gob.ar/PublicacionesEstadisticas/Evolucion_moneda_2.asp", data=payload)

            tree = html.fromstring(response.text)
            filas = tree.xpath("//table/tr")
            for fila in filas:
                fecha = fila[0].text.replace("\r", "").replace("\n", "")
                equivausd = fila[1].text.replace("\r", "").replace("\n", "")
                equivapeso = fila[2].text.replace("\r", "").replace("\n", "")
                codigo_moneda = moneda['codigo']
                nombre_moneda = moneda['nombre']
                arrayValores = [
                    {"fecha": fecha},
                    {"equivausd": equivausd},
                    {"equivapeso": equivapeso},
                    {"moneda": codigo_moneda}
                ]
                self.dbh.DBQuery(self.dbh.constructorInsert("cotizacion_historico", arrayValores))
                print("Insertado: " + fecha + "   " + str(nombre_moneda))
                
        self.dbh.commit()
        self.menu()

    def actualizacion(self):
            result = self.dbh.DBQuery("SELECT MAX(fecha) FROM cotizacion_historico")
            fecha_max = result[0]['MAX(fecha)']
            if fecha_max is not None: 
            
                fecha_actualizacion = (fecha_max + timedelta(days=1)).strftime("%Y.%m.%d")  
            else:
                    print("No hay datos de cotización en la base de datos. Por favor elija la opción '1. Histórico'")
                    self.menu()
                    return 

            print("\nLas cotizaciones están actualizadas al: " + str(result[0]['MAX(fecha)']))
            actualiza = input("\n¿Desea actualizar las cotizaciones a la fecha actual? (S/N):" )
            hoy = datetime.now().date()
            
            if actualiza.upper() == "S":
                if fecha_max < hoy:
                    for moneda in self.monedas:
                        payload = {
                            "Fecha": fecha_actualizacion,
                            "Moneda": moneda['codigo'],
                            "Nomoneda": moneda['nombre']
                        }
                        response = self.session.post(url="http://www.bcra.gob.ar/PublicacionesEstadisticas/Evolucion_moneda_2.asp", data=payload)

                        tree = html.fromstring(response.text)
                        filas = tree.xpath("//table/tr")
                        arrayValores=[]
                        for fila in filas:
                            fecha = fila[0].text.replace("\r", "").replace("\n", "")
                            equivausd = fila[1].text.replace("\r", "").replace("\n", "")
                            equivapeso = fila[2].text.replace("\r", "").replace("\n", "")
                            codigo_moneda = moneda['nombre']
                            nombre_moneda = moneda['nombre']

                            arrayValores = [
                                {"fecha": fecha},
                                {"equivausd": equivausd},
                                {"equivapeso": equivapeso},
                                {"moneda": codigo_moneda}
                            ]
                            self.dbh.DBQuery(self.dbh.constructorInsert("cotizacion_historico", arrayValores))
                            print("Insertado: " + fecha + "   " + str(nombre_moneda))

                    self.dbh.commit()

                    if not arrayValores:
                        print("No se pudo obtener datos de cotizaciones. Verifique la fecha de actualizacón.")
                        self.actualizacion()    
                            
                    print("\nSe actualizó la BD a la fecha actual")
                else:
                    print("La BD no requiere actualización")
            self.menu()

    def consulta_especifica(self):
        fechas_limites = self.dbh.DBQuery("SELECT MAX(fecha), MIN(fecha) FROM cotizacion_historico")
        print(f"\nSe pueden consultar datos entre {fechas_limites[0]['MIN(fecha)']} y {fechas_limites[0]['MAX(fecha)']}" )
        print("Si la fecha a consultar no está en el rango, puede actualizar datos desde el menú (el histórico parte del 2023-01-01)")
        opcionvolver=input("Desea continuar S/N: ")
        if opcionvolver.upper() =="N": self.menu()

        print("(Tenga en cuenta que no hay cotizaciones para sábados, domingos y feriados)")
        fecha_consulta = input("Ingrese la fecha en formato 'YYYY-MM-DD': ")
        tipo_moneda = self.tipoMonedas()
        
        result = self.dbh.DBQuery(f"SELECT distinct fecha, equivausd, equivapeso, moneda, nombre_moneda from cotizacion_historico inner join moneda on id_moneda = moneda WHERE fecha = '{fecha_consulta}' AND moneda = '{tipo_moneda['codigo']}'")
        if not result:
            print(f"No hay datos para la fecha {fecha_consulta} y el tipo de moneda {tipo_moneda['nombre']}.")
        else:
            print(f"\nCotizaciones para la fecha {fecha_consulta} y el tipo de moneda {tipo_moneda['nombre']}:")
            for row in result:
                print(f"Fecha: {row['fecha']}, Equiv. USD: {row['equivausd']}, Equiv. Peso: {row['equivapeso']}, Moneda: {row['nombre_moneda']}")
    
    def consulta_rango(self):
        fechas_limites = self.dbh.DBQuery("SELECT MAX(fecha), MIN(fecha) FROM cotizacion_historico")
        print(f"\nSe pueden consultar datos entre {fechas_limites[0]['MIN(fecha)']} y {fechas_limites[0]['MAX(fecha)']}" )
        print("Si la fecha a consultar no está en el rango, puede actualizar datos desde el menú (el histórico parte del 2023-01-01)")
        
        opcionvolver=input("Desea continuar S/N: ")
        
        if opcionvolver.upper() =="S":
            print("(Tenga en cuenta que no hay cotizaciones para sábados, domingos y feriados)")
            fecha_inicio = input("Ingrese la fecha de inicio en formato 'YYYY-MM-DD': ")
            fecha_fin = input("Ingrese la fecha de fin en formato 'YYYY-MM-DD': ")
            tipo_moneda = self.tipoMonedas()
            
            if fecha_fin < fecha_inicio: 
                print("La fecha de fin del rango no puede mayor a la fecha de inicio")
                self.consulta_rango
            result = self.dbh.DBQuery(f"SELECT * FROM cotizacion_historico WHERE fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}' AND moneda = '{tipo_moneda['codigo']}'")

            if not result:
                print(f"No hay datos para el rango de fechas {fecha_inicio} a {fecha_fin} y el tipo de moneda {tipo_moneda['nombre']}.")
            else:
                print(f"\nCotizaciones para el rango de fechas {fecha_inicio} a {fecha_fin} y el tipo de moneda {tipo_moneda['nombre']}:")
                for row in result:
                    print(f"Fecha: {row['fecha']}, Equiv. USD: {row['equivausd']}, Equiv. Peso: {row['equivapeso']}, Moneda: {tipo_moneda['nombre']}")

        else:
            self.menu()

    def consulta_diferencia(self):
        fechas_limites = self.dbh.DBQuery("SELECT MAX(fecha), MIN(fecha) FROM cotizacion_historico")
        print(f"\nSe pueden consultar datos entre {fechas_limites[0]['MIN(fecha)']} y {fechas_limites[0]['MAX(fecha)']}" )
        print("Si la fecha a consultar no está en el rango, puede actualizar datos desde el menú (el histórico parte del 2023-01-01)")
        
        opcionvolver=input("Desea continuar S/N: ")
        
        if opcionvolver.upper() =="S":
            print("(Tenga en cuenta que no hay cotizaciones para sábados, domingos y feriados)")
            fecha_inicio = input("Ingrese la fecha de inicio en formato 'YYYY-MM-DD': ")
            fecha_fin = input("Ingrese la fecha de fin en formato 'YYYY-MM-DD': ")
            tipo_moneda = self.tipoMonedas()
            
            if fecha_fin <= fecha_inicio: 
                print("La fecha de fin del rango debe ser mayor a la fecha de inicio")
                self.consulta_rango
            dato_antiguo=
            result = self.dbh.DBQuery(f"SELECT * FROM cotizacion_historico WHERE where fecha='{fecha_inicio}' OR fecha='{fecha_fin}' AND moneda = '{tipo_moneda['codigo']}'")

            if not result:
                print(f"No hay datos para el rango de fechas {fecha_inicio} a {fecha_fin} y el tipo de moneda {tipo_moneda['nombre']}.")
            else:
                print(f"\nCotizaciones para el rango de fechas {fecha_inicio} a {fecha_fin} y el tipo de moneda {tipo_moneda['nombre']}:")
                for row in result:
                    print(f"Fecha: {row['fecha']}, Equiv. USD: {row['equivausd']}, Equiv. Peso: {row['equivapeso']}, Moneda: {tipo_moneda['nombre']}")

        else:
            self.menu()

    def tipoMonedas(self):
        while True:
            print("\n      *** Monedas ***   ")
            print("-" * 25)
            print("| 1. Dolar US")
            print("| 2. Peso Argento")
            print("| 3. Real")
            print("| 4. Peso chileno")
            print("-" * 25)
            opcion = input("Ingrese una opción: ")

            monedas = {
                "1": {"codigo": 2, "nombre": "Dolar US"},
                "2": {"codigo": 80, "nombre": "Peso Argento"},
                "3": {"codigo": 12, "nombre": "Real"},
                "4": {"codigo": 11, "nombre": "Peso chileno"}
            }

            if opcion in monedas:
                return monedas[opcion]
            else:
                print("Opción inválida. Intente nuevamente.")

    
    def menu(self):
            while True:
                print("\n      *** Menú ***   ")
                print("-"*25)
                print("| Carga de datos:")
                print("| 1. Histórico")
                print("| 2. Actualización")
                print("| ")
                print("| Consultas:")
                print("| 3. Fecha específica")
                print("| 4. Consulta por rango de fechas")
                print("| 5. Diferencia")
                print("| 6. Atender cliente externo")
                print("| 0. Salir")
                print("-"*25)
                opcion = input("Ingrese una opción: ")

                if opcion == "1":
                    self.historico()
                elif opcion == "2":
                    self.actualizacion()
                elif opcion == "3":
                    self.consulta_especifica()
                elif opcion == "4":
                    self.consulta_rango()
                elif opcion == "5":
                    self.consulta_diferencia()
                elif opcion == "6":
                    self.servidor()
                elif opcion == "0":
                    break
                else:
                    print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    espiabcra = Cotizaciones()
    espiabcra.menu()
