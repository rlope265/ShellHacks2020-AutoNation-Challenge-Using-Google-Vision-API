import re, json
from datetime import datetime

with open(r'customerAPI.json') as customer:
  data = json.load(customer)

d = datetime.today().strftime("%B %d, %Y")

def findCustomer(tag):
    for i in data['customers']:
        if i['carTag'] == tag:
            print("\nCustomer Information")
            print("--------------------")
            print('Name: ' + i['name'])
            print('Car: ' + i['car'])
            if i['nextAppt'] == d :
                print("By Appointment: Yes")
            else:
                print("By Appointment: No")    
                print('Next Appointment: ' + i['nextAppt'])
            print('Service History: ' + i['servHistory'] + '\n')