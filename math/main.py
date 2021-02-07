from imagegather import gather_image
from mathcreatedata import generate_questions

if __name__ == "__main__":
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
        questions = generate_questions(template)
        output_questions = output_questions + questions
    print(len(output_questions))

    

    with open("generated.json", "w") as f:
        f.write(json.dumps(output_questions, indent=4))