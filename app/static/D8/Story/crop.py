import os
import subprocess

# Path to the base directory where the folders are located
base_directory = os.getcwd()  # Change this to your base directory

# Crop parameters
crop_width = 262
crop_height = 136
crop_x = 9
crop_y = 157

# Function to crop images using ImageMagick
def crop_image(input_path, output_path):
    # ImageMagick command to crop the image and output as PNG
    command = [
        'magick', input_path,  # Use 'convert' if older version of ImageMagick
        #'-crop', f'{crop_width}x{crop_height}+{crop_x}+{crop_y}',
        output_path
    ]
    
    # Execute the command
    subprocess.run(command)

# Loop through each folder with the required name pattern (01, 02, ..., 99)
for i in range(1, 100):  # Adjust range if needed
    # Format the folder name as two digits (e.g., 01, 02, ..., 99)
    folder_name = f'KDS_rivalportrait_{i:02d}_n_D8'
    folder_path = os.path.join(base_directory, folder_name)
    
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Loop through all .dds files in the folder
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".dds"):
                input_file_path = os.path.join(folder_path, file_name)
                output_file_path = os.path.join(os.getcwd(), f'{i}.png')  # Save as .png
                
                # Crop the image and save to output file in PNG format
                crop_image(input_file_path, output_file_path)
                print(f"Cropped image saved as: {output_file_path}")
    else:
        print(f"Folder {folder_name} does not exist.")
