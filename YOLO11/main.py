import cv2
import argparse
from ultralytics import YOLO
import supervision as sv
import inference
import os
import shutil
from PIL import Image
from roboflow import Roboflow

def flush_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Iterate over all the files and directories in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                # Check if it's a file or directory and remove accordingly
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

# Example usage

ROBOFLOW_API_KEY="ole2IjYlEPXdtasKC1Sx"
path = 'C:\\Users\gsanc\\OneDrive\\Documents\\Python\\RetosReciclaje\\images'


rf = Roboflow(api_key=ROBOFLOW_API_KEY)
project = rf.workspace().project("deteccionreciclaje")
model = project.version(1).model
#Arreglar resolucion 
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv11 live")
    parser.add_argument("--webcam-resolution", default=[1280,720], nargs=2, type=int)
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution
    cap = cv2.VideoCapture(0) #Acceder a la camara
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width) #Arreglar la anchura de la resolucion 
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height) # Arreglar la altura de la resolucion
    while True:
        ret, frame = cap.read() #Leer el frame
        k = cv2.waitKey(1)
        img_name = ""
        img_counter = 0
        

        cv2.imshow('yolov11', frame)
        
        if k % 256 == 32:
            img_name = f"opencv_frame_{img_counter}.png"
            
            saved_image = cv2.imwrite(os.path.join(path, f"{img_name}"),frame)

            result = model.predict(f"{path}\\opencv_frame_{img_counter}.png").json()
            
            # SPACE pressed
            
            print(f"{img_name} written!")
            img_counter += 1
            for pred in result["predictions"][0]['predictions']:
                if pred["confidence"] > 0.5:
                    print(pred["class"])
        
        if(k == 27): #Asignar escape como cierre
            break

if __name__ == "__main__":
    flush_folder(path)
    main()