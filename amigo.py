from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import json
import csv
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
browser = Chrome("./chromedriver",chrome_options=options)

amigo_url = "https://amigo.amityonline.com/login/index.php"
username = 'xyz'
password = "AUXYZ1994"
sleep_time = 0.01

data_links = []
heads = ["Title", "Link"]

try:
    browser.get(amigo_url)
    browser.maximize_window()

    element = browser.find_element(By.ID, "username")
    # time.sleep(sleep_time)
    element.send_keys(username)

    element = browser.find_element(By.ID, "password")
    element.send_keys(password)
    # time.sleep(sleep_time)

    element = browser.find_element(By.ID, "loginbtn")
    element.click()

    # <a href="/ODLMS/Student/AmigoLaunchPad"><i class="fa fa-book"></i><span>My Course</span> </a>

    # element = browser.find_element(By.XPATH, "//a[@href='/ODLMS/Student/AmigoLaunchPad']")
    # element.click()
    # browser.find_element_by_link_text("My Course").click()
    # browser.get("https://amigo.amityonline.com/my/")

    # USER ENTERS COURSE DASHBOARD
    courses = browser.find_elements(
        By.XPATH,
        "//a[contains(@href,'/course/view.php')]"
        # "dashboard-card"
    )
    # print(courses)
    course_links = []
    for course in courses:
        course_links.append(course.get_attribute("href"))
    for link in course_links:
        # link="facebook.com"
        time.sleep(1)
        browser.execute_script(f"window.open('');")
        browser.switch_to.window(browser.window_handles[1])
        browser.get(link)
        pages = browser.find_elements(
            By.XPATH,
            "//a[contains(@href,'https://amigo.amityonline.com/mod/page/view.php')]"
            # "dashboard-card"
        )
        page_links = []
        for page in pages:
            page_links.append(page.get_attribute("href"))
        for sublink in page_links:
            print(f"openining {sublink}")
            browser.execute_script(f"window.open('');")

            browser.switch_to.window(browser.window_handles[2])
            browser.get(sublink)
            try:
                time.sleep(0.5)
                frame = browser.find_elements(By.CLASS_NAME, "vjs-controls-enabled")
                vid_link=''
                for vid in frame:
                    data = vid.get_attribute("data-setup-lazy")
                    data = json.loads(data)
                    vid_link=vid_link+data["sources"][0]["src"]+' ,'
                heading = browser.find_element_by_xpath("//div[@role='main']/h2").text
                # print(data)
                print(heading, vid_link)
                data_links.append([heading,vid_link ])
            except Exception as e:
                print(e)
                try:
                    heading = browser.find_element_by_xpath(
                        "//div[@role='main']/h2"
                    ).text
                    data_links.append([heading, sublink])
                except:

                    print(f"no link found in {sublink}")

            browser.close()
            browser.switch_to.window(browser.window_handles[1])
        time.sleep(sleep_time)
        browser.close()
        time.sleep(sleep_time)
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(sleep_time)
    with open("amigo.csv", "w") as f:

        # using csv.writer method from CSV package
        write = csv.writer(f)

        write.writerow(heads)
        write.writerows(data_links)


except Exception as e:
    browser.quit()
    raise Exception(e)
