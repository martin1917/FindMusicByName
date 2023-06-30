from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium import webdriver
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import time
import os
import re

PATH_TO_NAME_PHONK = './data/PhonkName.txt'
PATH_TO_LINKS_PHONK = './data/LinksOfPhonkes.txt'
CLIENT_SECRETS_FILE = './data/client_secret.json'

def findIndexes(input: str, subStr: str) -> list[int]:
    return [i for i in range(len(input)) if input[i : i + len(subStr)] == subStr]

def findLinks():    
    PATH_TO_CHROME_DRIVER = 'D:\\Libs\\chromedriver_win32\\chromedriver.exe'
    FULL_X_PATH = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a'
    
    driver = webdriver.Chrome(service=ChromeService(executable_path=PATH_TO_CHROME_DRIVER))
    with open(file=PATH_TO_NAME_PHONK, mode='r', encoding='UTF-8') as rFile, open(file=PATH_TO_LINKS_PHONK, mode='w', encoding='UTF-8') as wFile:
        for i, line in enumerate(rFile):
            indexes = findIndexes(line, ':')
            offset = 5 if len(indexes) == 1 else 8
            name = line[offset : len(line) - 1]

            nameForQuery = name.replace(' ', '+')
            driver.get(f'https://www.youtube.com/results?search_query={nameForQuery}')
            time.sleep(1)

            element = driver.find_elements(by=By.XPATH, value=FULL_X_PATH)[0]
            targetLink = element.get_attribute('href')

            line = f'{i + 1}) {name}\n{targetLink}\n\n'
            wFile.write(line)
            print(line)

# see
# https://developers.google.com/youtube/v3/docs/playlistItems/insert
# https://developers.google.com/explorer-help/code-samples?hl=ru#python
def saveVideosToPlaylist():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes)
    
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(serviceName='youtube', version='v3', credentials=credentials)
    
    PLAYLIST_ID = 'PLnkwq-TNeFytaB3QQxLKcU4p2L8sHUTye'
    pattern = re.compile(r'v=.+&')
    with open(file=PATH_TO_LINKS_PHONK, mode='r', encoding='UTF-8') as file:
        for line in file:
            if line.startswith('https'):
                # v=...&
                idParamMatch = re.findall(pattern, line)[0]                
                videoId = idParamMatch[2 : -1]                
                request = youtube.playlistItems().insert(
                    part = 'snippet',
                    body={
                        'snippet': {
                            'playlistId': f'{PLAYLIST_ID}',
                            'resourceId': {
                                'kind': 'youtube#video',
                                'videoId': f'{videoId}'
                            }
                        }
                    }
                )
                request.execute()


if __name__ == '__main__':
    saveVideosToPlaylist()