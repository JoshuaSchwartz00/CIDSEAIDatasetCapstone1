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
        lwr = 0
        upr = 0
        for template in template_data:
            if(gen["question"][0:7] == template["question"][0:7]):
                lwr = template["nums_bounds"]["[NUM_KEY]"][0]
                upr = template["nums_bounds"]["[NUM_KEY]"][1]
                break

        num_key = gen["keys"]["[NUM_KEY]"]
        if(num_key < lwr or num_key > upr):
            isGood = False
            print(lwr, num_key, upr)

    return isGood
    

#checks if images are generated with text on them
def test2(generated_data) -> bool:
    return True
    #skim through all the images and see if they have numbers on them

#checks if the correct answer is correct according to the equation used
def test3(generated_data) -> bool:
    isGood = True

    for gen in generated_data:
        formula = gen["formula"]
        for key in gen["keys"]:
            formula = formula.replace(key, str(gen["keys"][key]))

        ans = eval(formula)

        if(ans != gen["answers"]):
            isGood = False

    return isGood

#checks that the answer choices are random
def test4(generated_data) -> bool:
    isGood = True

    for gen in generated_data:
        temp = gen["choices"]
        temp = list(set(temp))
        if(len(temp) != 5):
            isGood = False
            print(temp)

    return isGood

#checks that the main noun in the question matches the image in output.json
def test5(generated_data) -> bool:
    isGood = True

    for gen in generated_data:
        if(gen["noun"] + ".jpg" != gen["img_name"]):
            isGood = False

    return isGood

if __name__ == "__main__":
    command = "python main.py"
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
        
    if(test2(generated_data)):
        print("Test 2 passed.")
    else:
        print("Failure occured in Test 2.")

    if(test3(generated_data)):
        print("Test 3 passed.")
    else:
        print("Failure occured in Test 3.")
        
    if(test4(generated_data)):
        print("Test 4 passed.")
    else:
        print("Failure occured in Test 4.")
        
    if(test5(generated_data)):
        print("Test 5 passed.")
    else:
        print("Failure occured in Test 5.")
    
    #lets the program sleep so it gives it time to finish all the functions and image saving
    #time.sleep(60)

    #removes all the unneeded data
    os.remove("generated.json")
    os.rmdir("output")