This file describes how to run the recipes data collection script.
Authors: Autumn Martin & Jack Summers\
Arizona State University Senior Capstone Project
Team Name: CIDSE Large-Scale Dataset Creation for Artificial Intelligence (AI) Research
Team Members: Autumn Martin, Branden Roper, Joshua Schwartz, Jack Summers, Wei Chen, Ricky Hsu
Sponsor Name: Shailaja Sampat, PhD.

Script file name = WikiHow_recipes_6.py

Prerequisites:
-You need to install and setup on your PC:
    - Python 3
    - Google Chrome browser
    - Chromedriver for your version of Chrome from https://chromedriver.chromium.org/downloads
    - Selenium library for Python from https://selenium-python.readthedocs.io/installation.html
        - Do "pip install selenium"

Instructions: 
The above script will generate about 750 json files plus images 
with data scraped from WikiHow recipes.
- On line 6/7 of the script there is a PATH variable. You need to update
    this variable to be the path to "chromedriver.exe" on your PC.
- Create a folder where you want the generated files to be stored.
- Copy the python script to that folder and run it through the command line,
    i.e. "python3 WikiHow_recipes_6.py"



To see how many json files there are, you can run this (in Windows Powershell):
    "(Get-ChildItem -filter *.json | Measure-Object).Count"
