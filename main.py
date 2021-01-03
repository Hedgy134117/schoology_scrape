from selenium import webdriver
import time
import json
from pprint import pprint

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

browser = webdriver.Chrome('chromedriver.exe', options=option)
browser.get("https://adfs.parklandsd.org/adfs/ls/?SAMLRequest=fZJdT8IwFIbv%2BRWm96wF5jYbIEHxgwSBAHrhjSndGTR27ezpVP69Y1P8SPRcNe85z5vznrSPItcFH5V%2BZ5bwXAL61klVb7k2yOvmgJTOcCtQITciB%2BRe8tXodsq7AeOFs95Kq8kv7H9KIILzypoGm4wHZD67nM6vJ7PHVEZRKHtnkQxPeyxkQsYySzanLJGJjMJN7yxL4jhmDXoPDiufAalsSatxQyxhYtAL4yuddVmbhe1usu7EnMW8Ez006LgKq4zwNb7zvkBOqUgzDArhnrQwKaaBddtaoxppgy0%2BEp8rkyqz%2FT%2FophlCfrNeL9qL%2BWrdmIw%2BD3BhDZY5uBW4FyXhbjn92uVzjQDlzlptt%2FtA2pxWD2Xo4cjUgQT1AmRYm%2FYPGq%2Fju%2BExUFH8zYPxyu%2F79Dv4ZVXwWRVoMl5YreS%2B1g91ZV0u%2FN%2B5O0GnVlTazupRXhosQKpMQUqONiOt7euFA%2BFhQLwrgZzQYavVLPPzSw7fAQ%3D%3D&RelayState=https%3A%2F%2Fparkland.schoology.com%2Flogin%2Fsaml&SigAlg=http%3A%2F%2Fwww.w3.org%2F2001%2F04%2Fxmldsig-more%23rsa-sha256&Signature=hbdoUO21Iw2iNViAcDI37bqBQozR4rKQ5Ugi1t8yzLp%2B%2Bu7E%2BX89%2FYgPK1ZOZHH9SgZ0g%2FOkAAC5PYubCRXUrQX2g7TW6O2UAIPrAP2Q8IazZtSZP%2FxdF08bBu%2BUrL96oW1XGYJCNIn1V0bRvjIEygMzmnufP3euq9vIJ%2BYBa4E6TPWzXwk3JPCQ%2BS%2F6kT7C8%2BthjFhFNKS398Yt2r934O4WHQPVknMeU8Rl%2FRoq95PlPt9w4kXvE4nCGtv9h1EEuuxDKr3F7VCGa9s6atv6W0P6Tl6H680oamsxoiAbl9tbLgyK4BsoTR%2BY92h%2B9ZE5PhQzy4VPN5kotNrgBms1Gw%3D%3D")

tasks = { }

def login():
    emailInput = '//*[@id="userNameInput"]'
    passInput = '//*[@id="passwordInput"]'
    loginButton = '//*[@id="submitButton"]'

    browser.find_element_by_xpath(emailInput).send_keys(input('id number: '))
    browser.find_element_by_xpath(passInput).send_keys(input('password: '))
    browser.find_element_by_xpath(loginButton).click()

def get_homework(index):
    # Go to class page
    classCard = 'sgy-card'
    time.sleep(2)
    browser.find_elements_by_class_name(classCard)[index].click()
    time.sleep(2)

    # Get class name
    Class = browser.find_element_by_xpath('//*[@id="center-top"]/h2/a').text
    
    # Get events
    eventsContainer = browser.find_element_by_xpath('//*[@id="course-events"]/div[3]/div[1]/div')
    events = eventsContainer.find_elements_by_tag_name('div')
    mostRecentDate = ""
    homework = {}

    # Check for homework and then put it in tasks
    for event in events:
        elementClass = event.get_attribute("class")
        if "date-header" in elementClass:
            mostRecentDate = event.find_element_by_tag_name('h4').text
            continue

        if "course-event" in elementClass:
            try:
                task = event.find_element_by_tag_name('a').text
            except:
                continue
            if mostRecentDate in homework: homework[mostRecentDate].append(event.find_element_by_tag_name('a').text)
            else: homework[mostRecentDate] = [event.find_element_by_tag_name('a').text]
    print(Class)
    pprint(homework)
    print()

    tasks[Class] = homework
    browser.get("https://parkland.schoology.com/home#/?_k=3c9f7c")

if __name__ == '__main__':
    input('press enter to start')
    login()
    for i in range(7):
        get_homework(i)
    with open('tasks.json', 'w') as jsonFile:
        json.dump(tasks, jsonFile)
    print('Outputted to tasks.json')