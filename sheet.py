from __future__ import print_function

import os.path
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep


url = "https://www.otcmarkets.com/market-activity/news"


import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


driver.get(url)
sleep(3)

r= driver.page_source


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



