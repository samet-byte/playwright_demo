from playwright.sync_api import sync_playwright, Playwright
from time import sleep
from bs4 import BeautifulSoup
from finder import *
import json
from urllib import request
import os
from tqdm import tqdm



# sleep time
st = 1


login_page = "https://oys2.baskent.edu.tr/login/index.php"
grades_page = "https://oys2.baskent.edu.tr/grade/report/overview/index.php"
course_page_base = "https://oys2.baskent.edu.tr/course/view.php?id="

def run(playwright: Playwright):
    # firefox = playwright.firefox
    # browser = firefox.launch(headless=False)
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(login_page)
    sleep(st)
    
    # read the password from a file
    with open("p.txt", "r") as file:
        # 1st line username, 2nd line password
        [username, password] = [line.strip() for line in file.readlines()]
        page.get_by_placeholder("Username").fill(username)
        page.get_by_placeholder("Password").fill(password)
        sleep(1)
        
    page.get_by_role("button", name="Log in").click()
    print(page.title())
    sleep(st)


    # page_url = page.url
    page_content = page.content()
    courses = json.loads(find_courses(page_content))
    sleep(st)
    
    
    # loop through the courses with index
    for course in courses:
        print("Visiting course: ", course["name"])
        page.goto(course_page_base + str(course["id"]))
        sleep(st)
        
        resources = json.loads(find_resources(page.content()))
        sleep(1)
        
        
        allowed_types = ["pdf", "docx", "doc", "pptx", "ppt", "txt", "xls", "xlsx"]
        for resource in resources:
            if resource["type"] in allowed_types:
                print("Downloading ", resource["title"])
                # download the resource link to the folder with the course name
                pdf_link = resource["link"]
                pdf_title = resource["title"] + f".{resource['type']}"
                
                # create a folder with the course name if it does not exist
                course_folder = os.path.join(f"resources/{course['name']}")
                if not os.path.exists(course_folder):
                    os.makedirs(course_folder)
                
                
                pdf_path = os.path.join(course_folder, pdf_title)
                
                # if the file exists, skip
                if os.path.exists(pdf_path):
                    print(f"File {pdf_title} already exists in {course_folder}")
                    continue
                
                try:
                    with tqdm(total=1, desc=f"Downloading {resource['title']}") as pbar:
                        request.urlretrieve(pdf_link, pdf_path, reporthook=lambda count, blockSize, totalSize: pbar.update(blockSize))
                    print(f"Downloaded {pdf_title} to {pdf_path}")
                except Exception as e:
                    print(f"Failed to download {pdf_title}. Error: {e}")
                # input("Press Enter to continue...")
                    
                
        print("----------")
        
        
    page.goto(grades_page)

    # wait forever
    while True:
        pass

    # Do not close the browser or context here to keep the browser open
    # context.close()
    # browser.close()

with sync_playwright() as playwright:
    run(playwright)