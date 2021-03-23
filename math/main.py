from imagegather import gather_image
from mathcreatedata import generate_questions
import os
import json
import sys

if __name__ == "__main__":
    testMode = False
    if(len(sys.argv) > 2):
        if(sys.argv[2] == 1):
            testMode = True
    gather_image("templates_joshua.json")
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
        questions = generate_questions(template, testMode)
        output_questions = output_questions + questions
    print(len(output_questions))

    

    with open("generated.json", "w") as f:
        f.write(json.dumps(output_questions, indent=4))