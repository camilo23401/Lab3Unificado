#coding=utf-8
#Importar librerias
import socket
import threading
import os
import hashlib
import sys
from datetime import datetime
from time import time

archivo = input(" 1.Enviar a clientes archivo de 100M  \n 2.Enviar a clientes archivo de 250M   ")
numCliente = input(" A cuantos clientes desea transmitir en simúltaneo?   ")
nomArchivo = ""
tamano = 0
ruta = ""

directory_path = os.path.dirname(__file__)
def cambiarRuta(numArchivo):
    global ruta
    global tamano
    global nomArchivo
    if (numArchivo == "1"):
        ruta = os.path.join(directory_path, "ArchivosParaEnviar/ArchivoPrueba.txt")
        tamano = 100
        nomArchivo = "Archivo100M"
    if (numArchivo == "2"):
        ruta = os.path.join(directory_path, "ArchivosParaEnviar/Archivo200M.txt")
        tamano = 200
        nomArchivo = "Archivo250M"

# Creamos el socket del servidor TCP:
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket creado")

# Se define el host
host = "localhost"

cant_paquetes = 0
peso_tot = 0
start_time=time()

# Se define el puerto
port = 6666

# Se define el log del servidor
path_logs = "./Logs"

# Lo vinculamos al puerto con la función bind()
sock.bind((host, port))
print ("Socket bind completado con host " +str(host)+" y puerto "+str(port))

# Obtenemos variables de tiempo para poner en el log
year=datetime.now().year
mes = datetime.now().month
dia = datetime.now().day
hora= datetime.now().hour
min = datetime.now().minute
seg = datetime.now().second

# Obtenemos variables de tiempo para poner en el log
fecha= "/"+str(year)+"-"+str(mes)+"-"+str(dia)+"-"+str(hora)+"-"+str(min)+"-"+str(seg)+"log"
print(fecha)
archivolog = path_logs+fecha+".txt"
file = open(archivolog, "w")

# Establecemos un *timeout*
sock.settimeout(60)

# Ponemos el servidor en modo escucha:
sock.listen(1)

connection, client_address = sock.accept()
cambiarRuta(archivo)

def conexionServ():
    numeroConectados = 0
    while True & ( int(numCliente) <= numeroConectados):
        # Se establece la conexion con el cliente
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
        print("Todos los paquetes fueron enviados")
        cant_paquetes=cant_paquetes+1
        peso_tot=peso_tot+float(os.path.getsize(ruta))
        file.write("\n El archivo enviado fue: "+ nomArchivo )
        file.write("\n El tamaño del archivo es: "+ str(tamano)+"MB")
        file.write("\n La entrega fue exitosa")
        file.write("\n El cliente al que fue enviado el archivo: "+str(client_address))
        file.write("\n El peso total transferido fue: "+str(peso_tot))
        file.write("\n La cantidad de paquetes transferida fue: "+str(cant_paquetes))
        file.write("\n El tiempo de transferencia fue: "+str(time()-start_time)+" seg")
        connection.shutdown(socket.SHUT_WR)

    datax = open(ruta, encoding='utf-8')

    hash = hashlib.sha256()
    fb = datax.read(65536)
    while len(fb) > 0:
        hash.update(fb.encode('utf-8'))
        fb = datax.read(65536)
    resultadoHash =  hash.hexdigest()
    print(sys.getsizeof(resultadoHash))
    print(resultadoHash)
    #connection.send(resultadoHash.encode('utf-8'))
    print("Se envió el HASH al cliente")
    connection.shutdown(socket.SHUT_WR)
    break
    #print("Conexion enviada")
    #if data == b"DONE":
    #    print("Done Receiving.")
    #    break
    #file.write(data)

for num_hilo in range(int(numCliente)):
    hilo = threading.Thread(target=conexionServ,name='Cliente'+str(num_hilo))
    hilo.start()

file.close()
#connection.send("Fin de la conexion")
connection.shutdown(2)
connection.close()
sock.close()
