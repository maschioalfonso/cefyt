#!/usr/bin/env python
from sys import argv

SEPARATOR = ","
NUMERO_GIRE = "4057"

def main():

    if len(argv) != 2:
        print("Use: ./procesar_pagos <archivo>")
        return 0;

    filename = argv[1]
    f = open(filename, 'r')

    #Nombre de archivo
    print("Archivo: " + filename)

    # Encabezado
    header = SEPARATOR.join(["Fecha de pago", "id. Alumno", "id. Cuota", "Monto"])
    print(header)

    exclude = []
    for line in f:

        if line[23:23+4] != NUMERO_GIRE:
            exclude.append(line)
            continue

        # Fecha de pago
        payment_date = "/".join([line[6:6+2], line[4:4+2], line[0:4]])

        # Id. alumno
        student_id = line[27:27+5]

        # Id. cuota
        fee_id = line[33:33+6]

        # Monto
        amount = line[39:39+4] + "." + line[43:43+2]

        row = SEPARATOR.join([payment_date, student_id, fee_id, amount])

        print(row)

    # Líneas excluídas
    print("")
    print("Líneas excluídas:")
    for line in exclude:
        print(line[0:-2])


if __name__ == "__main__":
    main()