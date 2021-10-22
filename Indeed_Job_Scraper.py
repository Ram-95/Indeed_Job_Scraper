import os
import csv
import requests
from bs4 import BeautifulSoup

headers = {
    "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

# Skills and Place of Work
skill = input('Enter your Skill: ').strip()
place = input('Enter the location: ').strip()
no_of_pages = int(input('Enter the #pages to scrape: '))


# Creating the Main Directory
main_dir = os.getcwd() + '\\'
if not os.path.exists(main_dir):
    os.mkdir(main_dir)
    print('Base Directory Created Successfully.')


# Name of the CSV File
file_name = skill.title() + '_' + place.title() + '_Jobs.csv'
# Path of the CSV File
file_path = main_dir + file_name

# Writing to the CSV File
with open(file_path, mode='w') as file:
    writer = csv.writer(file, delimiter=',', lineterminator='\n')
    # Adding the Column Names to the CSV File
    writer.writerow(
        ['JOB_NAME', 'COMPANY', 'LOCATION', 'POSTED', 'APPLY_LINK'])

    # Requesting and getting the webpage using requests
    print(f'\nScraping in progress...\n')
    for page in range(no_of_pages):
        url = 'https://www.indeed.co.in/jobs?q=' + skill + \
            '&l=' + place + '&start=' + str(page * 10)
        response = requests.get(url, headers=headers)
        html = response.text

        # Scrapping the Web
        soup = BeautifulSoup(html, 'lxml')
        base_url = 'https://in.indeed.com/viewjob?jk='
        d = soup.find('div', attrs={'id': 'mosaic-provider-jobcards'})

        jobs = soup.find_all('a', class_='tapItem')

        for job in jobs:
            job_id = job['id'].split('_')[-1]
            job_title = job.find('span', title=True).text.strip()
            company = job.find('span', class_='companyName').text.strip()
            location = job.find('div', class_='companyLocation').text.strip()
            posted = job.find('span', class_='date').text.strip()
            job_link = base_url + job_id
            #print([job_title, company, location, posted, job_link])

            # Writing to CSV File
            writer.writerow(
                [job_title, company, location.title(), posted, job_link])

print(f'Jobs data written to <{file_name}> successfully.')
