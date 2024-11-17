import os
import xml.etree.ElementTree as ET

def convert_voc_to_yolo(xml_file, txt_file, classes):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)

    with open(txt_file, "w") as f:
        for obj in root.findall("object"):
            class_name = obj.find("name").text
            if class_name not in classes:
                continue
            class_id = classes.index(class_name)

            bndbox = obj.find("bndbox")
            xmin = int(bndbox.find("xmin").text)
            ymin = int(bndbox.find("ymin").text)
            xmax = int(bndbox.find("xmax").text)
            ymax = int(bndbox.find("ymax").text)

            # Convert to YOLO format
            x_center = (xmin + xmax) / 2.0 / width
            y_center = (ymin + ymax) / 2.0 / height
            bbox_width = (xmax - xmin) / width
            bbox_height = (ymax - ymin) / height

            f.write(f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n")

# Example usage
xml_dir = "path/to/xml_annotations"
yolo_dir = "./yolo_annotations"
classes = ["class1", "class2"]  # Replace with your actual classes

for xml_file in os.listdir(xml_dir):
    if xml_file.endswith(".xml"):
        txt_file = os.path.join(yolo_dir, os.path.splitext(xml_file)[0] + ".txt")
        convert_voc_to_yolo(os.path.join(xml_dir, xml_file), txt_file, classes)
