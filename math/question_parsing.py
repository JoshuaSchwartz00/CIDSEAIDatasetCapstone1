import json


data = dict()
with open("questions.json", 'r') as f:
    data = json.load(f)
    f.close()

class Parser:
    def _init_(self, templates):
        self.templates = templates
    def parse(self):
        