from flask import Flask
import requests
from bs4 import BeautifulSoup
import selenium
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import io
import sys
import os

sys.stdout=io.TextIOWrapper(io.BytesIO(), sys.stdout.encoding)

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

username = 'myrow@beaconpa.com',
password = 'Milo4242#'
first_date = "10/16/2023"
second_date = "10/16/2023"


s = driver.get('https://plus.cq.com/login?fntoken&jumpto=https://plus.cq.com/schedules/other?1')
driver.find_element("name", "username").send_keys(username)
driver.find_element("name", "password").send_keys(password)
driver.find_element(By.XPATH, "/html/body/div[2]/form/input").click()

driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div[1]/select/option[2]").click()
time.sleep(1)

driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div[2]/input[1]").click()

driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div[2]/input[1]").clear()

calendar = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div[1]/select/option[2]")
action = ActionChains(driver)
action.double_click(on_element = calendar)

driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div[2]/input[1]").send_keys(first_date)

driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/div/div/div/div/h1").click()

driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div[2]/input[2]").click()
driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div[2]/input[2]").clear()
driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div[2]/input[2]").send_keys(second_date)

driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[3]/div/a[1]").click()
time.sleep(5)

page_source = driver.page_source

soup = BeautifulSoup(page_source, "html.parser")

dates = []
links = []
categories = []

dates = (soup.find(class_="main-hit-title").string)
print(dates)


loop = 1

while loop == 1:
    for data in soup.find_all('div', class_='entity-hit-container schedhit'):
      if (not "Economic Indicators"in data.find('p').text) and (not "- Meeting" in data.find('p').text):
        for a in data.find_all('a'):
            if a.text != " Add to Calendar":
                    txt = a.get('href')
                    x = txt.split("..",2)
                    links.append('https://plus.cq.com' + x[1])
                    categories.append(a.text) 
    try: 
        driver.find_element("id", "id26").click()
        time.sleep(4) 
        pagesource = driver.page_source
        soup = BeautifulSoup(pagesource, "html.parser") 
    except:
        loop = 0 

session = requests.Session()
login_data = {
    'username': 'myrow@beaconpa.com',
    'password': 'Milo4242#'
}
s = session.post('https://plus.cq.com/login?fntoken&jumpto=https://plus.cq.com/schedules/other?1', data = login_data)

info = []
participants = []

#Link for more info: generate the output in html

top = (f"<html xmlns:v=\"urn:schemas-microsoft-com:vml\\n"
       f"xmlns:o=\"urn:schemas-microsoft-com:office:office\\n"
       f"xmlns:w=\"urn:schemas-microsoft-com:office:word\\n"
       f"xmlns:m=\"http://schemas.microsoft.com/office/2004/12/omml\\n"
       f"xmlns=\"http://www.w3.org/TR/REC-html40\">\n"
       f"<body lang=EN-US link=\"#0563C1\" vlink=\"#954F72\" style='tab-interval:.5in;word-wrap:break-word'>\n"
       f"<div class=WordSection1>")
print(top)
#print introductory commands
mih = []
h2 = []

 
for i in range(len(links)):
    events = session.get(links[i])
    broth = BeautifulSoup(events.content, "html.parser")
    for h in broth.findAll(True, {"class":["sked-text-top"]}):
        
        if not "Not in Session" in h.text:
            h2=h.text.split(",")
            for w in h2:
                if w=="Today" or w=="TODAY":
                    printme="Today"
                if w=="Monday" or w=="Tuesday" or w=="Wednesday" or w=="Thursday" or w=="Friday":
                    printme="On "+w.rstrip()
                if "a.m." in w or "p.m." in w:
                    printme=printme+" at"+w.rstrip()
                if w=="Today" or w=="TODAY":
                    printme=printme+" at"
            print("<p class=MsoNormal>"+printme+"</p")   #MsoNormal default word
    for y in broth.findAll(class_="text"):
        if "https://" in y.get_text():
            mih = y.get_text().split("//",2)
            print ("<p class=MsoNormal><a href=\"https://" + mih[1].rstrip() + "\">More information here</a></p>")    #explaining to python the quote is text not a command        
        elif not "Contact:" in y.get_text():
            print("<p class=MsoNormal>"+y.get_text()+"</p>")
        
    for z in broth.findAll(True, {"class":["sked-text", "item"]}):
        print(z.string)     
    print("\n")       


print("</div>")
print("</body>")
print("</html>")
app = Flask(__name__)
sys.stdout.seek(0)
data=sys.stdout.read()

@app.route("/")
def index():
    return data

if __name__ == '__main__':
    app.run()
