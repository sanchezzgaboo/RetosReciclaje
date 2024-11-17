from ultralytics import YOLO
import cv2
import urllib.request
import numpy as np
import serial

#def conectar_motores() -> serial.Serial:

ser = serial.Serial()
ser.baudrate = 115200

ser.port = 'COM6'
ser.open()
#return ser

# Replace the URL with the IP camera's stream URL
url = 'http://172.20.10.5/cam-lo.jpg' #Direccion del servidor

#model to use
model = YOLO('C:\\Users\\gsanc\\OneDrive\\Documents\\Python\\RetosReciclaje\\YOLO11\\yolo11x-cls.pt')
state = 0

opcion = input("Ingrese 0 si desea usar la camara interna o 1 si desea usar la esp32cam: ")
im = ""
while True:
    if(opcion == "\n" or opcion == "0"):
        videoCap = cv2.VideoCapture(0) #Si se quiere usar la camara del compu
        ret, im = videoCap.read() #frame de la camara
    elif(opcion == "1"):
        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        im = cv2.imdecode(imgnp,-1)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    results = model.predict(source=im, show=True, save=True, conf=0.6, line_width=2, save_crop=False, save_txt=False, show_labels=True, show_conf=True)
    for r in results:
        prediction = results[0].names[r.probs.top1]
    if("bottle" in prediction or "cup" in prediction or "beer" in prediction or "wine" in prediction or "plastic" in prediction or "bag" in prediction or "spoon" in prediction or "carton" in prediction):
        state = 1
    elif("paper" in prediction or "banana" in prediction or "tissue" in prediction or "Granny" in prediction or "smith" in prediction or "handkerchief" in prediction):
        state = 2
    else:
        state = 0
    if 0 <= state <= 3:
        ser.write(str(state).encode())  # Send the state as a single character
        print(f"Sent state: {state}", prediction)
    else:
        print("Invalid state. Must be between 0 and 3.")
ser.close()
cv2.destroyAllWindows()