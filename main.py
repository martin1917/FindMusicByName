from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium import webdriver
import time


def findIndexes(input: str, subStr: str) -> list[int]:
    return [i for i in range(len(input)) if input[i : i + len(subStr)] == subStr]


if __name__ == '__main__':
    PATH_TO_NAME_PHONK = './PhonkName.txt'
    PATH_TO_LINKS_PHONK = './LinksOfPhonkes.txt'
    PATH_TO_CHROME_DRIVER = 'D:\\Libs\\chromedriver_win32\\chromedriver.exe'
    FULL_X_PATH = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a'
    
    driver = webdriver.Chrome(service=ChromeService(executable_path=PATH_TO_CHROME_DRIVER))

    with open(file=PATH_TO_NAME_PHONK, mode='r', encoding='UTF-8') as rFile, open(file=PATH_TO_LINKS_PHONK, mode='w', encoding='UTF-8') as wFile:
        for i, line in enumerate(rFile):
            # phonk name
            indexes = findIndexes(line, ':')
            # mm:ss ==> 5;  hh:mm:ss ==> 8
            offset = 5 if len(indexes) == 1 else 8
            name = line[offset : len(line) - 1]

            # open YouTube with specified query
            nameForQuery = name.replace(' ', '+')
            driver.get(f'https://www.youtube.com/results?search_query={nameForQuery}')
            time.sleep(1)

            # extract first video link
            element = driver.find_elements(by=By.XPATH, value=FULL_X_PATH)[0]
            targetLink = element.get_attribute('href')

            # save phonk name and its YouTube's link
            line = f'{i + 1}) {name}\n{targetLink}\n\n' 
            wFile.write(line)

            # for watching process
            print(line)