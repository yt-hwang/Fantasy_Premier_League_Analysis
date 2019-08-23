# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

reference: http://trap.ncirl.ie/1845/1/briangibbons.pdf

"""

from urllib.request import urlopen
import json
#from bs4 import BeautifulSoup
#from lxml import html
#import requests
import pandas as pd
#import numpy as np
from openpyxl import load_workbook
#import os
    
def writing_in_excel(path, df, sheet_name):
    writer = pd.ExcelWriter(path, datetime_format='m/d/yyyy')
    df.to_excel(writer, sheet_name = sheet_name, index=False, freeze_panes = (0,1))
    writer.save()
    writer.close()
    
def writing_sheets_in_excel(path, df, sheet_name):
    book = load_workbook(path)
    writer = pd.ExcelWriter(path, engine = 'openpyxl', date_format='m/d/yyyy')
    writer.book = book
    df.to_excel(writer, sheet_name = sheet_name, index=False, freeze_panes = (0,1))
    writer.save()
    writer.close()
    
def drop_xy(df):
    # list comprehension of the cols that end with '_y'
    to_drop = [x for x in df if x.endswith('_y')]
    df.drop(to_drop, axis=1, inplace=True)
    
    #to_replace = [x for x in df if x.endswith('_x')]
    df.columns = [c.lower().replace('_x', '') for c in df.columns] 

def creating_excel_by_keys(path, html):
    path = path
    raw_html = urlopen(html)
    data = json.load(raw_html)
    keys = list(data.keys())
    i = 0
    while i < len(keys):
        try:
            name = keys[i]
            df1 = pd.DataFrame(data[keys[i]])
            writing_in_excel(path + name + '.xlsx', df1, name)
        except:
            pass
        i += 1


player_path = 'D:\\OneDrive - Georgia State University\\Data Science\\Personal_Project\\FPL_Analysis\\data\\players2019.xlsx'
fixture_path = 'D:\\OneDrive - Georgia State University\\Data Science\\Personal_Project\\FPL_Analysis\\data\\fixtures2019.xlsx'
player_error = 'D:\\OneDrive - Georgia State University\\Data Science\\Personal_Project\\FPL_Analysis\\data\\error2019.txt'
bootstrap_path = 'D:\\OneDrive - Georgia State University\\Data Science\\Personal_Project\\FPL_Analysis\\data\\bootstrap2019.xlsx'



def player_data_scraper():
    i=1
    frames = []

    while i < 600:
        try:
            player_html = urlopen("https://fantasy.premierleague.com/drf/element-summary/" + str(i))
            #bootstrap_html = urlopen("https://fantasy.premierleague.com/drf/bootstrap-static")
            player_raw = json.load(player_html)
            #bootstrap_raw = json.load(bootstrap_html)
            #type(player_raw)
            #player_raw.keys()
            player = player_raw['history']
            #bootstrap = bootstrap_raw['elements']
            player_df = pd.DataFrame(player)
            #bootstrap_df = pd.DataFrame(bootstrap)
            
            #player_df['position'] = bootstrap_df.loc[bootstrap_df['id'] == i, 'element_type']
            
            frames.append(player_df)
            result_df = pd.concat(frames)
            result_df = pd.DataFrame(result_df)
            print(i)
            
        except:
            #Write all of the numbers for which there was errors to a file
            errfile = open(player_error, "a")
            errfile.write(str(i) + "\n")
            pass
            print(i + 'pass')
    
        print (i)
        i += 1
    return result_df


result = player_data_scraper()
result2 = result.copy()
result2 = result2.rename(columns = {'id':'every_entry_player_id'})
result2 = result2.rename(columns = {'element':'player_id'})

writing_in_excel(player_path, result2, 'player_history')

print ("Player data scraped")


path = "https://fantasy.premierleague.com/drf/bootstrap-static"
raw_html = urlopen(path)
data = json.load(raw_html)
bootstrap_df = pd.DataFrame(data['elements'])
writing_in_excel(bootstrap_path, bootstrap_df, 'elements')

teams_path = 'D:\\OneDrive - Georgia State University\\Data Science\\Personal_Project\\FPL_Analysis\\data\\teams2019.xlsx'
teams_df = pd.DataFrame(data['teams'])
writing_in_excel(teams_path, teams_df, 'teams')



df1 = result.copy()
df2 = bootstrap_df.copy()
df3 = df1.merge(df2, on='id')
drop_xy(df3)


history_bootstrap_path = 'D:\\OneDrive - Georgia State University\\Data Science\\Personal_Project\\FPL_Analysis\\data\\history_bootstrap2019.xlsx'
writing_in_excel(history_bootstrap_path, df3, 'player_history')













###################################################### fixture datafram 만들기. 보류#############################
#1) 선수 정보 불러오고
#2) history 긁어오고
#3) fixtures 긁어오고
#4) history에서 'team[1,1]' 넘버 뽑아서 empty 리스트에 넣고, 
#5) fixtures 에서 'code'랑 'difficulty'랑 'is_home' 랑 'id' 뽑아서 데이터 프레임으로 만들고
#6) 
#7) 3번의 번호와 일치하는 것 찾아서
###################################################################################################


'''
def fixtures_scraper():
    i=1
    base_df = pd.DataFrame()

    while i < 6:
        try:
            player_html = urlopen("https://fantasy.premierleague.com/drf/element-summary/" + str(i))
            player_raw = json.load(player_html)
            fixture = player_raw['fixtures']
            fixture_df = pd.DataFrame(fixture)
            base_df = pd.merge(base_df, fixture_df, how = 'outer', on='code')
            
    
        except:
            #Write all of the numbers for which there was errors to a file
            errfile = open(player_error, "a")
            errfile.write(str(i) + "\n")
            pass
    
        print (i)
        i += 1
    return base_df



test_path = 'F:\\Data Science\\Personal_Project\\FPL_Analysis\\data\\fixtures.xlsx'

player_html = urlopen("https://fantasy.premierleague.com/drf/element-summary/1")
#bootstrap_html = urlopen("https://fantasy.premierleague.com/drf/bootstrap-static")
player_raw = json.load(player_html)
#bootstrap_raw = json.load(bootstrap_html)
#type(player_raw)
player_raw.keys()
fixtures = player_raw['fixtures']
#bootstrap = bootstrap_raw['elements']
fixtures_df = pd.DataFrame(fixtures)
fixtures_df

writing_in_excel(test_path, fixtures_df, 'fixtures')

'''



'''
fixtures = fixtures_scraper()
fixture_path = 'F:\\Data Science\\Personal_Project\\FPL_Analysis\\data\\fixtures.xlsx'
writing_in_excel(fixture_path, fixtures, 'fixtures')

'''










