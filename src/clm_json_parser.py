import pandas as pd
import pygsheets as pyg
import os


# global vars
raid_name = 'roci_20221122'
points_json = '20221122_point_history.json'
loot_json = '20221122_loot_history.json'

# static vars
creds = 'nerds_of_prey_service_account.json'
raid_log = 'raid_log.csv'
config = '..//config//'
clm_logs = './/clm_logs//'
utilities = './/utilities//'

def google_auth (creds):
    try:
        conn = pyg.authorize(service_file = creds)
        print(conn)
        print ('Connection Successful')
        return conn
    except:
        print ('Authorization Failed')
        exit()

def clean (s):
    """Brings in CLM export as string and isolates actual JSON"""
    # read in text as string
    # Find the first list
    # Keep only in first list
    # Import first list
    # Find second list
    # Third
    # return as pandas dataframe

def get_duplicate_on_time_awards(df):
    tmp = df.groupby(['player', 'reason']).count().reset_index()
    return tmp[(tmp.reason == 'On Time Bonus') & (tmp.points > 1)]

def get_on_time_awards (df):
    tmp = df.groupby(['player', 'reason']).first().reset_index()
    return tmp[tmp.reason == 'On Time Bonus']

def get_raid_completion_awards (df):
    tmp = df.groupby(['player', 'reason']).first().reset_index()
    return tmp[tmp.reason == 'Raid Completion Bonus']

def get_duplicate_raid_completion_awards(df):
    tmp = df.groupby(['player', 'reason']).count().reset_index()
    return tmp[(tmp.reason == 'Raid Completion Bonus') & (tmp.points > 1)]

def get_dkp_spent (df):
    tmp = df[['player', 'points']].groupby('player').sum().reset_index()
    return tmp

if __name__ == '__main__':
    print(os.getcwd())
    try:
        log = pd.read_csv(raid_log)
        print(log)
    except:
        log = pd.DataFrame(columns = ['raid_name', 'sheet_id'])  
        log.to_csv(raid_log)      
        log = pd.read_csv(raid_log)

    # Connect to google sheets
    gc = google_auth(config + creds)
    if raid_name in log.raid_name.values:
        print(log[log.raid_name == raid_name].sheet_id[0])
        raid_sheet = gc.open_by_key(log[log.raid_name == raid_name].sheet_id[0])
    else:
        raid_sheet = gc.create(raid_name, folder_name="Nerds")
        raid_sheet = gc.open_by_key(raid_sheet._id)
        new_raid = pd.DataFrame.from_dict({'raid_name': [raid_name], 'sheet_id': raid_sheet._id})
        log = pd.concat ([log, new_raid], axis=0,ignore_index= True )
        log.to_csv(raid_log)
    try:
        on_time_award_tab = raid_sheet.add_worksheet ('on_time_award') 
    except:    
        on_time_award_tab = raid_sheet.worksheet_by_title ('on_time_award')
        on_time_award_tab.clear()
    try:
        duplicate_on_time_award_tab = raid_sheet.add_worksheet ('duplicate_on_time_award') 
    except:
        duplicate_on_time_award_tab = raid_sheet.worksheet_by_title('duplicate_on_time_award')
        duplicate_on_time_award_tab.clear()
    try:
        raid_completion_award_tab = raid_sheet.add_worksheet ('raid_completion_award') 
    except:
        raid_completion_award_tab = raid_sheet.worksheet_by_title ('raid_completion_award') 
        raid_completion_award_tab.clear()
    try:
        duplicate_raid_completion_award_tab = raid_sheet.add_worksheet ('duplicate_raid_completion_award') 
    except:
        duplicate_raid_completion_award_tab = raid_sheet.worksheet_by_title ('duplicate_raid_completion_award') 
        duplicate_raid_completion_award_tab.clear()
    try:
        dkp_spent_tab = raid_sheet.add_worksheet ('dkp_spent')   
    except:
        dkp_spent_tab = raid_sheet.worksheet_by_title ('dkp_spent')
        dkp_spent_tab.clear()
    try:
        dkp_spent_itemized_tab = raid_sheet.add_worksheet ('dkp_spent_itemized')   
    except:
        dkp_spent_itemized_tab = raid_sheet.worksheet_by_title ('dkp_spent_itemized')
        dkp_spent_itemized_tab.clear()
    try:
        raid_sheet.del_worksheet(raid_sheet.worksheet_by_title('Sheet1'))
    except:
        pass 

    # Load CLM JSON
    df_points = pd.read_json(clm_logs + points_json)
    df_points.to_csv(clm_logs + raid_name + '_points.csv')
    df_loot = pd.read_json(clm_logs + loot_json)
    df_loot.to_csv(clm_logs +  raid_name + '_loot.csv')

    # How many people got an on time award
    on_time_award = get_on_time_awards (df_points)
    on_time_award_tab.set_dataframe(on_time_award,(1,1))

    # How many people got more than one on-time bonus
    duplicate_on_time_award = get_duplicate_on_time_awards(df_points)
    duplicate_on_time_award_tab.set_dataframe(duplicate_on_time_award,(1,1))

    # How many people got a raid completion bonus
    raid_completion_award = get_raid_completion_awards(df_points)
    raid_completion_award_tab.set_dataframe(raid_completion_award,(1,1))
    
    # How many people got more than one raid completion bonus
    duplicate_raid_completion_award = get_duplicate_raid_completion_awards(df_points)
    duplicate_raid_completion_award_tab.set_dataframe(duplicate_raid_completion_award,(1,1))

    # Who spent how much on loot
    dkp_spent = get_dkp_spent(df_loot)
    dkp_spent_itemized_tab.set_dataframe(df_loot,(1,1))
    dkp_spent_tab.set_dataframe(dkp_spent,(1,1))



    