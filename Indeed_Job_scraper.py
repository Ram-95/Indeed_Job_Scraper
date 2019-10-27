#Indeed Job Scraper
''' Given the Skill and the Location, this script will scrape the Indeed Indian website and present the matching job details.'''

import requests
import bs4 as bs
from prettytable import PrettyTable

headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

#Skills and Place of Work
skill = input('Enter your Skill: ').strip()
place = input('Enter the location: ').strip()

url = 'https://www.indeed.co.in/jobs?q=' + skill + '&l=' + place
response = requests.get(url, headers = headers)
html = response.text

#Scrapping the Web
soup = bs.BeautifulSoup(html, 'lxml')
jobs = soup.findAll('div', class_ = 'jobsearch-SerpJobCard')


#Table to present the Job Details
table = PrettyTable(['Job_Name', 'Company', 'Location'])

#Getting the Job Details
for i in jobs:
    #Getting the Job Names
    job_name = i.find('div', class_ = 'title').find('a')['title'].strip('\n')

    #Getting the Company Names
    company = i.find('div', class_ = 'sjcl').find('span', class_ = 'company').text.strip('\n').title()

    #Getting the Locations
    if i.find('div', class_ = 'sjcl').find('div', class_ = 'location') is None:
        location = i.find('div', class_ = 'sjcl').find('span', class_ = 'location').text.strip('\n')
    else:
        location = i.find('div', class_ = 'sjcl').find('div', class_ = 'location').text.strip('\n')

    table.add_row([job_name, company, location])

    
#Printing the final Table
print('\n********** Job Details for \'{}\' at \'{}\' ***********'.format(skill.title(), place.title()))
print(table)








