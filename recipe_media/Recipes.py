import os
import urllib.request
from selenium import webdriver

########################################################################################################################
# DRIVER
def get_recipe_page_url():
    return "https://www.wikihow.com/Category:Recipes"

def get_local_driver():
    def get_local_directory():
        return os.path.dirname(os.path.realpath(__file__))

    def get_driver(path):
        return webdriver.Chrome(path)

    return get_driver(get_local_directory() + "\chromedriver")
########################################################################################################################
########################################################################################################################
# XPATH
def get_links_xpath():
    return "//div[@class='responsive_thumb  ']/a"

def get_method_xpath():
    return "//div[@class='method_toc_item  toc_method ']"

def get_image_xpath(step_id):
    return "//div[@id='" + step_id + "']/ol/li/div[@class='mwimg  largeimage  floatcenter ']/a/div[@class='content-spacer']/img"

def left_truncate(string, substring):
    return string[string.index(substring) + len(substring):]

def web_elements_to_string(web_elements):
    return list(map(lambda web_element: web_element.text, web_elements))
########################################################################################################################
########################################################################################################################
# SCRAPING
def get_title(driver):
    return driver.title

def get_methods(driver):
    def clean_method(method_name):
        return left_truncate(method_name, "\n")

    def clean_methods(methods):
        return list(map(lambda method: clean_method(method), methods))

    return clean_methods(web_elements_to_string(driver.find_elements_by_xpath(get_method_xpath())))

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
########################################################################################################################
driver = get_local_driver()
recipes = { }

# recipe loop
for recipe_index in range(0, 2):
    driver.get(get_recipe_page_url())
    links = driver.find_elements_by_xpath(get_links_xpath())
    driver.get(links[recipe_index].get_attribute("href"))

    recipe = {}

    recipe["title"] = get_title(driver)
    recipe["methods"] = get_methods(driver)
    save_images(driver, recipe_index, len(recipe["methods"]))
    recipes["recipe" + str(recipe_index)] = recipe

for key, value in recipes.items():
    print(key, '->', value)

driver.close()