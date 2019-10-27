#Indeed Job Scraper
''' Given the Skill and the Location, this script will scrape the Indeed Indian website and present the matching job details.'''

import csv
import requests
import bs4 as bs
from prettytable import PrettyTable

headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

#Skills and Place of Work
skill = input('Enter your Skill: ').strip()
place = input('Enter the location: ').strip()

#Name of the CSV File
file_name = skill.title() + '_' + place.title() + '_Jobs.csv'
#Path of the CSV File
file_path = 'C:\\Users\\shyam\\Desktop\\' + file_name

#Requesting and getting the webpage using requests
url = 'https://www.indeed.co.in/jobs?q=' + skill + '&l=' + place
response = requests.get(url, headers = headers)
html = response.text

#Scrapping the Web
soup = bs.BeautifulSoup(html, 'lxml')
jobs = soup.findAll('div', class_ = 'jobsearch-SerpJobCard')

#Writing to the CSV File
with open(file_path, mode = 'w') as file:
    writer = csv.writer(file, delimiter = ',', lineterminator = '\n')

    #Adding the Column Names to the CSV File
    writer.writerow(['Job_Name', 'Company', 'Location'])

    #Table to present the Job Details
    table = PrettyTable(['Job_Name', 'Company', 'Location'])

    #Getting the Job Details
    for i in jobs:
        #Getting the Job Names
        job_name = i.find('div', class_ = 'title').find('a')['title'].strip('\n').title()

        #Getting the Company Names
        company = i.find('div', class_ = 'sjcl').find('span', class_ = 'company').text.strip('\n').title()

        #Getting the Locations
        if i.find('div', class_ = 'sjcl').find('div', class_ = 'location') is None:
            location = i.find('div', class_ = 'sjcl').find('span', class_ = 'location').text.strip('\n')
        else:
            location = i.find('div', class_ = 'sjcl').find('div', class_ = 'location').text.strip('\n')

        #Adding to the table row
        table.add_row([job_name, company, location.title()])

        #Writing to CSV File
        writer.writerow([job_name, company, location.title()])
    
#Printing the final Table
print('\n********** Job Details for \'{}\' at \'{}\' ***********'.format(skill.title(), place.title()))
print(table)








