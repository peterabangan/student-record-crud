#AUTOMATE CRONBACH'S ALPHA

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import pingouin as pg


def get_cronbach_alpha(sheet_name):
    #Connection to Google Sheets & Retrieve Data
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('cronalpha.json', scope)
    client = gspread.authorize(creds)

    #Sync Data from Google Sheets
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    #Remove timestamp column (because gsheets always adds timestamp, ruins cronbach result)
    items = df.drop(df.columns[[0, 1, 2, 8]], axis=1)

    #Calculate Cronbach's Alpha
    alpha_result = pg.cronbach_alpha(data=items)
    return alpha_result

#Usage Example
alpha, ci = get_cronbach_alpha("PilotTest_Alpha")
print(f"Cronbach's Alpha: {alpha:.3f}")
print(f"95% Confidence Interval: {ci}")