import json
from google_images_search import GoogleImagesSearch
from PIL import Image, ImageDraw, ImageFont
import os
def gather_image(template_file):
    GCS_DEVELOPER_KEY = "AIzaSyBhT5S6xOtfiVj2q0B-hXrLJ8ToKs1ZtPA"
    GCS_CX = "b29678caa4b0cc505"

    gis = GoogleImagesSearch(GCS_DEVELOPER_KEY, GCS_CX)


    f = open(template_file)
    data = json.load(f)

    nouns = []

    for d in data:
        nouns = nouns + d["nouns"]

    print(nouns)
    nouns = list(set(nouns))

    print(nouns)


    for i, noun in enumerate(nouns):
        search_params = {
                'q': noun,
                'num': 1,
                'safe': 'high',
                'fileType': 'png',
            }
        for root, dir, files in os.walk(os.getcwd()+"\\img"):
            filename = noun + ".jpg"
            if filename not in files:
                gis.search(search_params=search_params, 
                    path_to_dir= "./img/".format(i), 
                    custom_image_name = noun.format(noun))

        # picture = "./img/{:04d}/".format(i) + '{:02d}'.format(n) + ".png"

        # #open image as a background
        # with Image.open('{:02d}'.format(n) + ".png") as image:
        #     draw = ImageDraw.Draw(image)

        #     #set up message
        #     font = ImageFont.truetype("Roboto-Bold.ttf", size = 30)
        #     (x, y) = (50, 50)
        #     message = "some number"
        #     color = "rgb(0, 0, 0)"

        #     draw.text((x, y), message, fill=color, font=font)
            
        #     image.save(picture)

    f.close()