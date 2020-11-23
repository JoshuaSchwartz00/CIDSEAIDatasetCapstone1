import json
import re
import random

NUM_REGEX_STRING = r"(\[NUM_(?:KEY|\d+)\])"



def generate_questions(template):
    question_base = template["question"]
    formula_base = template["formula"]
    m = re.findall(NUM_REGEX_STRING, question_base)

    generated_questions = list()
    for noun in template["nouns"]:
        question_replaced = question_base.replace("[NOUN]", noun) 

        
        formula_replaced = formula_base
        #iterate through the num replacements
        for idx, n in enumerate(m):
            lwr = template["nums_bounds"][n]["lower"]
            upr = template["nums_bounds"][n]["upper"]

            rand_num = random.randint(lwr, upr)
            question_replaced = question_replaced.replace(n, str(rand_num))
            formula_replaced = formula_replaced.replace(n, str(rand_num))

        answer = eval(formula_replaced)

        list_choices = [answer]
        for i in range(template["options_num"] - 1):
            list_choices.append(answer + random.randint(-100,100))
        
        random.shuffle(list_choices)

        generated_questions.append({
            "L": template["passage"],
            "Q": question_replaced,
            "C": list_choices,
            "A": answer
        })
    return generated_questions


if __name__ == "__main__":

    templates = None
    with open("templates.json", "r") as f:
        templates = json.load(f)
        f.close()

    print(templates)
    for template in templates:
        questions = generate_questions(template)

        with open("generated.json", "w") as f:
            f.write(json.dumps(questions, indent=4))