import re
import ast

# Step 1: Read the dictionary from the text file
with open('C:\\Users\\gsanc\\OneDrive\\Documents\\Python\\RetosReciclaje\\YOLO11\\names.txt', 'r') as file:
    # Read lines and concatenate them into a single string
    content = ''.join(line.strip() for line in file)

# Step 2: Clean up the content by removing unwanted newlines
# This regex will match any newline followed by a non-whitespace character
cleaned_content = re.sub(r'\n(?=\S)', ' ', content)

# Step 3: Convert the cleaned string representation of the dictionary to an actual dictionary
try:
    dictionary = ast.literal_eval(cleaned_content)
except (SyntaxError, ValueError) as e:
    print("Error parsing dictionary:", e)
    exit(1)

# Step 4: Create a new formatted string
formatted_output = []

for key, value in dictionary.items():
    formatted_output.append(f"{key}: {value}")
    if isinstance(value, (int, float)):  # Check if the value is a number
        formatted_output.append("\n")  # Add a newline if the value is a number

# Join the formatted output into a single string
output_string = ''.join(formatted_output)

# Step 5: Write the organized output to a new text file
with open('organized_data.txt', 'w') as file:
    file.write(output_string)

print("Organized data has been written to 'organized_data.txt'.")