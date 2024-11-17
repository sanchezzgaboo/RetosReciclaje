from ultralytics import YOLO 

# Load a smaller model
model = YOLO("yolo11n.pt")  # Ensure this is a lightweight version, like YOLOv11 Nano or Small

# Train the model with optimizations for limited resources
train_results = model.train(
    data="taco_dataset.yaml",  # path to dataset YAML
    epochs=50,                   # fewer epochs to reduce runtime
    imgsz=320,                   # lower image size to fit into memory
    batch=2,                # lower batch size to reduce VRAM usage
    device="cpu",                    # specify GPU, or use 'cpu' if no GPU is available
    half=True                    # enable mixed precision for memory savings
)

# Evaluate model performance on the validation set
metrics = model.val()

# Perform object detection on an image
results = model("path/to/image.jpg")
results[0].show()

# Export the model to ONNX format
path = model.export(format="onnx")  # returns path to exported model
