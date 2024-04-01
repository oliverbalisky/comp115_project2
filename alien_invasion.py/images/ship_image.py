
from PIL import Image
import os

# Ensure the "images" directory exists
os.makedirs("images", exist_ok=True)

# Load the image
image = Image.open("/Users/oliverbalisky/Downloads/pcc_3e-main/chapter_12/adding_ship_image/images/ship_image_no_back.png")

# Save the image to the "images" directory
image.save("images/ship.bmp")