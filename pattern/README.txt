Step 1 - Generating images:
    Run pattern_matching.py.
    A folder will be created called "pattern_matching_dataset" in the current working directory.
    You will see images being generated in this folder.
    Let execution finish before going to the next step.

Step 2 - Using the dataset:
    1000 files will be present in the "pattern_matching_dataset" folder.
    500 of these are JSON files, and 500 are JPG files.
    The naming scheme for these files is "pattern{index}.{extension}", where:
        index is an integer from 0 to 499
        extension can be either JSON or JPG
    The files are associated with one another by index (pattern0.json corresponds with pattern0.jpg).
    Additionally, each JSON file contains a link to its corresponding image file.
    Either association can be used when working with the dataset.
