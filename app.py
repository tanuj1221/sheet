from __future__ import print_function
import os.path
from bs4 import BeautifulSoup
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from google.oauth2 import service_account
import numpy as np
import pandas as pd
import requests
from flask import *  
from selenium import webdriver
from time import sleep
app = Flask(__name__)  

def sem():
    url = "https://www.otcmarkets.com/market-activity/news"
    import os

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--window-size=1920,1080")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)

    driver.get(url)
    sleep(6)
    try:

        driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/button').click()
    except:pass
    sleep(6)

    r= driver.page_source
    soup=BeautifulSoup(r, 'html.parser')




    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'key.json'

    credentials=None
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # If modifying these scopes, delete the file token.json.


    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1X8lKo1meN11XHHMDVECpw-Ek-nKhhDg4U7iGU1VwmCs'
    service = build('sheets', 'v4', credentials=credentials)


    df_list = pd.read_html(r) # this parses all the tables in webpages to a list
    df = df_list[0]
   
    df.replace(np.nan, '', inplace=True)
    rangeAll = '{0}!A1:Z'.format('DF')
    body = {}
    resultClear = service.spreadsheets( ).values( ).clear( spreadsheetId=SAMPLE_SPREADSHEET_ID, range=rangeAll,
                                                        body=body ).execute( )
    response_date = service.spreadsheets().values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        valueInputOption='RAW',
        range='df!A1',
        body=dict(
            majorDimension='ROWS',
            values=df.T.reset_index().T.values.tolist())
    ).execute()
    driver.close()

def asx():
    url = "https://www.asx.com.au/asx/v2/statistics/todayAnns.do"


    import os

    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--window-size=1920,1080")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)




    vgc=[]
    driver.get(url)
    sleep(5)
    links=driver.find_elements_by_css_selector('a')
    for i in links:
        
        vgc.append(i.get_attribute('href'))

    r= driver.page_source
    soup=BeautifulSoup(r, 'html.parser')


    data = []



    # Get rid of empty values


    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'key.json'

    credentials=None
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # If modifying these scopes, delete the file token.json.


    df_list = pd.read_html(r) # this parses all the tables in webpages to a list
    df = df_list[0]
    df1=pd.DataFrame(vgc)
    df['links']=df1
   



    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1X8lKo1meN11XHHMDVECpw-Ek-nKhhDg4U7iGU1VwmCs'
    service = build('sheets', 'v4', credentials=credentials)






    df.replace(np.nan, '', inplace=True)

    rangeAll = '{0}!A1:Z'.format('ASX')
    body = {}
    resultClear = service.spreadsheets( ).values( ).clear( spreadsheetId=SAMPLE_SPREADSHEET_ID, range=rangeAll,
                                                        body=body ).execute( )
    response_date = service.spreadsheets().values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        valueInputOption='RAW',
        range='asx!A1',
        body=dict(
            majorDimension='ROWS',
            values=df.T.reset_index().T.values.tolist())
    ).execute()
    driver.close()


@app.route('/main')  
def asxm():
    asx()
    return render_template('index.html')

@app.route('/')  
def message():
    sem()  
    return render_template('index.html') 
if __name__ == '__main__':  
   app.run(debug = False,port=80)  
   