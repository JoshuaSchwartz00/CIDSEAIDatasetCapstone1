#imports

import json
import spacy
from spacy.symbols import NOUN, NUM
from spacy.matcher import Matcher
import re
from google_images_search import GoogleImagesSearch
from PIL import Image, ImageDraw, ImageFont

#initializations

nlp = spacy.load('en_core_web_sm')

GCS_DEVELOPER_KEY = "AIzaSyBhT5S6xOtfiVj2q0B-hXrLJ8ToKs1ZtPA"
GCS_CX = "b29678caa4b0cc505"

gis = GoogleImagesSearch(GCS_DEVELOPER_KEY, GCS_CX)

stopwords = [##################################

]

#pull questions from json file

data = []

with open('train.json', 'r') as f:
    lines = f.readlines()
    data = list(map(lambda x: json.loads(x), lines))
    f.close()

#clean questions
for x in data:
    x['cleaned_question'] = x["question"].split('\n')[0].strip()
#filter math prob with 2 sentences
data = list(filter(lambda x: len(re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", x["cleaned_question"])) >= 2, data))



data = data[:1]

data_formatted = []

pattern = re.compile('^..+')

for i, data_ob in enumerate(data):
    real_question = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", data_ob["cleaned_question"])[-1]
    raw_passage = data_ob["question"].replace(real_question, "").strip()
    print(real_question)
    print(raw_passage)

    q_doc = nlp(raw_passage)
    nouns = []
    numbers = []
    for token in q_doc :
        if token.pos == NOUN and pattern.match(token.text) != None:
            nouns.append(token.text)
        elif token.pos == NUM:
            numbers.append(token.text)
    data_ob["nouns"] = nouns

    print(nouns)
    print(numbers)

    for n, noun in enumerate(nouns):

        #replace nouns in question with numbers
        data_ob["question"] = data_ob["question"].replace(noun, '[{:02d}]'.format(n), 1)

        #searches google and saves enumerated images to an enumerated folder
        search_params = {
            'q': noun,
            'num': 1,
            'safe': 'high',
            'fileType': 'png',
        }
        gis.search(search_params=search_params, 
            path_to_dir= "./img/{:04d}/".format(i), 
            custom_image_name = '{:02d}'.format(n))

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

    new_data = {}

    last_segment = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", data_ob["cleaned_question"])[-1]
    question_ind = data_ob["question"].find(last_segment)

    print(last_segment)
    print(question_ind)
    #creating a dictionary for each problem and appending it to data_formatted
    new_data["P"] = data_ob["question"][:question_ind]
    new_data["Q"] = data_ob["question"][question_ind:]
    new_data["A"] = data_ob["options"]
    new_data["I"] = "{:04d}".format(i)

    for n, noun in enumerate(nouns):
        data_formatted.append(new_data)

        picture = "./img/{:04d}/".format(i) + '{:02d}'.format(n) + ".jpg"

        with Image.open(picture) as image:
                    draw = ImageDraw.Draw(image)

                    #set up message
                    font = ImageFont.truetype("arial.ttf", size = 30)
                    (x, y) = (50, 50)
                    message = "some number"
                    color = "rgb(0, 0, 0)"

                    draw.text((x, y), message, fill=color, font=font)
                    
                    image.save(picture)

    data_formatted.append(new_data)


with open('train.save.json', 'w') as f:
    f.write(json.dumps(data_formatted, indent=4))
    f.close()






#Figure out a way to enumerate these pictures


#replace nouns in questions with numbers


#create a mock dataset of 10 items; refinement and scalability aren't important right now
#that is, make the dataset the same format as the VLQA stuff
