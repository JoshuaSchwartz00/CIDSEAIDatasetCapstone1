import string
import json
import os


class PatternData:
    question_count = 500
    default_directory = "pattern_matching_dataset"
    default_filename = "pattern{}"
    expected_text_passage_start = "Consider the following sequence:"
    expected_question = "Based on the given diagram, what would the new sequence be?"
    expected_answer_choice_count = 4
    answer_bullet = "({})"
    list_len_range = range(3, 8)
    test_function_prefix = "check"
    test_dict = {}

    @staticmethod
    def orchestrate():
        PatternData.init_testing_dict()
        PatternData.run_all_tests()
        PatternData.print_test_report()

    @staticmethod
    def print_test_report():
        for test_name, pass_count in PatternData.test_dict.items():
            print("{} passed {}/{}".format(test_name, pass_count, PatternData.question_count))

    @staticmethod
    def run_all_tests():
        for index in range(0, PatternData.question_count):
            pattern_data = PatternData.load(index)
            for test_name in PatternData.test_dict:
                test_func = getattr(PatternData, test_name)
                PatternData.test_dict[test_name] += int(test_func(pattern_data))

    @staticmethod
    def init_testing_dict():
        for attr in dir(PatternData):
            if str.startswith(attr, PatternData.test_function_prefix):
                PatternData.test_dict[attr] = 0

    @staticmethod
    def load(index):
        directory = PatternData.default_directory
        filename = PatternData.default_filename.format(index)
        ext = ".json"
        with open("{}\\{}{}".format(directory, filename, ext)) as file:
            json_dict = json.load(file)
        pattern_data = PatternData(filename, **json_dict)
        return pattern_data

    def __init__(self, filename, text_passage, question, answer_choices, answer, image_link):
        self.filename = filename
        self.text_passage = text_passage
        self.question = question
        self.answer_choices = answer_choices
        self.answer = answer
        self.image_link = image_link
        self.text_passage_list = self.derive_text_passage_list()
        self.answer_choice_dict = self.derive_answer_choice_dict()
        self.answer_list = self.derive_answer_list()

    def derive_text_passage_list(self):
        truncate_str = ": "
        try:
            truncate_index = self.text_passage.index(truncate_str) + len(truncate_str)
            text_passage_list = self.text_passage[truncate_index:].split(",")
            text_passage_list = list(map(str.strip, text_passage_list))
        except ValueError:
            text_passage_list = None
        return text_passage_list

    def derive_answer_choice_dict(self):
        answer_choice_dict = {}
        for index, letter in enumerate(string.ascii_uppercase):
            left_index = self.decide_answer_choice_index(index, True, None)
            right_index = self.decide_answer_choice_index(index + 1, False, len(self.answer_choices))
            if left_index is not None:
                self.map_answer_choice_list(answer_choice_dict, letter, left_index, right_index)
                if right_index == len(self.answer_choices):
                    break
            else:
                answer_choice_dict = None
                break
        return answer_choice_dict

    def derive_answer_list(self):
        answer_list = self.answer.split(",")
        return list(map(str.strip, answer_list))

    def map_answer_choice_list(self, answer_choice_dict, letter, left, right):
        answer_choice_list = self.answer_choices[left:right].split(",")
        answer_choice_list = list(map(str.strip, answer_choice_list))
        answer_choice_dict[letter] = answer_choice_list

    def decide_answer_choice_index(self, index, offset, default):
        letter = string.ascii_uppercase[index]
        bullet = self.answer_bullet.format(letter)
        try:
            index = self.answer_choices.index(bullet)
            if offset:
                index += len(bullet)
        except ValueError:
            index = default
        return index

    def check_text_passage_start(self):
        return str.startswith(self.text_passage, self.expected_text_passage_start)

    def check_question(self):
        return self.question == self.expected_question

    def check_answer_choice_count(self):
        passed = self.answer_choice_dict is not None
        return passed and len(self.answer_choice_dict) == self.expected_answer_choice_count

    def check_answer_choice_lettering(self):
        passed = self.answer_choice_dict is not None
        if passed:
            for index, actual_letter in enumerate(self.answer_choice_dict.keys()):
                expected_letter = string.ascii_uppercase[index]
                passed = passed and actual_letter == expected_letter
                if not passed:
                    break
        return passed

    def check_list_lengths(self):
        passed = self.text_passage_list is not None
        passed = passed and self.answer_choice_dict is not None
        passed = passed and self.answer_list is not None
        if passed:
            length = len(self.text_passage_list)
            passed = passed and length == len(self.answer_list)
            if passed:
                answer_choices = list(self.answer_choice_dict.values())
                for answer_choice in answer_choices:
                    passed = passed and length == len(answer_choice)
                    if not passed:
                        break
            passed = passed and length in self.list_len_range
        return passed

    def check_image_link(self):
        path = "{}\\{}".format(PatternData.default_directory, self.image_link)
        return os.path.isfile(path)


def main():
    PatternData.orchestrate()


if __name__ == "__main__":
    main()
