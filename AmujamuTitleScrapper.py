from bs4 import BeautifulSoup
import requests
import csv

url_list= []
activity_ids= []
activity_names= []

start = 1
end = 24

csv_file = open("all_urls_amujamu.csv", 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['URL', 'Title'])

while start <= end:
    url=f'https://amujamu.com/search_results?currency=THB&page={start}'
    headers = {'user-agent': 'my-app/0.0.1'}
    source= requests.get(url, headers=headers).text

    soup= BeautifulSoup(source, 'lxml')

    for content in soup.find_all('div', class_='media-heading'):
        try:
            url = content.a['href']
            title = content.a['title']


            csv_writer.writerow([url, title])
            print(url)
            print(title)
        except Exception as e:
            pass

    start += 1
