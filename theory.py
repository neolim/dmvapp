from selenium import webdriver
import datetime
import re
import os
import time

def main():
    firstname = 'John'
    lastname = 'Jonson'
    phone = '1234567890'
    dmv = ['SANTA CLARA', 'SAN JOSE', 'LOS GATOS', 'SANTA TERESA', 'FREMONT', 'HAYWARD', 'SAN MATEO', 'REDWOOD CITY']

    # Remove uncomfortable days. ex. ^[Mon|Wed].*$
    apnt_week_day = '^[Mon|Tue|Wed|Thu|Fri].*$'

    # Maximum number of days between today and appointment date. Not less than 7
    apnt_date_diff = 30
    if apnt_date_diff < 7:
        print('appointment date is too low, select more than 7 days')
        exit(1)

    url = 'https://www.dmv.ca.gov/wasapp/foa/clear.do?goTo=officeVisit&localeName=en'
    project_root = os.path.abspath(os.path.dirname(__file__))
    driver_bin = os.path.join(project_root, "bin/chromedriver_2.41")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(executable_path=driver_bin, chrome_options=options)
    today = datetime.datetime.now()

    def parse_page():
        driver.get(url)
        driver.find_element_by_id("first_name").send_keys(firstname)
        driver.find_element_by_id("last_name").send_keys(lastname)
        driver.find_element_by_name("telArea").send_keys(phone[:3])
        driver.find_element_by_name("telPrefix").send_keys(phone[3:6])
        driver.find_element_by_name("telSuffix").send_keys(phone[6:])
        driver.find_element_by_xpath("//select[@name='officeId']/option[text()='" + office + "']").click()
        driver.find_element_by_id("one_task").click()
        driver.find_element_by_id("taskCID").click()
        driver.find_element_by_name("ApptForm").submit()

    while True:
        for office in dmv:
            parse_page()
            apnt_date = driver.find_elements_by_tag_name('strong')[3].text
            print(office + " : " + apnt_date)
            pattern = re.compile(apnt_week_day)
            if pattern.match(apnt_date):
                apnt_datetime = datetime.datetime.strptime(apnt_date, "%A, %B %d, %Y at %I:%M %p")
                if (apnt_datetime - today).days < apnt_date_diff:
                    driver = webdriver.Chrome(executable_path=driver_bin)
                    parse_page()
                    time.sleep(600)
                    exit()

        time.sleep(5)

if __name__ == '__main__':
    main()