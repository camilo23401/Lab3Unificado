#coding=utf-8
# Importar librerias
import socket
import threading
import os
import hashlib
import sys
from datetime import datetime
from time import time

archivo = input("1.Enviar a cliente archivo de 100M \n2.Transmitir a clientes archivo de 250M")
numCliente = input("A cuantos clientes desea transmitir en simúltaneo")
nomArchivo = ""
tamano = 0
ruta = ""

directory_path = os.path.dirname(__file__)
def cambiarRuta(numArchivo):
    global ruta
    global tamano
    global nomArchivo
    if (numArchivo == "1"):
        ruta = os.path.join(directory_path, "ArchivosParaEnviar/Archivo100M.txt")
        tamano = 100
        nomArchivo = "Archivo100M"
    if (numArchivo == "2"):
        ruta = os.path.join(directory_path, "ArchivosParaEnviar/Archivo250M.txt")
        tamano = 200
        nomArchivo = "Archivo250M"

aux = 0
def conexionServ():
    global aux
    # Creamos el socket del servidor TCP:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket creado")

    # Se define el host
    host = "localhost"

    # Se define el puerto
    port = 6666+aux
    aux +=1
    path_log = "./Logs"
    year = datetime.now().year
    mes = datetime.now().month
    dia = datetime.now().day
    hora = datetime.now().hour
    min = datetime.now().minute
    seg = datetime.now().second

    fecha = "/" + str(year) + "-" + str(mes) + "-" + str(dia) + "-" + str(hora) + "-" + str(min) + "-" + str(
        seg) + "log"
    archivolog = path_log + fecha + ".txt"
    file = open(archivolog, "w")

    # Lo vinculamos al puerto con la función bind()
    sock.bind((host, port))
    print("Socket bind completado con host " + str(host) + " y puerto " + str(port))

    # Establecemos un *timeout*
    sock.settimeout(60)

    # Ponemos el servidor en modo escucha:
    sock.listen(int(numCliente))

    cambiarRuta(archivo)
    numeroConectados = 0

    while True & numeroConectados<=int(numCliente):
        # Se establece la conexion con el cliente
        connection, client_address = sock.accept()
        print ('Conexion obtenida de ', client_address)
        numeroConectados+=1
        print ("Recibiendo solicitudes...")
        print(numeroConectados);
        connection.recv(4096)
        print("Recibio respuesta del cliente")

        datax = open(ruta, encoding='utf-8')

        hash = hashlib.sha256()
        start_time=time()
        cant_paquetes=0
        peso_tot=0
        fb = datax.read(65536)
        while len(fb) > 0:
            hash.update(fb.encode('utf-8'))
            fb = datax.read(65536)
        resultadoHash = hash.hexdigest()
        strHas = str(resultadoHash).encode('utf-8')
        connection.send(bytes(strHas))
        print("Se envió el HASH al cliente")

        data = open(ruta, encoding='utf-8')
        dr = data.read(4096)
        while len(dr) > 0:
            connection.send(dr.encode('utf-8'))
            print("Enviando paquete")
            dr = data.read(4096)
            cant_paquetes = cant_paquetes + 1
        print("Todos los paquetes fueron enviados")
        peso_tot=peso_tot+float(os.path.getsize(ruta))
        file.write("\n El archivo enviado fue: "+ nomArchivo )
        file.write("\n El tamaño del archivo es: "+ str(tamano)+"MB")
        file.write("\n La entrega fue exitosa")
        file.write("\n El cliente al que fue enviado el archivo: "+str(client_address))
        file.write("\n El peso total transferido fue: "+str(peso_tot))
        file.write("\n La cantidad de paquetes transferida fue: "+str(cant_paquetes))
        file.write("\n El tiempo de transferencia fue: "+str(time()-start_time)+" seg")
        connection.shutdown(socket.SHUT_WR)
        file.close()
        connection.shutdown(2)
        connection.close()
        sock.close()
        break

    #print("Conexion enviada")
    #if data == b"DONE":
    #    print("Done Receiving.")
    #    break
    #file.write(data)

for num_hilo in range(int(numCliente)):
    hilo = threading.Thread(target=conexionServ,name='Servidor'+str(num_hilo))
    hilo.start()

