import requests
from pathlib import Path
import mysql.connector

def get_info(info_dict):
    List_of_stock_info = []
    List_of_stock_info.append(info_dict['CoID'])
    List_of_stock_info.append(info_dict['CoName'])
    List_of_stock_info.append(info_dict['CoNameEnglish'])
    List_of_stock_info.append(info_dict['CompanySymbol'])
    List_of_stock_info.append(info_dict['CoTSESymbol'])
    List_of_stock_info.append(info_dict['GroupID'])
    List_of_stock_info.append(info_dict['GroupName'])
    List_of_stock_info.append(info_dict['IndustryID'])
    List_of_stock_info.append(info_dict['IndustryName'])
    List_of_stock_info.append(info_dict['InstCode'])
    List_of_stock_info.append(info_dict['TseCIsinCode'])
    List_of_stock_info.append(info_dict['TseSIsinCode'])
    List_of_stock_info.append(info_dict['MarketID'])
    List_of_stock_info.append(info_dict['MarketName'])

    return List_of_stock_info

def stock_names():
    
    Stock_Name_Path = 'C:\\Users\\Hessum\\OneDrive\\Bourse\\Dictionary.txt'
    Stock_Name_Per2En = open(Stock_Name_Path, 'r')
    lines = Stock_Name_Per2En.readlines()
    Per2En = {}

    for line in lines:
        line = line.strip()
        values = line.split(',')
        Per2En[values[1]] = values[0]

    return Per2En

Per2En = stock_names()

response = requests.get('https://data.nadpco.com/v1/BaseInfo/Companies')
all_stock_info = response.json()

cnx = mysql.connector.connect(user='root', password='harchi',
                              host='127.0.0.1',
                              database='market')

cursor = cnx.cursor()

for item in all_stock_info:

    stock_info = get_info(item)
    try:
        stock_info.append(Per2En[stock_info[4]])
        format_strings = ','.join(['%s'] * len(stock_info))
        cursor.execute('INSERT INTO companies VALUES (%s)' % format_strings, tuple(stock_info))
        cnx.commit()

    except:
        continue



cnx.close()