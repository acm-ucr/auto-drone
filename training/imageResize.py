import os
from PIL import Image

def imageResize():
    input_directory = "p_unsized"
    output_directory = "p_sized"

    for file in os.listdir(input_directory):
        file_path = os.path.join(input_directory, file)

        try:
            with Image.open(file_path) as image:
                new_image = image.resize((640, 480))
                output_path = os.path.join(output_directory, file)
                new_image.save(output_path, 'JPEG')

        except Exception as e:
            print(f"{file_path} Could not be processed: {e}")

if __name__ == "__main__":
    imageResize()