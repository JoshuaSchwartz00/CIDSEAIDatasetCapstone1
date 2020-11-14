import os
import urllib.request
from selenium import webdriver

def get_local_directory():
    return os.path.dirname(os.path.realpath(__file__))

def get_driver(path):
    return webdriver.Chrome(path)

def get_local_driver():
    return get_driver(get_local_directory() + "\chromedriver")

def get_image_xpath(step_id):
    return "//div[@id='" + step_id + "']/ol/li/div[@class='mwimg  largeimage  floatcenter ']/a/div[@class='content-spacer']/img"

def save_images(driver, recipe_index, num_methods):
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

driver1 = get_local_driver()
driver2 = get_local_driver()

url = "https://www.wikihow.com/Category:Recipes"
driver1.get(url)

links = driver1.find_elements_by_xpath("//div[@class='responsive_thumb  ']/a")

num_links= len(links)
method_title = ""
recipes = {
   
}
images = []
recipe_steps = []
count = 0

for i in range(0, 2):
    driver2.get(links[i].get_attribute("href"))
    
    recipe_dict = { "title": None,
    "methods": [],
    "images": None, 
    "steps": None
                   
    }
    
    methods = driver2.find_elements_by_xpath("//div[@class='method_toc_item  toc_method ']")
    num_methods = len(methods)
    save_images(driver2, i, num_methods)
    
    for j in range(0, num_methods):
        title = driver2.title
        recipe_dict["title"] = title
        recipe_steps = []
        step_id = "steps_" + str(j + 1)
        method_title = methods[j].text
    
        image_links = driver2.find_elements_by_xpath("//div[@id='"+ step_id + "']/ol/li/div[@class='mwimg  largeimage  floatcenter ']/a/div[@class='content-spacer']/img")
        recipe_step = driver2.find_elements_by_xpath("//div[@id='"+ step_id + "']/ol/li/div[@class='step']/b[@class='whb']")
    
        for f in range(0, len(recipe_step)):
            recipe_steps.append(recipe_step[f].text)
            #print(recipe_steps[f])
        #print("\n")
        for p in range(0, len(image_links)):
            src = image_links[p].get_attribute('src')
            images.append(src)
            
        recipe_dict["methods"].append(method_title)
        recipe_dict["images"] = images
        recipe_dict["steps"] = recipe_steps
        recipes["recipe" + str(count)+ "(" + str(j) + ")"] = recipe_dict
        count = count + 1


    
        
       
   
for key, value in recipes.items():
    print(key, '->', value)
    
driver2.close()
driver1.close()
