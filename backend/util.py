import gspread
from oauth2client.service_account import ServiceAccountCredentials

def init_gspread():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('path_to_your_credentials_file.json', scope)
    client = gspread.authorize(creds)
    return client