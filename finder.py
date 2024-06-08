from bs4 import BeautifulSoup
import json


def find_resources(html_content=None):
    if html_content is None: html_content = open("322.html", "r").read()
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all list items with the specific class indicating course modules
    course_modules = soup.find_all('div', class_='activity-item focus-control')
    

    # Initialize a list to store the extracted data
    extracted_data = []

    # Loop through each module and extract the title and link
    for module in course_modules:
        # print(module)
        
        title = module.get('data-activityname')
        link = module.find('div', class_='activityname').find('a').get('href')
        try: 
            type = module.find('span', class_='activitybadge').text.strip().lower().replace(" ", "")
        except:
            type = None
        if title and link:
            extracted_data.append({'title': title, 'link': link, 'type': type})
            


    if __name__ == "__main__":
    # Print the extracted data
        for data in extracted_data:
            print(f"Title: {data['title']}, Link: {data['link']}")
        
    resources = json.dumps(extracted_data)
    
    # for resource in json.loads(resources):
    #     print(resource["link"])    
    
    return resources



def demo(html_content):
    # Step 2: Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Step 3: Find all course links and names
    resources = []
    num_resources = 0

    for a_tag in soup.find_all('a', href=True):
        # resource_title = a_tag['title']
        resource_link = a_tag['href']
        if resource_link.startswith("https://oys2.baskent.edu.tr/mod/resource/view.php?id="):
            num_resources += 1
            resources.append(
                {
                # "title": resource_title,
                "link": resource_link, 
                # id as integer
                "id": int(resource_link.split("=")[-1])
                }
            )
            
    resources = json.dumps(resources)
    return resources

def content_demo():
    resources = json.loads(find_resources(open("322.html", "r").read()))
    
    for resource in resources:
        print(resource["link"])
    
    # write the list into a json file:
    with open("resources.json", "w") as file:
        json.dump(resources, file, indent=4)



def find_courses(html_content):
    # Step 2: Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Step 3: Find all course links and names
    courses = []
    num_courses = 0

    for a_tag in soup.find_all('a', href=True, title=True):
        course_title = a_tag['title']
        course_link = a_tag['href']
        if course_link.startswith("https://oys2.baskent.edu.tr/course/"):
            num_courses += 1
            courses.append(
                {
                "name": course_title,
                "code": course_title.split("-")[0].strip(),
                "link": course_link, 
                # id as integer
                "id": int(course_link.split("=")[-1])
                }
            )
            
    courses = json.dumps(courses)
    return courses


# if called with args, it is being called from main.py



def course_demo():
    courses = json.loads(find_courses(open("oys_main.html", "r").read()))
    
    for course in courses:
        print(course["name"])
    
    # write the list into a json file:
    with open("courses.json", "w") as file:
        json.dump(courses, file, indent=4)
    
if __name__ == "__main__":
    # content_demo()
    find_resources()