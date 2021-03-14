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
print ("Socket bind completado con host " +host+" y puerto "+port)

# Establecemos un *timeout*
sock.settimeout(60)

file = open("img.png", "wb")
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
    ruta = os.path.join(directory_path,"ArchivosParaEnviar/Archivo100M.txt")
    data = open(ruta).read(4096)

    try:
        hash = hashlib.sha256()
        with open(data, "rb") as f:
            for bloque in iter(lambda: f.read(4096), b""):
                hash.update(bloque)
                hash.hexdigest()
    except Exception as e:
        print("Error: %s" % (e))
    except:
        print("Error desconocido")
        
    connection.send(data)
    print("Conexion enviada")
    #if data == b"DONE":
    #    print("Done Receiving.")
    #    break
    #file.write(data)
file.close()
connection.send("Fin de la conexion")
connection.shutdown(2)
connection.close()
sock.close()
