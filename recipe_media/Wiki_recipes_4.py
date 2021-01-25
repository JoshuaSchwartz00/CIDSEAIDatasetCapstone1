import urllib.request
import json
import random
from selenium import webdriver



PATH = "/home/autumn/Downloads/chromedriver" # need to change this for your own path

driver1 = webdriver.Chrome(PATH)
driver2 = webdriver.Chrome(PATH)



def get_image_xpath(step_id): # function that grabs the image xpath for an image on a page with a particular id
    return "//div[@id='" + step_id + "']/ol/li/div[@class='mwimg  largeimage  floatcenter ']/a/div[@class='content-spacer']/img"

def save_images(driver, recipe_index, num_methods): # function that
    def save_method_images(method_index):
        def get_image_links():
            return driver.find_elements_by_xpath(get_image_xpath("steps_" + str(method_index + 1)))

        def get_image_srcs(image_links):
            return list(map(lambda image_link: image_link.get_attribute("src"), image_links))

        def get_image_filename(image_index):
            return "Recipe" + str(recipe_index) + "Method" + str(method_index) + "Image" + str(image_index) + ".webp"

        def save_images(image_srcs):
            for image_index, image_src in enumerate(image_srcs):
                urllib.request.urlretrieve(image_src, get_image_filename(image_index))

        save_images(get_image_srcs(get_image_links()))

    for index in range(0, num_methods):
        save_method_images(index)

def answer_choice(answer): #function that generates a list of a random order of answer choices
    answer_list = ["(i)", "(ii)", "(iii)", "(iv)"]
    
    random.shuffle(answer_list)
    
    while answer == answer_list:
        random.shuffle(answer_list)
        
    return answer_list

def main:
    url = "https://www.wikihow.com/Category:Recipes"
    driver1.get(url)

    links = driver1.find_elements_by_xpath("//div[@class='responsive_thumb  ']/a") # links is a list of all recipe article links from the wikiHow 

    num_links= len(links)
    method_title = ""
    recipes = {}
    images = []
    recipe_steps = []
    count = 0

    for i in range(0, 10): #this for loop can be adjusted to create a number of json files containing recipe
        driver2.get(links[i].get_attribute("href"))

        recipe_dict = { "title": None, #dictionary used to store attributes of the recipe
        "methods": [],
        "images": None, 
        "steps": []

        }

        json_dict = {"Question" : None, # json dictionary to store all attributes of the json file for a recipe method
                    "Step1" : None, 
                    "Step2" : None,
                    "Step3": None, 
                     "Step4": None,
                    "Answer": None,
                    "Answer Choices": []}

        methods = driver2.find_elements_by_xpath("//div[@class='method_toc_item  toc_method ']") #method list that contains all methods for a recipe
        num_methods = len(methods)

        for j in range(0, num_methods): # this for loop creates the json file for each method of a recipe
            images = []
            answer = [None, None, None, None]
            title = driver2.title #got title
            recipe_dict["title"] = title + " " + methods[j].text
            json_dict["Question"] = "Choose the correct order of images/steps (i) through (iv) for " + title + ": " + methods[j].text


            recipe_steps = []
            step_id = "steps_" + str(j + 1)
            method_title = methods[j].text

            image_links = driver2.find_elements_by_xpath("//div[@id='"+ step_id + "']/ol/li/div[@class='mwimg  largeimage  floatcenter ']/a/div[@class='content-spacer']/img") # this grabs all images for a particular recipe method and stores them in images
            recipe_step = driver2.find_elements_by_xpath("//div[@id='"+ step_id + "']/ol/li/div[@class='step']/b[@class='whb']") # this grabs all textual steps for a particular recipe method and stores them in recipe_step

            for f in range(0, len(recipe_step)):
                recipe_steps.append(recipe_step[f].text)


            if len(recipe_steps) < 4 or len(image_links) < 4: continue # checks that there are a sufficient number of method steps and images grabbed from the website

            num_list = [0, 1, 2, 3]

            random.shuffle(num_list) #generate a list with random order of numbers 0-3

            json_dict["Step1"] = "(i) " + recipe_steps[num_list[0]]  #set step 1 of json dictionary to random recipe method textual step      
            json_dict["Step2"] = "(iii) " + recipe_steps[num_list[1]] #set step 2 of json dictionary to random recipe method textual step

            answer[num_list[0]] = "(i)"
            answer[num_list[1]] = "(iii)"
            answer[num_list[2]] = "(ii)"
            answer[num_list[3]] = "(iv)"

            json_dict["Answer"] = answer #get answer to the question

            for p in range(0, len(image_links)): #for loop grabs the url of images for every image for recipe method and stroes them in images
                src = image_links[p].get_attribute('src')
                images.append(src)

            urllib.request.urlretrieve(images[num_list[2]], "recipe" + str(i) + "method" + str(j) + "image0.webp") #download randomly selected image from list of images
            urllib.request.urlretrieve(images[num_list[3]], "recipe" + str(i) + "method" + str(j) + "image1.webp") #download randomly selected image from list of images

            json_dict["Step3"] = "(ii) " + images[num_list[2]] # set step 3 of json dictionary to randomly selected image from the images list      
            json_dict["Step4"] = "(iv) " + images[num_list[3]] # set step 4 of json dictionary to randomly selected image from the images list

            while len(json_dict["Answer Choices"]) < 4:
                ans_list = answer_choice(answer)
                if ans_list not in json_dict["Answer Choices"]:
                    json_dict["Answer Choices"].append(ans_list)

            json_dict["Answer Choices"].append(answer)
            random.shuffle(json_dict["Answer Choices"])


            recipe_dict["methods"].append(method_title)
            recipe_dict["images"] = images
            recipe_dict["steps"].append(recipe_steps)
            recipes["recipe" + str(count)+ "(" + str(j) + ")"] = recipe_dict
            count = count + 1

            # Serializing json  
            jsonfile = json.dumps(json_dict, indent = 3) 

            # Writing to sample.json 
            with open("recipe" + str(i) + "method" + str(j) + ".json", "w") as outfile: 
                outfile.write(jsonfile) 

    driver2.close()
    driver1.close()

    
if __name__ =="__main__":
    main()
