#coding=utf-8
# Importar librerias
import socket
import threading
import os
import hashlib
import sys
from datetime import datetime
from time import time

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

while True:
    # Se establece la conexion con el cliente
    connection, client_address = sock.accept()
    print ('Conexion obtenida de ', client_address)
    print ("Recibiendo...")
    connection.recv(4096)
    print("Recibio respuesta del cliente")
    directory_path = os.path.dirname(__file__)
    ruta = os.path.join(directory_path,"ArchivosParaEnviar/ArchivoPrueba.txt")

    data = open(ruta, encoding='utf-8')
    dr = data.read(4096)
    while len(dr) > 0:
        connection.send(dr.encode('utf-8'))
        print("Enviando paquete")
        dr = data.read(4096)
    print("Todos los paquetes fueron enviados")

    file.write("\n El archivo enviado fue : ")
    file.write("\n El peso fue de :"+str(os.path.getsize(ruta))+" Bytes")
    cant_paquetes=cant_paquetes+1
    peso_tot=peso_tot+float(os.path.getsize(ruta))
    file.write("\n Entrega exitosa: ")
    file.write("\n Cliente: "+ str(client_address))

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

file.write("\n Cantidad de paquetes recibidos: "+str(cant_paquetes))
file.write("\n total bytes recibidos: "+str(peso_tot))
file.write("\n Tiempo de transferencia: "+str(time()-start_time)+"seg")

file.close()
sock.close()
