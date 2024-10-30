import os, time, json, requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# load the config file
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
print(parent_dir)
config_path = os.path.join(current_dir,"config.json")
with open(config_path, "r") as f:    
    config = json.load(f)


# function to set up the WebDriver
def setup_driver():

    # load the user profile 
    options = webdriver.ChromeOptions();
    options.add_experimental_option("detach", True)
    options.add_argument(f"user-data-dir={config['user_data_dir']}")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    

    service = webdriver.ChromeService()
    driver = webdriver.Chrome(service = service, options=options)
    return driver

# function to log in to the website
def login(driver, username, password):
    driver.get(config["login_url"])
    time.sleep(1)

    # target elements, fill out the accounts & incredentials
    input_username = driver.find_element(By.CSS_SELECTOR, "#username")
    input_username.send_keys(username)

    input_pass = driver.find_element(By.CSS_SELECTOR, "#password")
    input_pass.send_keys(password)

    # press the sumbit button
    login_button = driver.find_element(By.CSS_SELECTOR, "body > div > form > input.btn.btn-primary")
    login_button.click()
    time.sleep(1)

def scrape_contents(driver, start_page, end_page,target_url):
    all_content = []
    for page in range(start_page, end_page+1):
        url = target_url.format(page=page)
        driver.get(url)
        time.sleep(2)

        # fetch and parse web pages
        soup = BeautifulSoup(driver.page_source, "html.parser");
        # print(soup)

        # locate all the targeted elements
        targetElements = soup.find_all("div", {"class": "quote"})

        # loop through the elements
        for e in targetElements:
            text = e.find("span", {"class":"text"}).text
            author = e.find("small", {"class":"author"}).text
            all_content.append({"quote":text, "author":author})
    
        
        print(f"Scraped page {page}")
        
    with open(os.path.join(parent_dir, "data", "content.txt"), "w") as f:
        for i in all_content:
            content = [
                f"Quote: {i['quote']}",
                f"Author: {i['author']}",
                "--------------------"
            ]
            f.write("\n".join(content) + "\n")


    return all_content

# scrape all movies with its name and its url of detail page
def scrape_details(driver, target_url):
    url_of_detail = []
    driver.get(target_url)
    time.sleep(2)

    # get the page source and parse it
    soup = BeautifulSoup(driver.page_source, "html.parser")

    for e in soup.find_all("li",{"class": "ipc-metadata-list-summary-item sc-4929eaf6-0 DLYcv cli-parent"}):
        # get the movie name
        title = e.find("h3").text.strip()
        if title:
             # find the download link
             href = e.find("a", href=True)['href']
             print("href",href)
             # join the complete urls
             full_url = urljoin(driver.current_url, href)
             url_of_detail.append({"img_name":title, "url":full_url})

    # print(img_with_url)
    return url_of_detail

def download_img(driver, target_url):
    srcs = []
    driver.get(target_url)
    time.sleep(2)

    # get the page source and parse it
    soup = BeautifulSoup(driver.page_source, "html.parser")

    results = soup.find_all("img", {"class":"I7OuT DVW3V L1BOa"})

    # find all the img tags
    for index, element in enumerate(results):
        src = element["src"]
        title = element["alt"] if 'alt' in element.attrs else str(index)
        srcs.append({"src":src, "title":title})
    
    # download the images
    for i in srcs:
        response = requests.get(i["src"])
        local_img_download_dir = os.path.join(parent_dir, "data", i["title"]+".jpg")

        with open(local_img_download_dir, "wb") as f:
            f.write(response.content)



def main():

    driver = setup_driver()

    try:
        login(driver, config["username"], config["password"])
        scrape_contents(driver, config["start_page"], config["end_page"], config["target_url"])
        # scrape_details(driver, config["target_url_2"])
        # download_img(driver, config["target_url_3"])
    except Exception as e:
        print(f"An error occured: {e}")
    # finally:
    #     driver.quit()

if __name__ == "__main__":
    main()