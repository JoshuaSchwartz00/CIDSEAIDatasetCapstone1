from PIL import Image, ImageDraw, ImageFont
import os
import glob

path = os.getcwd() + "\\img"
files = os.listdir(path)

count = 0

# CHANGE AS NEEDED TO READ FROM JSON AND ALTER IMAGES
for pic in files: 
    picture = os.getcwd() + "\\img2\\{:03d}".format(count) + ".png" # CHANGE AS NEEDED

    print(pic)

    #open image as a background
    with Image.open("img/" + pic) as image:
        draw = ImageDraw.Draw(image)

        (width, height) = image.size

        #set up message
        message = "some number" # FIX TO BE NUM_KEY
        font = ImageFont.truetype("arial.ttf", size = width//30+50)
        w, h = draw.textsize(message, font=font)
        (x, y) = ((width-w)//2, (height-h)//10)
        color = "rgb(255, 0, 255)"  # I HOPE HOT PINK STANDS OUT ENOUGH

        draw.text((x, y), message, fill=color, font=font)
        
        image.save(picture)

    count += 1  # REMOVE
