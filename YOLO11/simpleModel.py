from ultralytics import YOLO	
import serial

ser = serial.Serial()
	
ser.baudrate = 115200
ser.port = 'COM6'
	
ser.open()


model = YOLO('C:\\Users\\gsanc\\OneDrive\\Documents\\Python\\RetosReciclaje\\YOLO11\\yolo11n.pt')
results = model.predict(source="0", show=True, save=False, conf=0.6, line_width=2, save_crop=False, save_txt=False, show_labels=True, show_conf=True)


for result in results:
    print(result)
ser.write(results)

ser.close()
