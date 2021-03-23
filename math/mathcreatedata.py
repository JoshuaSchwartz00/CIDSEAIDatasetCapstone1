import json
import re
import random
from PIL import Image, ImageDraw, ImageFont
import os
import glob
#NUM_REGEX_STRING = r"(\[NUM_(?:KEY|\d+)\])"

COUNT = 0

def generate_questions(template, testMode = False):
    global COUNT
    question_base = template["question"]
    formula_base = template["formula"]
    passage_base = template["passage"]
    #m = re.findall(NUM_REGEX_STRING, question_base)

    generated_questions = list()

    
    for noun in template["nouns"]:
        for i in range(0,4):
            COUNT = COUNT + 1
            question_replaced = question_base.replace("[NOUN]", noun) 
            passage_replaced = passage_base.replace("[NOUN]", noun)

            formula_replaced = formula_base

            keys = {}
            name = ""
            #iterate through the num replacements
            #for idx, n in enumerate(m):
            for key in template["nums_bounds"]:
                lwr = int(template["nums_bounds"][key][0])
                upr = int(template["nums_bounds"][key][1])

                rand_num = random.randint(lwr, upr)
                question_replaced = question_replaced.replace(key, str(rand_num))
                formula_replaced = formula_replaced.replace(key, str(rand_num))
                passage_replaced = passage_replaced.replace(key, str(rand_num))

                keys[key] = rand_num

                if key == "[NUM_KEY]":
                    name = annotate_img(noun, rand_num, COUNT)

            answer = eval(formula_replaced)


            list_choices = [answer]
            for i in range(template["options_num"] - 1):
                list_choices.append(answer + random.randint(-100,100))
            
            random.shuffle(list_choices)

            if(testMode):
                generated_questions.append({
                    "passage": passage_replaced,
                    "question": question_replaced,
                    "choices": list_choices,
                    "answers": answer,
                    "keys": keys,
                    "noun": noun,
                    "formula": formula_base,
                    "img_name": name,
                    "image": "/output/{:03d}".format(COUNT) + ".png"
                })
            else:
                generated_questions.append({
                    "passage": passage_replaced,
                    "question": question_replaced,
                    "choices": list_choices,
                    "answers": answer,
                    "image": "/output/{:03d}".format(COUNT) + ".png"
                })

    return generated_questions

def annotate_img(name, value, question_num):
    path = os.getcwd() + "/img"
    files = os.listdir(path)
        
    picture = os.getcwd() + "/output/{:03d}".format(question_num) + ".png"
    with Image.open("img/" + name + ".jpg") as image:
        draw = ImageDraw.Draw(image)

        (width, height) = image.size

        #set up message
        message = str(value) # FIX TO BE NUM_KEY
        font = ImageFont.truetype(os.getcwd() + "/Roboto-Regular.ttf", size = width//30+50)
        w, h = draw.textsize(message, font=font)
        (x, y) = ((width-w)//2, (height-h)//10)
        color = "rgb(255, 0, 255)"  # I HOPE HOT PINK STANDS OUT ENOUGH

        draw.text((x, y), message, fill=color, font=font)
        
        image.save(picture)

    return name + ".jpg"


if __name__ == "__main__":
    if not os.path.exists('output'):
        os.makedirs('output')
    COUNT = 0
    templates = None


    with open("templates_joshua.json", "r") as f:
        templates = json.load(f)
        f.close()

    print(len(templates))
    output_questions = []
    for template in templates:
        questions = generate_questions(template)
        output_questions = output_questions + questions
    print(len(output_questions))

    

    with open("generated.json", "w") as f:
        f.write(json.dumps(output_questions, indent=4))