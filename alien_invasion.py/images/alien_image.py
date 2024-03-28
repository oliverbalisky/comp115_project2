from PIL import Image
import os

# Ensure the "images" directory exists
os.makedirs("images", exist_ok=True)

# Load the image
image = Image.open("/Users/oliverbalisky/Downloads/pcc_3e-main/chapter_13/building_alien_fleet/images/alien_image_no_back.png")

# Save the image to the "images" directory
image.save("images/alien.bmp")
