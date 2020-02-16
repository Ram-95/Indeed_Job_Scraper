#Indeed Job Scraper
''' Given the Skill and the Location, this script will scrape the Indeed Indian website and present the matching job details.'''
try:
    import csv
    import requests
    import bs4 as bs
    from prettytable import PrettyTable
    import Slack_Push_Notification as Slack
    from datetime import datetime

    headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

    #Skills and Place of Work
    skill = input('Enter your Skill: ').strip()
    place = input('Enter the location: ').strip()
    no_of_pages = int(input('Enter the #pages to scrape: '))

    #Getting the Timestamp
    '''timestamp = datetime.now().strftime("%d%m%Y,%H_%M_%S").replace(',','_')'''


    #Name of the CSV File
    file_name = skill.title() + '_' + place.title() + '_Jobs.csv'
    #Path of the CSV File
    file_path = 'C:\\Users\\shyam\\Desktop\\' + file_name

    #Writing to the CSV File
    with open(file_path, mode = 'w') as file:
        writer = csv.writer(file, delimiter = ',', lineterminator = '\n')

        #Adding the Column Names to the CSV File
        writer.writerow(['Job_Name', 'Company', 'City', 'State', 'Apply_Link', 'Posted_Date'])

        #Table to present the Job Details
        table = PrettyTable(['Job_Name', 'Company', 'Job_URL', 'time'])

        #Requesting and getting the webpage using requests
        print('\nWeb Scraping in progress...')
        for page in range(no_of_pages):
            url = 'https://www.indeed.co.in/jobs?q=' + skill + '&l=' + place +'&start=' + str(page * 10) 
            response = requests.get(url, headers = headers)
            html = response.text

            #Scrapping the Web
            soup = bs.BeautifulSoup(html, 'lxml')
            jobs = soup.findAll('div', class_ = 'jobsearch-SerpJobCard')

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

                #Splitting the location into City and State
                location_list = location.split(',')
                state = location_list[-1]
                city = ', '.join(location_list[:len(location_list)-1])

                #Getting the Link to Job
                job_base_link = 'https://www.indeed.co.in/viewjob?jk='
                job_url = job_base_link + i['id'].split('_')[1]

                #Filtering out the jobs that were posted on or after 20 days
                time_period = i.find('div', class_= 'jobsearch-SerpJobCard-footer').find('span', class_= 'date').text
                time = time_period.split(' ')[0]
                if time == '30+':
                    continue

                elif time in ('Just', 'Today'):
                    #Adding to the table row
                    table.add_row([job_name, company, job_url, time_period])

                    #Writing to CSV File
                    writer.writerow([job_name, company, city.title(), state.title(), job_url, time_period])
                
                elif int(time) <= 29:
                    #Adding to the table row
                    table.add_row([job_name, company, job_url, time_period])

                    #Writing to CSV File
                    writer.writerow([job_name, company, city.title(), state.title(), job_url, time_period])

except Exception as e:
    print(f'EXCEPTION: {e}')

else:
    '''    
    #Printing the final Table
    print('\n********** Job Details for \'{}\' at \'{}\' ***********'.format(skill.title(), place.title()))
    print(table)
    '''
    try:
        print('\nData Written to \'{}\' Successfully.\nFile Location: {}'.format(file_name, file_path))
        Slack.slack_message(('\nData Written to \'{}\' Successfully.'.format(file_name)))
    except Exception as e:
        print(f'EXCEPTION - SLACK MODULE: {e}')
    
