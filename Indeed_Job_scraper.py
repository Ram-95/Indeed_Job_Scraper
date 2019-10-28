#Indeed Job Scraper
''' Given the Skill and the Location, this script will scrape the Indeed Indian website and present the matching job details.'''


#To-Do
'''
1. Should get all the jobs from all the pages of indeed website in a single run and put them into the CSV File.
2. Get the URL of the job item - Done
'''



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
    writer.writerow(['Job_Name', 'Company', 'Location', 'Apply_Link'])

    #Table to present the Job Details
    table = PrettyTable(['Job_Name', 'Company', 'Location', 'Job_URL'])

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

        #Getting the Link to Job
        job_base_link = 'https://www.indeed.co.in/viewjob?jk='
        job_url = job_base_link + i['id'].split('_')[1]
            
        
        #Adding to the table row
        table.add_row([job_name, company, location.title(), job_url])

        #Writing to CSV File
        writer.writerow([job_name, company, location.title(), job_url])
    
#Printing the final Table
print('\n********** Job Details for \'{}\' at \'{}\' ***********'.format(skill.title(), place.title()))
print(table)
print('\n\nData Written to \'{}\' Successfully.'.format(file_name))







