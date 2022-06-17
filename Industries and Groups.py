import requests
from pathlib import Path
import mysql.connector

def get_info(info_dict):

    List_of_industry_info = []
    List_of_industry_info.append(info_dict['IndustryID'])
    List_of_industry_info.append(info_dict['IndustryName'])
    List_of_industry_info.append(info_dict['IndustryNameEnglish'])

    return List_of_industry_info

def industries_codes():
    
    Stock_Name_Path = 'C:\\Users\\Hessum\\OneDrive\\Bourse\\Stock Market Python\\Financial Market Projects\\Companies-Information\\Industries Dictionary.txt'
    Stock_Name_Per2En = open(Stock_Name_Path, 'r')
    lines = Stock_Name_Per2En.readlines()
    codes = {}

    for line in lines:
        line = line.strip()
        values = line.split(',')
        try: 
            codes[values[2]] = values[0]
        except: pass

    return codes

def industry_info2sql():

    code2name = industries_codes()

    response = requests.get('https://data.nadpco.com/v1/BaseInfo/Industries')
    all_industries_info = response.json()

    # industry_info = [IndustryID, FullName, EnglishName, AddressName]
    # IndustryID is Primary Key

    for item in all_industries_info:
        
        industry_info = get_info(item)
        try: industry_info.append(code2name['%s' %industry_info[0]])
        except: industry_info.append(None)
        format_strings = ','.join(['%s'] * len(industry_info))
        cursor.execute('INSERT INTO industries VALUES (%s)' % format_strings, tuple(industry_info))
        cnx.commit()



cnx = mysql.connector.connect(user='root', password='harchi',
                              host='127.0.0.1',
                              database='market')

cursor = cnx.cursor()
    
#industry_info2sql()
cnx.close()