#coding=utf-8
# Importar librerias
import socket
import threading
import os
import hashlib

# Creamos el socket del servidor TCP:
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket creado")

# Se define el host
host = "localhost"

# Se define el puerto
port = 6666

# Lo vinculamos al puerto con la función bind()
sock.bind((host, port))
print ("Socket bind completado con host " +str(host)+" y puerto "+str(port))

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
    connection.shutdown(socket.SHUT_WR)
    print("Todos los paquetes fueron enviados")

    #datax = open(ruta, encoding='utf-8')

    #hash = hashlib.sha256()
    #fb = datax.read(65536)
    #while len(fb) > 0:
    #    hash.update(fb.encode('utf-8'))
    #    fb = datax.read(65536)
    #resultadoHash =  hash.hexdigest()
    #connection.send(resultadoHash.encode('utf-8'))

    #print("Conexion enviada")
    #if data == b"DONE":
    #    print("Done Receiving.")
    #    break
    #file.write(data)
file.close()
connection.send("Fin de la conexion")
connection.shutdown(2)
connection.close()
sock.close()
