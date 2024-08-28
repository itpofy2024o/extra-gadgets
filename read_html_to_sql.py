from bs4 import BeautifulSoup as BS
import sys
import requests as reres
import re
import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database=''
)

cursor = connection.cursor()

def is_string_newline(string):
  return not bool(re.search("[^\\n]", string))

url = sys.argv[1] 

file_paths = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w"]

suffix = ".html"

final_paths = [url+i+suffix for i in file_paths]

for i in final_paths:
    html_body = reres.get(i).text

    soup = BS(html_body,"html.parser")

    string_soup = str(soup)

    instances = soup.find_all("string", text="soup")

    trading_list = string_soup.split("")

    for k in range(1,len(trading_list)):
        each = trading_list[k].split("<br/>")[1:]
        datetime = each[0].split("+0800")[0].split(".")[0]
        each_data = each[1:]
        subdata = []
        for h in range(0,len(each_data),7):
            sublist = each_data[h:h + 7]
            subdata.append(sublist)

        subdata = [q[:-1] for q in subdata]
        
        for e in subdata:
            if len(e)==6:
                name = e[0]
                if "font>" in name:
                    name = name.split("font>")[1]
                if "#550055" in name:
                    name = name.split("#550055")[1].split('"')[1].split(">")[1]
                rate = e[1]
                if "font>" in rate:
                    rate = rate.split("font>")[1]
                if "#550055" in rate:
                    rate = rate.split("#550055")[1].split('"')[1].split(">")[1]
                depth = e[3]
                if "font>" in depth:
                    depth = depth.split("font>")[1]
                if "#550055" in depth:
                    depth = depth.split("#550055")[1].split('"')[1].split(">")[1]
                volume = e[2]
                if "font>" in volume:
                    volume = volume.split("font>")[1]
                if "#550055" in volume:
                    volume = volume.split("#550055")[1].split('"')[1].split(">")[1]
                comment = e[5]
                if "#550055" in comment:
                    comment = comment.split("#550055")[1].split('"')[1].split(">")[1]
                if "font>" in comment:
                    comment = comment.split("font>")[1]
                percentage = e[4]
                if "#550055" in percentage:
                    percentage = percentage.split("#550055")[1].split('"')[1].split(">")[1]
                if "font>" in percentage:
                    percentage = percentage.split("font>")[1]
                percentage = percentage.split(".")[1]
                sql = "INSERT INTO email (name, rate, depth, volume, comment, percentage, time) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                val = (name,rate,depth,volume,comment,percentage,datetime)
                print(val)
                cursor.execute(sql,val)

                connection.commit()

cursor.close()
connection.close()
        
        