import os
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

# Function to retrieve EXIF data from an image file
def get_exif_data(image_path):
    image = Image.open(image_path)
    exif_data = {}
    info = image._getexif()
    if info is not None:
        for tag, value in info.items():
            tag_name = TAGS.get(tag, tag)
            exif_data[tag_name] = value
    return exif_data

# Function to add a date and time stamp to the image
def add_timestamp(image_path, output_path, exif):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size

    date_time = exif['DateTime']
    date_time = date_time.replace(':', '-', 2)  # Replace first colon with comma

    fontsize = width//25
    # Define the font and size for the timestamp
    font = ImageFont.truetype("Pillow/Tests/fonts/DejaVuSans.ttf", fontsize)
    left, top, right, bottom = font.getmask(date_time).getbbox()
    print(left, top, right, bottom)
    # Define the position and color of the timestamp text
    text_position = (width - right - 10, height - fontsize)
    text_color = (255, 0, 0)  # Red

    # Add the timestamp text to the image
    draw.text(text_position, date_time, font=font, fill=text_color)

    # Save the modified image with the timestamp
    image.save(output_path)

    print("Timestamp added to the image.")

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filenames = askopenfilenames(defaultextension=".jpg .jpeg .png") # show an "Open" dialog box and return the path to the selected file

for filename in filenames:
    # Retrieve and display the EXIF data
    exif_data = get_exif_data(filename)

    # Ask user for a save filename
    output_path = os.path.splitext(filename)[0]+'-timestamped.jpg'

    # Add a timestamp to the image and save it
    add_timestamp(filename, output_path, exif_data)
