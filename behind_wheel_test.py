from selenium import webdriver
import datetime
import time
import re
import os


firstname = 'John'
lastname = 'Johnson'
tel = '1234567890'
dl_number = 'A12345678'
birthday = '01011900'
dmv = ['SANTA CLARA', 'SAN JOSE', 'LOS GATOS', 'SANTA TERESA', 'FREMONT', 'HAYWARD', 'SAN MATEO', 'REDWOOD CITY']
apnt_week_day = '^[Mon|Tue|Wed|Thu|Fri].*$' #remove uncomfortable days. ex. ^[Mon|Wed].*$

url = 'https://www.dmv.ca.gov/wasapp/foa/clear.do?goTo=driveTest&localeName=en'
project_root = os.path.abspath(os.path.dirname(__file__))
driver_bin = os.path.join(project_root, "bin/chromedriver_2.41")
driver = webdriver.Chrome(executable_path=driver_bin)

window_idx = 0
dates = []

for office in dmv:
    # if stuck add timeout
    #time.sleep(1)
    driver.get(url)
    driver.find_element_by_xpath("//select[@name='officeId']/option[text()='" + office + "']").click()

    driver.find_element_by_id("DT").click()

    driver.find_element_by_id("first_name").send_keys(firstname)
    driver.find_element_by_id("last_name").send_keys(lastname)

    driver.find_element_by_id("dl_number").send_keys(dl_number)

    driver.find_element_by_name("birthMonth").send_keys(birthday[:2])
    driver.find_element_by_name("birthDay").send_keys(birthday[2:4])
    driver.find_element_by_name("birthYear").send_keys(birthday[4:])

    driver.find_element_by_name("telArea").send_keys(tel[:3])
    driver.find_element_by_name("telPrefix").send_keys(tel[3:6])
    driver.find_element_by_name("telSuffix").send_keys(tel[6:])

    driver.find_element_by_name("ApptForm").submit()
    current_date = driver.find_elements_by_tag_name('strong')[2].text
    pattern = re.compile(apnt_week_day)
    if pattern.match(current_date):
        dates.insert(window_idx, datetime.datetime.strptime(current_date, "%A, %B %d, %Y at %I:%M %p").strftime("%Y%m%d"))
    else:
        dates.insert(window_idx, '29000000')
    if window_idx < len(dmv) - 1:
        window_idx += 1
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[window_idx])

min_window = dates.index(min(dates))
driver.switch_to.window(driver.window_handles[min_window])
get_dmv = driver.find_elements_by_class_name("no-margin-bottom")[0].text
lowest_dmv = get_dmv.split('\n', 1)[0]

for i in range(min_window):
    driver.switch_to.window(driver.window_handles[0])
    driver.close()

for i in range(window_idx - min_window):
    driver.switch_to.window(driver.window_handles[1])
    driver.close()

driver.switch_to.window(driver.window_handles[0])
driver.find_element_by_link_text("Back").click()
driver.find_element_by_xpath("//select[@name='officeId']/option[text()='" + lowest_dmv + "']").click()
driver.find_element_by_name("ApptForm").submit()
