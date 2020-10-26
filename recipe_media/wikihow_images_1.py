import urllib
from selenium import webdriver
PATH = "/home/autumn/Downloads/chromedriver"

driver1 = webdriver.Chrome(PATH)

images = []

url = "https://www.wikihow.com/Make-Buttermilk-with-Vinegar"
driver1.get(url)

images = driver1.find_elements_by_tag_name('img')

num_images = len(images)
count = 0

for i in range(num_images):
    src = images[i].get_attribute('src')
    print(src)
    filename = "wikihow" + str(i) + ".png"
    urllib.request.urlretrieve(src, filename)

driver1.close()
