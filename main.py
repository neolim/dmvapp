from selenium import webdriver
import datetime
import time
import re

url = 'https://www.dmv.ca.gov/wasapp/foa/clear.do?goTo=officeVisit&localeName=en'

driver = webdriver.Chrome()
#driver = webdriver.Firefox()

firstname = 'John'#'Yevheniia'
lastname = 'Jonson'#'Konieva'
tel = '1234567890'#'6506031270'

dmv = ['SANTA CLARA', 'SAN JOSE', 'LOS GATOS', 'SANTA TERESA', 'FREMONT', 'HAYWARD', 'SAN MATEO', 'REDWOOD CITY']

window_idx = 0
dates = []

for office in dmv:
    #time.sleep(5)
    driver.get(url)
    driver.find_element_by_id("first_name").send_keys(firstname)
    driver.find_element_by_id("last_name").send_keys(lastname)
    driver.find_element_by_name("telArea").send_keys(tel[:3])
    driver.find_element_by_name("telPrefix").send_keys(tel[3:6])
    driver.find_element_by_name("telSuffix").send_keys(tel[6:])

    driver.find_element_by_xpath("//select[@name='officeId']/option[text()='" + office + "']").click()
    driver.find_element_by_id("one_task").click()
    driver.find_element_by_id("taskDLO").click()

    driver.find_element_by_name("ApptForm").submit()

    current_date = driver.find_elements_by_tag_name('strong')[3].text
    #pattern = re.compile("^[Mon|Tue|Wed|Thu|Fri].*$")
    pattern = re.compile("^[Wed|Fri].*$")
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

for i in range(min_window):
    driver.switch_to.window(driver.window_handles[0])
    driver.close()

for i in range(window_idx - min_window):
    driver.switch_to.window(driver.window_handles[1])
    driver.close()