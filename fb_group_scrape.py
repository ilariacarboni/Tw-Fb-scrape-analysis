from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from time import sleep
import configparser
import uuid
from amazons3 import save_to_s3,retrieve_from_s3
from openai_request import get_dalle_response
#Chrome driver instance
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
driver.get("https://www.facebook.com")
sleep(2)
#accept cookies
try:
    cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[1]'))).click()
    print("accepted cookies")
except Exception as e:
    print('no cookie button')

config = configparser.RawConfigParser()
config.read('config.ini')
myemail = config['facebook']['email']
mypassw = config['facebook']['passw']

email=driver.find_element("name", "email")
email.send_keys(myemail)
password=driver.find_element("name", "pass")
password.send_keys(mypassw)
sleep(1)
login=driver.find_element("name", "login")
login.click()
sleep(2)
print("logged in")
driver.get("https://www.facebook.com/groups/affittistudentiperugia") 
sleep(4)

content_set = set()
name_list=[]
image_list=[]
counter = 1
while len(content_set) < 5:
    soup=BeautifulSoup(driver.page_source, "html.parser")
    all_posts = soup.find_all("div", {"class" : "x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"}) #classe post
    
    for post in all_posts :
        try:
            name=post.find("a",{"class" : "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f"})#classe account
            name=name.text
        except:
            name="not found"
        print(name)
        try:
            content=post.find("div",{"class" : "x11i5rnm xat24cr x1mh8g0r x1vvkbs xdj266r x126k92a"}) #classe content
            content=content.text
        except:
            content="not found"
        try:
            image=post.find("div",{"class" : "x10l6tqk x13vifvy"})
            img_tag = image.find('img')
            if img_tag is not None:
                image_url = img_tag['src']
                response = requests.get(image_url)
                file_name = f"image_{counter}.jpg"
                with open(file_name, "wb") as f:
                    f.write(response.content)
                counter +=1
            else:
                image_url = None
        except AttributeError:
            image_url = None
        if content not in content_set:
            content_set.add(content)
            name_list.append(name)
            image_list.append(image_url)

        if len(content_set) >= 5:
            break

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(5)

content_list = list(content_set)
#file json saved in storage
for i in range(len(content_list)):
    data = {"name": name_list[i], "content": content_list[i], "image": image_list[i]}
    object_name = f"object/{uuid.uuid4()}.json"
    save_to_s3(data, object_name)
#get data from storage
query_res = str(retrieve_from_s3()) 
print(query_res)

get_dalle_response("image_1.jpg")