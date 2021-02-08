This file describes how to run the math data collection script.
authors: Ricky Hsu and Joshua Schwartz
Arizona State University Senior Capstone Project
Team Name: CIDSE Large-Scale Dataset Creation for Artificial Intelligence (AI) Research
Team Members: Autumn Martin, Branden Roper, Joshua Schwartz, Jack Summers, Wei Chen, Ricky Hsu
Sponsor Name: Shailaja Sampat, PhD.

Script file name = main.py


## Prerequisites

To use the scripts, you need to install some additional libraries. These include Pillow and Google Images Search.

pip install -u pillow

pip install -u Google-Images-Search


## Instructions

In commandline, you run "py -3 main.py" and it will generate an output json file and annotated images. The output file will have dictionaries containing a passage, question, choices, answers, and image. The passage is the groundwork for the question, which is the text part of the VLQA format. The choices are all randomized except for the correct answer. And the image contains a relevant image with text from the question on it, thus also satisfying the VLQA requirement. This script can be run multiple times, since it uses random generation to create questions.


## Output

Output file name = generated_questions.json

Output images file = /output/
