import os
import time
import json
import pytesseract
import cv2
import argparse
from pytesseract import Output

#checks if [NUM_KEY] is within the bounds specified
def test1(template_data, generated_data) -> bool:
    isGood = True

    for gen in generated_data:
        temp = {}
        for template in template_data:
            if(gen["question"][0:5] == template["question"][0:5]):
                temp = template
                break
        lwr = template["nums_bounds"][0]
        upr = template["nums_bounds"][1]

        if(gen["keys"]["[NUM_KEY]"] < lwr or gen["keys"]["[NUM_KEY]"] > upr):
            isGood = False

    return isGood
    

#checks if images are generated with text on them
def test2(template_data, generated_data) -> bool:
    isGood = True

    for gen in generated_data:
        ans = gen["answers"]

        image = cv2.imread(gen["image"])
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pytesseract.image_to_data(rgb, output_type=Output.DICT)

        for i in range(0, len(results["text"])):
            x = results["left"][i]
            y = results["top"][i]
            w = results["width"][i]
            h = results["height"][i]

            text = results["text"][i]
            conf = int(results["conf"][i])

        if conf > args["min_conf"]:
            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()

        if(text != ans):
            isGood = False

    return isGood

#checks if the correct answer is correct according to the equation used
def test3(template_data, generated_data) -> bool:
    isGood = True

    for gen in generated_data:
        formula = gen["formula"]
        for key, val in zip(gen["keys"].keys, gen["keys"].values):
            formula.replace(key, val)

        ans = eval(formula)

        if(ans != gen["answers"]):
            isGood = False

    return isGood

#checks that the answer choices are random
def test4(template_data, generated_data) -> bool:
    isGood = True

    for gen in generated_data:
        temp = gen["options"]
        temp = list(set(temp))
        if(len(temp) != 5):
            isGood = False

    return isGood

#checks that the main noun in the question matches the image in output.json
def test5(template_data, generated_data) -> bool:
    isGood = True

    for gen in generated_data:
        if(gen["noun"] + ".jpg" != gen["name"]):
            isGood = False

    return isGood

if __name__ == "__main__":
    command = "python main.py 1"
    os.system(command)

    #gets all the data
    with open("templates_joshua.json") as f:
        template_data = json.load(f)

    with open("generated.json") as f:
        generated_data = json.load(f)
    
    #runs all the tests
    if(test1(template_data, generated_data)):
        print("Test 1 passed.")
    else:
        print("Failure occured in Test 1.")
        
    if(test2(template_data, generated_data)):
        print("Test 2 passed.")
    else:
        print("Failure occured in Test 2.")

    if(test3(template_data, generated_data)):
        print("Test 3 passed.")
    else:
        print("Failure occured in Test 3.")
        
    if(test4(template_data, generated_data)):
        print("Test 4 passed.")
    else:
        print("Failure occured in Test 4.")
        
    if(test5(template_data, generated_data)):
        print("Test 5 passed.")
    else:
        print("Failure occured in Test 5.")
    
    #lets the program sleep so it gives it time to finish all the functions and image saving
    time.sleep(60)

    #removes all the unneeded data
    os.remove("generated.json")
    os.rmdir("output")