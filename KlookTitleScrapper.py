from bs4 import BeautifulSoup
import requests
import csv

url_list= []
activity_ids= []
activity_names= []

start = 1
end = 33

csv_file = open("all_urls_klook.csv", 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['URL', 'Title', 'Activity_ID'])

while start <= end:
    url=f'https://www.klook.com/search?query=THAILAND&price_from=0&start={start}&type=country'
    headers = {'user-agent': 'my-app/0.0.1'}
    source= requests.get(url, headers=headers).text

    soup= BeautifulSoup(source, 'lxml')

    for content in soup.find_all('a', class_='j_activity_item_link'):
        try:
            url = content['href']

            f_url = url.split('/')[2]
            full_url = f'https://www.klook.com/activity/{f_url}'
            url_list.append(full_url)

            id_from_url = f_url.split("-")[0]
            activity_ids.append(id_from_url)

            #csv_writer.writerow([full_url, "", ""])
            #print(full_url)
        except Exception as e:
            pass

    start += 1

for urls in url_list:
    url=urls
    headers = {'user-agent': 'my-app/0.0.1'}
    source= requests.get(url, headers=headers).text

    review_parse= BeautifulSoup(source, 'lxml')

    f_url = url.split('/')[4]
    activity_id = f_url.split('-')[0]
    full_url = f'https://www.klook.com/activity/{activity_id}'
    activity_ids.append(activity_id)

    print(activity_id)


    #print(full_url)

    package_name = review_parse.find('h1', class_='t32').text
    activity_names.append(package_name)

    csv_writer.writerow([full_url, package_name, activity_id])
    print(package_name)


print(url_list)
