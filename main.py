import csv


ARCHIVO_CSV = "empleados.csv"
solicitudes = []


# Lee los empleados desde el archivo CSV y los guarda en una lista de diccionarios.
def leer_empleados():
    empleados = []

    try:
        with open(ARCHIVO_CSV, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                empleado = {
                    "dni": fila["dni"],
                    "nombre": fila["nombre"],
                    "dias_disponibles": int(fila["dias_disponibles"])
                }
                empleados.append(empleado)

        return empleados

    except FileNotFoundError:
        print("\nError!!! No se encontró el archivo empleados.csv.")
        return []


# Guarda los cambios de los empleados en el mismo archivo CSV.
def guardar_empleados(empleados):
    with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as archivo:
        campos = ["dni", "nombre", "dias_disponibles"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()

        for empleado in empleados:
            escritor.writerow(empleado)


def buscar_empleado(empleados, dni):
    for empleado in empleados:
        if empleado["dni"] == dni:
            return empleado

    return None


# Suma los días de solicitudes pendientes de un empleado.
def dias_pendientes(dni):
    total = 0

    for solicitud in solicitudes:
        if solicitud["dni"] == dni and solicitud["estado"] == "Pendiente":
            total = total + solicitud["cantidad"]

    return total


def pedir_dni():
    dni = input("BOT: Ingresa tu DNI: ")

    while not dni.isdigit() or len(dni) < 7 or len(dni) > 8:
        print("\nBOT: El DNI debe tener 7 u 8 números.")
        dni = input("\nBOT: Ingresa tu DNI nuevamente: ")

    return dni


def pedir_cantidad(dias_disponibles):
    while True:
        try:
            cantidad = int(input("\nBOT: Cuantos dias queres solicitar? "))

            if cantidad <= 0:
                print("BOT: La cantidad debe ser mayor que cero.")
            elif cantidad > dias_disponibles:
                print("\nBOT: No tenes suficientes dias disponibles.")
            else:
                return cantidad

        except ValueError:
            print("\nBOT: Debes ingresar un numero entero (Ejemplo: 5)")


def solicitar_vacaciones(empleados):
    print("\n--- CHATBOT DE VACACIONES ---")
    print("BOT: Hola. Soy el asistente de Recursos Humanos.")

    dni = pedir_dni()
    empleado = buscar_empleado(empleados, dni)

    # Compuerta BPMN: ¿el empleado existe?
    if empleado is None:
        print("\nBOT: El empleado no existe, contacta a Recursos Humanos!!!")
        return

    print("\nBOT: Hola", empleado["nombre"] + ".")

    # Se descuentan las solicitudes pendientes para no pedir dos veces los mismos días.
    disponibles_reales = empleado["dias_disponibles"] - dias_pendientes(dni)

    # Compuerta BPMN: ¿tiene días disponibles?
    if disponibles_reales <= 0:
        print("\nBOT: No tenes dias de vacaciones disponibles.")
        return

    print("BOT: Tenes", disponibles_reales, "días disponibles.")
    cantidad = pedir_cantidad(disponibles_reales)

    solicitud = {
        "dni": empleado["dni"],
        "nombre": empleado["nombre"],
        "cantidad": cantidad,
        "estado": "Pendiente"
    }

    solicitudes.append(solicitud)
    print("\nBOT: Solicitud registrada como PENDIENTE.")
    print("BOT: Recursos Humanos la revisará.")


def ver_solicitudes():
    print("\n------------ SOLICITUDES -----------------")

    if len(solicitudes) == 0:
        print("\nNo hay solicitudes cargadas.")
        return

    # Ordenamiento alfabético por nombre (método burbuja).
    solicitudes_ordenadas = solicitudes[:]

    for i in range(len(solicitudes_ordenadas) - 1):
        for j in range(len(solicitudes_ordenadas) - 1 - i):
            if solicitudes_ordenadas[j]["nombre"] > solicitudes_ordenadas[j + 1]["nombre"]:
                auxiliar = solicitudes_ordenadas[j]
                solicitudes_ordenadas[j] = solicitudes_ordenadas[j + 1]
                solicitudes_ordenadas[j + 1] = auxiliar

    for solicitud in solicitudes_ordenadas:
        print("Empleado:", solicitud["nombre"])
        print("DNI:", solicitud["dni"])
        print("Dias solicitados:", solicitud["cantidad"])
        print("Estado:", solicitud["estado"])
        print("-" * 30)


def revisar_solicitud(empleados):
    print("\n--------------- REVISIÓN DE SOLICITUDES ----------------------")
    pendientes = []

    for solicitud in solicitudes:
        if solicitud["estado"] == "Pendiente":
            pendientes.append(solicitud)

    if len(pendientes) == 0:
        print("\nNo hay solicitudes pendientes.")
        return

    for posicion in range(len(pendientes)):
        solicitud = pendientes[posicion]
        print(posicion + 1, "-", solicitud["nombre"], "pidió", solicitud["cantidad"], "día(s).")

    try:
        opcion = int(input("\nElegi el número de solicitud: "))
    except ValueError:
        print("\nError!!! Debes ingresar un número válido.")
        return

    if opcion < 1 or opcion > len(pendientes):
        print("\nOpción inválida.")
        return

    solicitud = pendientes[opcion - 1]
    decision = input("\nEscribí A (aprovado) o R (rechazado): ").upper()

    if decision == "A":
        solicitud["estado"] = "Aprobada"
        empleado = buscar_empleado(empleados, solicitud["dni"])
        empleado["dias_disponibles"] = empleado["dias_disponibles"] - solicitud["cantidad"]
        guardar_empleados(empleados)
        print("Solicitud aprobada.")
        print("Se actualizó el saldo en empleados.csv.")

    elif decision == "R":
        solicitud["estado"] = "Rechazada"
        print("Solicitud rechazada.")

    else:
        print("Decision invalida. La solicitud sigue pendiente.")


def ver_estadisticas():
    aprobadas = 0
    rechazadas = 0
    pendientes = 0

    for solicitud in solicitudes:
        if solicitud["estado"] == "Aprobada":
            aprobadas = aprobadas + 1
        elif solicitud["estado"] == "Rechazada":
            rechazadas = rechazadas + 1
        else:
            pendientes = pendientes + 1

    print("\n--- ESTADISTICAS ---")
    print("Total de solicitudes:", len(solicitudes))
    print("Aprobadas:", aprobadas)
    print("Rechazadas:", rechazadas)
    print("Pendientes:", pendientes)


def menu_principal():
    empleados = leer_empleados()
    opcion = ""

    while opcion != "5":
        print("\n================== MENU ====================")
        print("1. Solicitar vacaciones")
        print("2. Ver solicitudes")
        print("3. Revisar solicitud")
        print("4. Ver estadísticas")
        print("5. Salir")
        opcion = input("\nElegi una opción: ")

        if opcion == "1":
            solicitar_vacaciones(empleados)
        elif opcion == "2":
            ver_solicitudes()
        elif opcion == "3":
            revisar_solicitud(empleados)
        elif opcion == "4":
            ver_estadisticas()
        elif opcion == "5":
            print("\nFin del programa. Gracias por usar el chatbot. Hasta luego!")
        else:
            print("\nOpcion invalida. Elegí un número del 1 al 5.")


menu_principal()