import json
import os
import shutil

# Define paths for annotations and images
annotations = {
    "train": "C:\\Users\\gsanc\\OneDrive\\Documents\\Python\\RetosReciclaje\\TACO\\detector\\data\\batch_1\\annotations_0_train.json",
    "val": "C:\\Users\\gsanc\\OneDrive\\Documents\\Python\\RetosReciclaje\\TACO\\detector\\data\\batch_1\\annotations_0_val.json",
    "test": "C:\\Users\\gsanc\\OneDrive\\Documents\\Python\\RetosReciclaje\\TACO\\detector\\data\\batch_1\\annotations_0_test.json"
}
images_dir = "C:\\Users\\gsanc\\OneDrive\\Documents\\Python\\RetosReciclaje\\TACO\\detector\\data"  # Folder where all images are stored

# Define YOLO output directory structure
output_dir = "taco_yolo_1"
for split in ["train", "val", "test"]:
    os.makedirs(os.path.join(output_dir, "images", split), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "labels", split), exist_ok=True)

# Function to convert bounding boxes to YOLO format
def convert_bbox(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[2] / 2.0) * dw
    y = (box[1] + box[3] / 2.0) * dh
    w = box[2] * dw
    h = box[3] * dh
    return x, y, w, h

# Convert each annotation file
for split, annotation_path in annotations.items():
    # Load annotations
    with open(annotation_path) as f:
        data = json.load(f)

    # Class names (from TACO annotations)
    categories = {cat['id']: cat['name'] for cat in data['categories']}
    classes = list(categories.values())

    # Process each image in the annotation file
    for img in data['images']:
        file_name = img['file_name']
        width, height = img['width'], img['height']
        
        # Copy images to YOLO images folder
        image_path = os.path.join(images_dir, file_name)
        output_image_path = os.path.join(output_dir, "images", split, file_name)
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)  # Ensure directory exists
        if os.path.exists(image_path):
            shutil.copy(image_path, output_image_path)
        
        # Create label file for each image in taco_yolo/labels/{split} folder
        label_file_name = os.path.splitext(file_name)[0] + ".txt"
        label_file_path = os.path.join(output_dir, "labels", split, label_file_name)
        
        # Ensure the directory for the label file exists
        os.makedirs(os.path.dirname(label_file_path), exist_ok=True)
        
        # Generate the labels in the correct directory
        with open(label_file_path, "w") as f:
            for ann in data['annotations']:
                if ann['image_id'] == img['id']:
                    cat_id = ann['category_id']
                    class_id = classes.index(categories[cat_id])
                    
                    # Convert bounding box
                    bbox = ann['bbox']
                    yolo_bbox = convert_bbox((width, height), bbox)
                    
                    # Write to label file
                    f.write(f"{class_id} " + " ".join(map(str, yolo_bbox)) + "\n")
