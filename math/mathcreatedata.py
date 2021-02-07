import json
import re
import random

#NUM_REGEX_STRING = r"(\[NUM_(?:KEY|\d+)\])"



def generate_questions(template):
    question_base = template["question"]
    formula_base = template["formula"]
    passage_base = template["passage"]
    #m = re.findall(NUM_REGEX_STRING, question_base)

    generated_questions = list()
    for noun in template["nouns"]:
        for i in range(0,4):
            question_replaced = question_base.replace("[NOUN]", noun) 
            passage_replaced = passage_base.replace("[NOUN]", noun)

            formula_replaced = formula_base
            #iterate through the num replacements
            #for idx, n in enumerate(m):
            for key in template["nums_bounds"]:
                lwr = int(template["nums_bounds"][key][0])
                upr = int(template["nums_bounds"][key][1])

                rand_num = random.randint(lwr, upr)
                question_replaced = question_replaced.replace(key, str(rand_num))
                formula_replaced = formula_replaced.replace(key, str(rand_num))
                passage_replaced = passage_replaced.replace(key, str(rand_num))


            answer = eval(formula_replaced)

            list_choices = [answer]
            for i in range(template["options_num"] - 1):
                list_choices.append(answer + random.randint(-100,100))
            
            random.shuffle(list_choices)

            generated_questions.append({
                "passage": passage_replaced,
                "question": question_replaced,
                "choices": list_choices,
                "answers": answer,
                "image": noun + ".jpg"
            })
    return generated_questions


if __name__ == "__main__":

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