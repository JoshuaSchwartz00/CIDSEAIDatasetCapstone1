from PIL import Image, ImageDraw, ImageColor
import random
import string
import os


########################################################################################################################
# MATH
# returns a random item from the given list
# returns a function that, when called, returns a random element from the given list
def get_random_generator(given_list):
    return lambda: given_list[random.randrange(0, len(given_list))]


# generates a list of the given size, populating it with elements returned by the given generator
def generate_list(generator, size):
    generated_list = []
    while size > 0:
        generated_list.append(generator())
        size -= 1
    return generated_list


# populates and returns a list of the given size using the given generator where each element is guaranteed to be unique
# if this loops forever/too long, the given generator cannot/cannot efficiently generate enough unique elements
def generate_unique_list(generator, size):
    unique_list = []
    while size > 0:
        element = generator()
        if element not in unique_list:
            unique_list.append(element)
            size -= 1
    return unique_list


# returns a list of elements of the given size, where for each element:
#   (1) the element was returned by the given generator
#   (2) the element agrees with the given condition
# if the function loops forever/too long, the given condition is too strict for the given generator
def generate_list_conditionally(generator, condition, size):
    generated_list = []
    while size > 0:
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


########################################################################################################################
# ALPHABET
def alphanumerate(list_arg):
    new_list = []
    for index, item in enumerate(list_arg):
        new_list.append([string.ascii_uppercase[index], item])
    return new_list


# returns the list of colors used for shape generation
def get_colors():
    return ["black", "royalblue", "brown", "cyan", "gray", "red", "purple", "pink", "gold", "orange", "teal", "green",
            "darkcyan"]


# returns the name of a color for pretty printing if one exists; otherwise, returns the given color name
def get_color_for_pretty_printing(color):
    try:
        return {"royalblue": "royal blue", "darkcyan": "dark cyan"}[color]
    except KeyError:
        return color


# returns the list of shapes used for question generation
def get_shapes():
    return ["circle", "square", "triangle", "ellipse", "pentagon"]


# returns a randomly generated color-shape pair
def generate_sequence_item():
    return [random.choice(get_colors()), random.choice(get_shapes())]


# returns a randomly-generated list of sequence items of the form (index, color, shape)
def generate_sequence(length):
    return unpack_and_enumerate(generate_list(generate_sequence_item, length))


# returns a sequence as defined above, but with unique elements
def generate_unique_sequence(sequence_length):
    return unpack_and_enumerate(generate_unique_list(generate_sequence_item, sequence_length))


def generate_child_sequence(parent_sequence, length):
    return generate_list(get_random_generator(parent_sequence), length)


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


def generate_incorrect_answer_sequences(output_sequence, correct_answer_sequence, amount=3):
    def generator():
        return generate_child_sequence(output_sequence, len(correct_answer_sequence))

    def condition(incorrect_answer_sequence):
        return incorrect_answer_sequence != correct_answer_sequence

    incorrect_answer_sequences = generate_list_conditionally(generator, condition, amount)
    return incorrect_answer_sequences


def generate_answer_strings(output_sequence, answer_sequence):
    answer_strings = [sequence_to_string(answer_sequence)]
    incorrect_answer_sequences = generate_incorrect_answer_sequences(output_sequence, answer_sequence)
    for item in incorrect_answer_sequences:
        answer_strings.append(sequence_to_string(item))
    random.shuffle(answer_strings)
    return answer_strings


def pair_list_to_bullets(pair_list):
    bullets = ""
    for pair in pair_list:
        bullets += "({}) {} ".format(*pair)
    bullets = bullets.strip()
    return bullets


def get_answer_choices(output_sequence, answer_sequence):
    answer_strings = generate_answer_strings(output_sequence, answer_sequence)
    return pair_list_to_bullets(alphanumerate(answer_strings))


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


class ImageHandler:
    directory = "pattern_matching_dataset"
    filename = "pattern{}.jpg"
    color_mode = "RGB"
    background_color = "white"
    has_rotation = False
    shape_width = 100
    shape_height = 100
    x_spacing = 225
    y_spacing = 125
    arrowhead_width = 20
    arrowhead_height = 20
    line_width = 5
    default_fill = "black"

    canvas_width = None
    arrow_y_start = None
    arrowhead_x = None
    line_length = None

    @staticmethod
    def orchestrate(input_list, output_list, image_index):
        image_handler = ImageHandler(input_list, output_list, image_index)
        image_handler.draw_all()
        if ImageHandler.has_rotation:
            image_handler.perform_random_rotation()
        image_handler.save_image()

    @staticmethod
    def derive_static_variables():
        ImageHandler.canvas_width = ImageHandler.derive_canvas_width()
        ImageHandler.arrow_y_start = ImageHandler.derive_arrow_y_start()
        ImageHandler.arrowhead_x = ImageHandler.derive_arrowhead_x()
        ImageHandler.line_length = ImageHandler.derive_line_length()

    @staticmethod
    def derive_canvas_width():
        return 2 * ImageHandler.shape_width + (ImageHandler.x_spacing - ImageHandler.shape_width)

    @staticmethod
    def derive_arrow_y_start():
        return ImageHandler.shape_height / 2 - 10

    @staticmethod
    def derive_arrowhead_x():
        return ImageHandler.x_spacing - ImageHandler.arrowhead_width

    @staticmethod
    def derive_line_length():
        return ImageHandler.arrowhead_x - ImageHandler.shape_width

    def __init__(self, input_list, output_list, image_index):
        self.input_list = input_list
        self.output_list = output_list
        self.image_index = image_index
        self.canvas_height = self.derive_canvas_height()
        self.image = self.derive_image()
        self.draw = self.derive_draw()

    def derive_canvas_height(self):
        shape_amount = len(self.input_list)
        return shape_amount * self.shape_height + ((shape_amount - 1) * (self.y_spacing - self.shape_height))

    def derive_image(self):
        image_color = ImageColor.getrgb(self.background_color)
        return Image.new(self.color_mode, (self.canvas_width, self.canvas_height), image_color)

    def derive_draw(self):
        return ImageDraw.Draw(self.image)

    def perform_random_rotation(self):
        degrees = random.randint(0, 359)
        self.image = self.image.rotate(degrees, fillcolor=self.background_color, expand=True)

    def draw_all(self):
        self.draw_arrows()
        self.draw_shapes(self.input_list, 0)
        self.draw_shapes(self.output_list, self.x_spacing)

    def save_image(self):
        filename = self.filename.format(self.image_index)
        path = "{}\\{}".format(self.directory, filename)
        self.image.save(path)

    def draw_shapes(self, model_triple_list, x):
        for model_triple in model_triple_list:
            model_index = model_triple[0]
            y = model_index * self.y_spacing
            self.draw_shape(model_triple, x, y)

    def draw_shape(self, model_triple, x, y):
        shape_dictionary = {"circle": self.draw_circle, "square": self.draw_square, "ellipse": self.draw_ellipse,
                            "triangle": self.draw_triangle, "pentagon": self.draw_pentagon}
        fill = model_triple[1]
        shape = model_triple[2]

        #   a bug with pycharm will flag this with "unexpected arguments" despite the fact that all possible resultant
        # functions (shown above) take the same three arguments in the same order

        # noinspection PyArgumentList
        shape_dictionary[shape](fill, x, y)

    def draw_circle(self, fill, x, y):
        x1 = x
        y1 = y

        x2 = x + self.shape_width
        y2 = y + self.shape_height

        self.draw.ellipse((x1, y1, x2, y2), fill=fill)

    def draw_square(self, fill, x, y):
        x1 = x
        y1 = y

        x2 = x + self.shape_width
        y2 = y + self.shape_height

        self.draw.rectangle((x1, y1, x2, y2), fill=fill)

    def draw_ellipse(self, fill, x, y):
        x1 = x + self.shape_width / 4
        y1 = y

        x2 = x + self.shape_width / 4 + self.shape_width / 2
        y2 = y + self.shape_height

        self.draw.ellipse((x1, y1, x2, y2), fill=fill)

    def draw_triangle(self, fill, x, y):
        x1 = x
        y1 = y + self.shape_height

        x2 = x + self.shape_width
        y2 = y1

        x3 = x + self.shape_width / 2
        y3 = y

        self.draw.polygon(((x1, y1), (x2, y2), (x3, y3)), fill=fill)

    def draw_pentagon(self, fill, x, y):
        x1 = x
        y1 = y + self.shape_height / 2

        x2 = x + self.shape_width / 2
        y2 = y

        x3 = x + self.shape_width
        y3 = y1

        x4 = x3
        y4 = y + self.shape_height

        x5 = x
        y5 = y4

        self.draw.polygon(((x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5)), fill=fill)

    def draw_arrows(self):
        arrow_count = len(self.input_list)
        y = self.arrow_y_start
        while arrow_count > 0:
            self.draw_arrow(y)
            y += self.y_spacing
            arrow_count -= 1

    def draw_arrow(self, y):
        line_y = y + self.arrowhead_height / 2
        arrowhead_y = y
        self.draw_line(line_y)
        self.draw_arrowhead(arrowhead_y)

    def draw_arrowhead(self, y):
        x = self.arrowhead_x
        width = self.arrowhead_width
        height = self.arrowhead_height
        fill = self.default_fill

        x1 = x
        y1 = y + height

        x2 = x
        y2 = y

        x3 = x + width
        y3 = y + height / 2

        self.draw.polygon(((x1, y1), (x2, y2), (x3, y3)), fill=fill)

    def draw_line(self, y):
        x = self.shape_width
        length = self.line_length
        width = self.line_width
        fill = self.default_fill

        x1 = x
        y1 = y

        x2 = x + length
        y2 = y

        self.draw.line((x1, y1, x2, y2), width=width, fill=fill)


ImageHandler.derive_static_variables()


########################################################################################################################
# MAIN
def main():
    question_count = 500
    io_list_len_range = range(3, 6)
    ta_list_len_range = range(3, 8)

    for index in range(0, question_count):
        io_sequence_length = random.choice(io_list_len_range)
        ta_sequence_length = random.choice(ta_list_len_range)

        input_list = generate_unique_sequence(io_sequence_length)
        output_list = generate_sequence(io_sequence_length)
        text_passage_list = generate_child_sequence(input_list, ta_sequence_length)
        answer_list = generate_transformed_sequence(text_passage_list, output_list)

        directory = "pattern_matching_dataset"
        filename = "pattern{}".format(index)
        path = "{}\\{}".format(directory, filename)
        json_path = path + ".json"

        if not os.path.isdir(directory):
            os.mkdir(directory)

        ImageHandler.orchestrate(input_list, output_list, index)

        text_passage = get_text_passage(text_passage_list)
        question = get_question()
        answer_choices = get_answer_choices(output_list, answer_list)
        answer = get_answer(answer_list)
        image_link = get_image_link(filename)
        problem_info_dict = {"text_passage": text_passage, "question": question, "answer_choices": answer_choices,
                             "answer": answer, "image_link": image_link}
        json = dict_to_json(problem_info_dict)
        with open(json_path, "w") as file:
            file.write(json)


if __name__ == "__main__":
    main()
