import pygsheets
import pandas as pd
import json


# global vars
creds = '..//nerds_of_prey_service_account.json'
workbook_name = 'rocinate_attendance_dkp'
workbook_url = 'https://docs.google.com/spreadsheets/d/11q6Q-GWDEONTIPbydFk56OG3V_UU8AlEmOlYVreTunA/edit?usp=sharing'

def google_auth (creds):
    try:
        conn = pygsheets.authorize(service_file = creds)
        print(conn)
        print ('Connection Successful')
        return conn
    except:
        print ('Authorization Failed')
        exit()


if __name__ == '__main__':
    # Create connection. Authorization can take a few minutes
    conn = google_auth(creds)
    book = conn.open_by_url(workbook_url)
    
    # Grab data from google sheet
    df_attendance = pd.DataFrame.from_dict(book[0].get_all_records())
    df_loot = pd.DataFrame.from_dict(book[1].get_all_records())
    print (df_attendance.head())
    print (df_loot.head())

    exit()