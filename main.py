
#coding=utf-8
import socket
import os
import hashlib
from datetime import datetime
import threading
from time import time
import sys

def conexion():
    host = '127.0.0.1'
    port = 6666
    path_archivos = "./ArchivosRecibidos"
    path_logs = "./Logs"

    BLOCK_SIZE = 65536
    conexiones = 25
    obj = socket.socket()

    obj.connect((host, port))
    print("conecto")

    year=datetime.now().year
    mes = datetime.now().month
    dia = datetime.now().day
    hora= datetime.now().hour
    min = datetime.now().minute
    seg = datetime.now().second

    fecha= "/"+str(year)+"-"+str(mes)+"-"+str(dia)+"-"+str(hora)+"-"+str(min)+"-"+str(seg)+"log"
    print(fecha)
    archivolog = path_logs+fecha+".txt"
    file = open(archivolog, "w")

    cliente= threading.currentThread().getName()
    print("Cliente "+cliente)
    print("Conectado al servidor")
    start_time=time()
    cant_paquetes=0
    peso_tot=0
    while (True):
        obj.send(b"Mensaje de confirmacion. Listo para recibir un archivo")
        print("Se recibio un archivo del servidor")
        nombre_archivo = cliente + "-Prueba-" + str(conexiones)
        archivoPorEscribir = os.path.join(path_archivos, nombre_archivo)
        file1 = open(archivoPorEscribir, "wb")
        recibido = obj.recv(4096)
        while len(recibido)>0:
            print("Recibiendo paquete")
            file1.write(recibido)
            recibido = obj.recv(4096)
        print("Terminó la recepción de paquetes")
        file1.close()
        dataHash = open(archivoPorEscribir)
        file.write("\n El archivo recibido fue : "+nombre_archivo)
        file.write("\n El peso fue de :"+str(os.path.getsize(archivoPorEscribir))+" Bytes")
        cant_paquetes=cant_paquetes+1
        peso_tot=peso_tot+float(os.path.getsize(archivoPorEscribir))
        file.write("\n Entrega exitosa: ")
        file.write("\n Cliente: "+cliente)

# ------------------------------------- HASHING! ------------------------------------------------

        #print("En espera de hash por parte del servidor")
        #hash = obj.recv(4096)
        #hashstr = hash.decode('utf-8')
        #print(hashstr)
        #print("Verificando integridad")
        #hash = hashlib.sha256()
        #fb = recibido.read(65536)
        #while len(fb) > 0:
        #    hash.update(fb.encode('utf-8'))
        #    fb = recibido.read(65536)
        #resultadoHash = hash.hexdigest()
        #obj.send(resultadoHash.encode('utf-8'))
        #dataHash.close()
        #print("Cliente "+str(resultadoHash))
        #print("Servidor "+str(hash))
        #if(str(resultadoHash)==str(hash)):
        #    print("Coincide")


        if(os.path.getsize(archivoPorEscribir)!=0):
            file.write("si")
        else:
            file.write("no")
        break
    obj.close()
    file.write("\n Cantidad de paquetes recibidos: "+str(cant_paquetes))
    file.write("\n total bytes recibidos: "+str(peso_tot))
    file.write("\n Tiempo de transferencia: "+str(time()-start_time)+"seg")
    file.close()
    print("Conexión cerrada")


NUM_HILOS = 1

for num_hilo in range(NUM_HILOS):
    hilo = threading.Thread(target=conexion,name='Cliente'+str(num_hilo))
    hilo.start()

