from PIL import Image, ImageDraw, ImageColor
import random


########################################################################################################################
# MATH
# returns a random item from the given list
def get_random_item_from(given_list):
    return given_list[random.randrange(0, len(given_list))]


# returns a function that, when called, returns a random element from the given list
def get_random_generator(given_list):
    return lambda: given_list[random.randrange(0, len(given_list))]


# generates a list of the given size, populating it with elements returned by the given generator
def generate_list(generator, size):
    generated_list = []
    while size >= 0:
        generated_list.append(generator())
        size -= 1
    return generated_list


# populates and returns a list of the given size using the given generator where each element is guaranteed to be unique
# if this loops forever/too long, the given generator cannot/cannot efficiently generate enough unique elements
def generate_unique_list(generator, size):
    unique_list = []
    while size >= 0:
        element = generator()
        if element not in unique_list:
            unique_list.append(element)
            size -= 1
    return unique_list


# returns a list of elements of the given size, where for each element:
#   (1) the element was returned by the given generator
#   (2) the element agrees with the given condition
# if the function loops forever/too long, the given condition is too strict for the given generator
def generate_list_conditionally(generator, size, condition):
    generated_list = []
    while size >= 0:
        new_element = generator()
        if condition(new_element):
            generated_list.append(new_element)
            size -= 1
    return generated_list


# unpacks each element of a list, enumerates it, then repacks it; useful for enumerating nested lists
def unpack_and_enumerate(given_list):
    new_list = []
    for index, item in enumerate(given_list):
        new_list.append([index, *item])
    return new_list


# converts an integer to a new base; returns a list from most significant digit to least
# if the given integer is negative, the first element in the list will be a minus sign
def get_new_base(integer, new_base):
    if new_base >= 2:
        new_base_integer = []  # start empty
        if integer < 0:  # check sign
            new_base_integer.append("-")
            integer *= -1
        insertion_point = len(new_base_integer)  # insert digits at 1 if we have a negative sign, 0 if we don't
        while integer >= new_base:  # iterate to get all digits except for the least significant
            new_base_integer.insert(insertion_point, integer % new_base)
            integer //= new_base
        new_base_integer.insert(insertion_point, integer)  # get the least significant digit
    else:
        new_base_integer = "Error: Bases must be >= 2, but you entered {}".format(new_base)
    return new_base_integer


########################################################################################################################
# ALPHABET
# returns the english alphabet as a string (all caps)
def get_english_alphabet():
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# converts an integer to a string based on the given alphabet
def int_to_alpha(integer, alphabet):
    alpha = ""
    character_mapping = get_new_base(integer, len(alphabet))
    for index in character_mapping:
        alpha += alphabet[index]
    return alpha


# enumerates the given list using the given alphabet instead of integers
def alphanumerate(list_arg, alphabet):
    new_list = []
    for index, item in enumerate(list_arg):
        alpha_index = int_to_alpha(index, alphabet)
        new_list.append([alpha_index, item])
    return new_list


########################################################################################################################
# COLORS
# returns the list of colors used for shape generation
def get_colors():
    return ["black", "royalblue", "brown", "cyan", "gray", "red", "purple", "pink", "gold", "orange", "teal", "green",
            "darkcyan"]


# returns a random color from the list of all colors
def get_random_color():
    return get_random_item_from(get_colors())


# returns the name of a color for pretty printing if one exists; otherwise, returns the given color name
def get_color_for_pretty_printing(color):
    try:
        return {"royalblue": "royal blue", "darkcyan": "dark cyan"}[color]
    except KeyError:
        return color


########################################################################################################################
# SHAPES
# returns the list of shapes used for question generation
def get_shapes():
    return ["circle", "square", "triangle", "ellipse", "pentagon"]


# returns a random shape from the list of all shapes
def get_random_shape():
    return get_random_item_from(get_shapes())


########################################################################################################################
# SEQUENCES
# returns a randomly generated color-shape pair
def generate_sequence_item():
    return [get_random_color(), get_random_shape()]


# returns a randomly-generated list of sequence items of the form (index, color, shape)
def generate_sequence(length):
    return unpack_and_enumerate(generate_list(generate_sequence_item, length))


# returns a sequence as defined above, but with unique elements
def generate_unique_sequence(sequence_length):
    return unpack_and_enumerate(generate_unique_list(generate_sequence_item, sequence_length))


# generates a child sequence of the given length by randomly selecting elements from the parent sequence
def generate_child_sequence(parent_sequence, sequence_length):
    return generate_list(get_random_generator(parent_sequence), sequence_length)


# generates a transformed sequence by mapping the enumerative indexes of the parent sequence
#   to the true indexes of the key sequence
def generate_transformed_sequence(parent_sequence, key_sequence):
    transformed_sequence = []
    for item in parent_sequence:
        enumerative_index = item[0]
        transformed_element = key_sequence[enumerative_index]
        transformed_sequence.append(transformed_element)
    return transformed_sequence


# converts a sequence element to a string; looks like "<color> <shape>"
def sequence_item_to_string(sequence_element):
    color_string = get_color_for_pretty_printing(sequence_element[1])
    shape_string = sequence_element[2]
    return "{} {}".format(color_string, shape_string)


# converts a sequence to a string; looks like "<color 0> <shape 0>, <color 1> <shape 1>, ..."
def sequence_to_string(sequence):
    sequence_as_string = ""
    for item in sequence:
        sequence_as_string += "{}, ".format(sequence_item_to_string(item))
    return sequence_as_string[:sequence_as_string.rindex(",")]


###############################################################################################################
# JSON
# returns the text passage as a string
def get_text_passage(text_passage_sequence):
    return "Consider the following sequence: {}".format(sequence_to_string(text_passage_sequence))


# returns the question as a string
def get_question():
    return "Based on the given diagram, what would the new sequence be?"


# generates a list of incorrect answer choice sequences
def generate_incorrect_answer_sequences(output_sequence, answer_sequence, amount):
    def generator():
        return generate_child_sequence(output_sequence, len(answer_sequence))

    def condition(new_sequence):
        return new_sequence != answer_sequence
    return generate_list_conditionally(generator, amount, condition)


# generates a list of the given length containing shuffled answer strings, where only one is correct
def generate_answer_strings(output_sequence, answer_sequence, length):
    answer_strings = [sequence_to_string(answer_sequence)]
    incorrect_answer_sequences = generate_incorrect_answer_sequences(output_sequence, answer_sequence, length)
    for item in incorrect_answer_sequences:
        answer_strings.append(sequence_to_string(item))
    random.shuffle(answer_strings)
    return answer_strings


# converts a pair list to bullets
def pair_list_to_bullets(pair_list):
    bullets = ""
    for pair in pair_list:
        bullets += "({}) {} ".format(pair[0], pair[1])
    bullets = bullets.strip()
    return bullets


# returns the answer choices as a string
def get_answer_choices(output_sequence, answer_sequence, length):
    answer_strings = generate_answer_strings(output_sequence, answer_sequence, length)
    return pair_list_to_bullets(alphanumerate(answer_strings, get_english_alphabet()))


# returns the answer as a string
def get_answer(answer_sequence):
    return sequence_to_string(answer_sequence)


# returns a link to the image in the local directory as a string
def get_image_link(filename):
    return filename + ".jpg"


# converts a key value pair to json
def pair_to_json(pair):
    return "\"{}\": \"{}\"".format(pair[0], pair[1])


# converts a list of key value pairs to json
def pair_list_to_json(pair_list):
    json = "{\n"
    for pair in pair_list:
        json += "\t{},\n".format(pair_to_json(pair))
    json = json[:json.rindex(",")] + "\n}"
    return json


# converts a dict to json
def dict_to_json(given_dict):
    return pair_list_to_json(list(given_dict.items()))


########################################################################################################################
# DRAW
# draw functions take (x, y) as the upper left-hand corner
def draw_line(draw, x, y, length, fill="black", width=5):
    draw.line((x, y, x + length, y), fill=fill, width=width)


def draw_arrowhead(draw, x, y, width, height, fill="black"):
    draw.polygon([(x, y + height), (x, y), (x + width, y + height/2)], fill=fill)


def draw_arrow(draw, x, y, length, arrowhead_width=20, arrowhead_height=20):
    draw_line(draw, x, y + arrowhead_height/2, length - arrowhead_width)
    draw_arrowhead(draw, x + length - arrowhead_width, y, arrowhead_width, arrowhead_height)


def draw_arrows(draw, amount, x, y, length, y_spacing):
    y_current = y
    while amount > 0:
        draw_arrow(draw, x, y_current, length)
        y_current += y_spacing
        amount -= 1


def draw_circle(draw, color, x, y, width, height):
    draw.ellipse((x, y, x + width, y + height), fill=color)


def draw_square(draw, color, x, y, width, height):
    draw.rectangle((x, y, x + width, y + height), fill=color)


def draw_ellipse(draw, color, x, y, width, height):
    draw.ellipse((x + width/4, y, x + width/4 + width/2, y + height), fill=color)


def draw_triangle(draw, color, x, y, width, height):
    draw.polygon([(x, y + height), (x + width, y + height), (x + width/2, y)], fill=color)


def draw_pentagon(draw, color, x, y, width, height):
    draw.polygon([(x, y + height/2), (x + width/2, y), (x + width, y + height/2), (x + width, y + height),
                  (x, y + height)], fill=color)


# maps the shape name to the appropriate draw function
def draw_shape(draw, sequence_item, x, y, width, height):
    shape_dictionary = {"circle": draw_circle, "square": draw_square, "ellipse": draw_ellipse,
                        "triangle": draw_triangle, "pentagon": draw_pentagon}
    shape_color = sequence_item[1]
    shape_name = sequence_item[2]
    shape_dictionary[shape_name](draw, shape_color, x, y, width, height)


def draw_shapes(draw, sequence, x, y_spacing, width, height):
    for sequence_item in sequence:
        draw_shape(draw, sequence_item, x, sequence_item[0] * y_spacing, width, height)


def draw_all(draw, input_sequence, output_sequence, shape_width, shape_height, x_spacing, y_spacing, x=0, y=0):
    draw_arrows(draw, len(input_sequence), x + shape_width, y + shape_height / 2 - 10, x_spacing - shape_width,
                y_spacing)
    draw_shapes(draw, input_sequence, x, y_spacing, shape_width, shape_height)
    draw_shapes(draw, output_sequence, x + x_spacing, y_spacing, shape_width, shape_height)


# determine canvas size, make an image, draw everything, and return the image
def draw_image(input_sequence, output_sequence, has_rotation, shape_width=100, shape_height=100, x_spacing=225,
               y_spacing=125):
    shape_amount = len(input_sequence)  # determine canvas width
    canvas_width = 2 * shape_width + (x_spacing - shape_width)
    canvas_height = (shape_amount * shape_height) + ((shape_amount - 1) * (y_spacing - shape_height))

    image = Image.new("RGB", (canvas_width, canvas_height), ImageColor.getrgb("white"))  # draw image
    draw = ImageDraw.Draw(image)
    draw_all(draw, input_sequence, output_sequence, shape_width, shape_height, x_spacing, y_spacing)

    if has_rotation:  # rotate image if desired
        degrees = random.randint(0, 359)
        image = image.rotate(degrees, expand=True, fillcolor="white")
    return image


########################################################################################################################
# MAIN
# terms:
#   length: the number of problems to generate
#   sequence item: a 3-tuple of the form (index, color, shape)
#   input sequence: a list of sequence items describing objects on the left side of the image
#   output sequence: a list of sequence items describing objects on the right side of the image
#   text passage sequence: a list of sequence items describing objects in the text passage entry of the json file
#   answer sequence: a list of sequence items describing objects in the answer entry of the json file; the correct
#                    answer to the generated problem
#   io_sequences: the input and output sequences; these must be the same length for a given problem
#   ta_sequences: the text passage and answer sequences; these must be the same length for a given problem
#   answer choice length: the number of answer choices to be generated for a problem
def main(length, min_io_sequence_length=2, max_io_sequence_length=5, min_ta_sequence_length=3, max_ta_sequence_length=7,
         min_answer_choice_length=4, max_answer_choice_length=4, has_rotation=False):
    # one iteration produces one question; each question has an image component (jpg), and a text component (json)
    for index in range(0, length):
        # determine sequence lengths
        io_sequence_length = random.randint(min_io_sequence_length, max_io_sequence_length)
        ta_sequence_length = random.randint(min_ta_sequence_length, max_ta_sequence_length)
        answer_choice_length = random.randint(min_answer_choice_length, max_answer_choice_length)

        # generate sequences
        input_sequence = generate_unique_sequence(io_sequence_length)
        output_sequence = generate_sequence(io_sequence_length)
        text_passage_sequence = generate_child_sequence(input_sequence, ta_sequence_length)
        answer_sequence = generate_transformed_sequence(text_passage_sequence, output_sequence)

        # draw & save image
        filename = "Pattern_Matching_{}".format(index)
        image = draw_image(input_sequence, output_sequence, has_rotation)
        image.save(filename + ".jpg")

        # write json
        text_passage = get_text_passage(text_passage_sequence)
        question = get_question()
        answer_choices = get_answer_choices(output_sequence, answer_sequence, answer_choice_length)
        answer = get_answer(answer_sequence)
        image_link = get_image_link(filename)
        problem_info_dict = {"text_passage": text_passage, "question": question, "answer_choices": answer_choices,
                             "answer": answer, "image_link": image_link}
        json = dict_to_json(problem_info_dict)
        with open(filename + ".json", "w") as file:
            file.write(json)


########################################################################################################################
if __name__ == "__main__":
    main(500, has_rotation=True)
