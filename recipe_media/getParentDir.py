import os
from os.path import dirname, abspath
#explanation here: https://stackoverflow.com/questions/30218802/get-parent-of-current-directory-from-python-script/30218825

def main():
    parentdir = dirname((abspath(__file__)))
    folderdir = parentdir + "\\recipe_data"
    print(folderdir)
main()