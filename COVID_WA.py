from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

file_dir = os.getcwd()
driver = webdriver.Chrome(file_dir + "\chromedriver_win32\chromedriver")  # Chrome Driver path
url = 'https://www.doh.wa.gov/Emergencies/Coronavirus'
driver.get(url)
time.sleep(30)  # Wait for page to load
html = driver.page_source

soup = BeautifulSoup(html, 'lxml')
table_soup = soup.find(id="pnlConfirmedCasesDeathsTbl")  # Find Table of Confirmed Cases and Deaths
table_soup_data = table_soup.tbody.find_all("tr")  # Get Table Body Data

data_list = [[0 for x in range(3)] for x in range(len(table_soup_data))]  # List to collect data from table

# Parse html for table data
for t in range(0, len(table_soup_data)):
    data_list[t][1] = table_soup_data[t].find_all('td')[len(table_soup_data[t].find_all('td')) - 2].contents[0]
    data_list[t][2] = table_soup_data[t].find_all('td')[len(table_soup_data[t].find_all('td')) - 1].contents[0]
    try:
        data_list[t][0] = table_soup_data[t].find_all('a')[0].contents[0]
    except IndexError:  # Index Error catcher since last row of data is formatted differently
        try:
            data_list[t][0] = table_soup_data[t].find_all('th')[0].contents[0].strip()
        except IndexError:
            data_list[t][0] = table_soup_data[t].find_all('td')[0].contents[0]

# Add date time pulled and disclaimer
date_pulled = 'Data Pulled as of: '
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
disclaimer = 'Source: Washington DOH'
d = [date_pulled, current_time, disclaimer]

data_list.append(d)

df = pd.DataFrame(data_list, columns=['County', 'Confirmed Cases', 'Deaths'])
df.to_csv(file_dir + '\Cases_and_Deaths_By_County.csv', index=False)
driver.quit()
