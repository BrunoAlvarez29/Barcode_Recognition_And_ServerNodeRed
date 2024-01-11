from pyzbar import pyzbar
import cv2
import time
import socket

# PROTOCOLO TCP
# Dirección IP y puerto del nodo tcp in en Node-RED
node_red_ip = '127.0.0.1' 
node_red_port = 29042  # Puerto configurado en tu nodo tcp in

def enviar_datos_a_node_red(dato):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((node_red_ip, node_red_port))
            s.sendall(str(dato).encode())
            print(f"Dato {dato} enviado a Node-RED correctamente.")
    except Exception as e:
        print(f"Error al enviar dato a Node-RED: {e}")

# Activamos la camara        
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error")

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            
            # Obtiene el último dígito del código de barras
            ultimo_digito = int(barcodeData[-1]) if barcodeData else None

            if ultimo_digito in [1, 2, 3, 4]:
                print(f"Último dígito detectado: {ultimo_digito}")
                enviar_datos_a_node_red(ultimo_digito)

            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeType = barcode.type
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            print("{}".format(barcodeData))
            time.sleep(0.15)

        cv2.imshow('Frame', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
