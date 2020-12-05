#imports

import json
from google_images_search import GoogleImagesSearch
from PIL import Image, ImageDraw, ImageFont
import random
import compiler

#initializations
GCS_DEVELOPER_KEY = "AIzaSyBhT5S6xOtfiVj2q0B-hXrLJ8ToKs1ZtPA"
GCS_CX = "b29678caa4b0cc505"

gis = GoogleImagesSearch(GCS_DEVELOPER_KEY, GCS_CX)

answers = ["A", "B", "C", "D", "E"]

#getting data

data = []

with open('templates_joshua.json', 'r') as f:
    lines = f.readlines()
    data = list(map(lambda x: json.loads(x), lines))
    f.close()

#script
new_data = []

for row in data:
    #replace [NOUN] with random noun
    #replace [NUM] with random num within lower_bound <= x <= upper_bound
    #create new sentence and give it an index
    rand_noun = row["nouns"][random.randrange(0, len(row["nouns"]))]
    rand_num = random.randint(row["lower bound"], row["upper bound"])

    new_question = row["question"].replace("[NOUN]", rand_noun).replace("[NUM]", rand_num)




    #search for image and append num to image




    # for n, noun in enumerate(nouns):

    #     #replace nouns in question with numbers
    #     data_ob["question"] = data_ob["question"].replace(noun, '[NOUN]', 1)

        #searches google and saves enumerated images to an enumerated folder
        # search_params = {
        #     'q': noun,
        #     'num': 1,
        #     'safe': 'high',
        #     'fileType': 'png',
        # }
        # gis.search(search_params=search_params, 
        #     path_to_dir= "./img/{:04d}/".format(i), 
        #     custom_image_name = '{:02d}'.format(n))

    # for n, noun in enumerate(nouns):
    #     data_formatted.append(new_data)

    #     picture = "./img/{:04d}/".format(i) + '{:02d}'.format(n) + ".jpg"

    #     with Image.open(picture) as image:
    #                 draw = ImageDraw.Draw(image)

    #                 #set up message
    #                 font = ImageFont.truetype("arial.ttf", size = 30)
    #                 (x, y) = (50, 50)
    #                 message = "some number"
    #                 color = "rgb(0, 0, 0)"

    #                 draw.text((x, y), message, fill=color, font=font)
                    
    #                 image.save(picture)

    #create a correct answer and assign to A, B, C, D, E
    new_answers = [None, None, None, None, None]
    correct_formula = row["formula"].replace["[NUM]", rand_num]
    correct_answer = compiler.parse(correct_formula)

    rand_correct = random.randint(0, 5)
    new_answers[rand_correct] = correct_answer


    #all other answers should be wrong, but within formula(lower_bound <= wrong_answer < x < wrong_answer <= upper_bound)
    i = 0
    while i <= len(new_answers):
        wrong_num = random.randint(row["lower bound"], row["upper bound"])
        if wrong_num == rand_num:
            pass
        elif new_answers[i] is not None:
            i += 1
        elif wrong_num != rand_num and new_answers[i] is None:
            wrong_formula = row["formula"].replace("[NUM]", wrong_num)
            wrong_answer = compiler.parse(wrong_formula)
            new_answers[i] = wrong_answer

            i += 1
        else:
            print(new_answers)
            break

    #format things
    ans = ["A", "B", "C", "D", "E"]
    new_options = []
    for a, num in zip(ans, new_answers):
        new_options.append(ans + ")" + num)


    #put new data in new_data

    new_temp = {}
    new_temp["question"] = new_question
    new_temp["options"] = new_options
    new_temp["correct"] = ans[rand_correct]

    new_data.push(new_temp)

#save to json

with open('dataset.json', 'w') as f:
    f.write(json.dumps(new_data, indent=4))
    f.close()