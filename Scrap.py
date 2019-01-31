from bs4 import BeautifulSoup
import requests
import math
import csv

url_list= []
activity_names= []
review_counts= []
activity_ids= []

url='https://www.klook.com/search?query=THAILAND&price_from=0&start=1&type=country'
headers = {'user-agent': 'my-app/0.0.1'}
source= requests.get(url, headers=headers).text

url_parse= BeautifulSoup(source, 'lxml')



# Scrap Activity Name
for content in url_parse.find_all('a', class_='j_activity_item_link'):
    try:
        url= content['href']

        f_url= url.split('/')[2]
        full_url=f'https://www.klook.com/activity/{f_url}'
        url_list.append(full_url)

        id_from_url= f_url.split("-")[0]
        activity_ids.append(id_from_url)
        print(full_url)
    except Exception as e:
        pass


for urls in url_list:
    url=urls
    headers = {'user-agent': 'my-app/0.0.1'}
    source= requests.get(url, headers=headers).text

    review_parse= BeautifulSoup(source, 'lxml')

    try:
        package_name = review_parse.find('h1', class_='t32').text
        activity_names.append(package_name)
        #print(package_name)

        no_of_reviews= review_parse.find('button', class_='j_goto_review more m_bg_white t14').text.split(" ")[2]
        review_count_comma_strip= str(no_of_reviews).replace(',', '')
        review_counts.append(review_count_comma_strip)
        #print(no_of_reviews)
    except Exception as e:
        print("None")



# Scrap Reviews
for review_count in review_counts:
    count= int(review_count)/10
    total_page_count= math.ceil(count)
    page_no= 1

    for activity_id in activity_ids:
        csv_file = open("reviews/" + activity_id + ".csv", 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['author', 'content'])
        if(page_no<=total_page_count):
            main_api=f'https://www.klook.com/xos_api/v1/usrcsrv/activities/{activity_id}/reviews?page={page_no}&limit=10'
            try:
                json_data = requests.get(main_api).json()

                for activity_name in activity_names:
                    print("ACTIVITY_TITLE "+activity_name)
                    for each in json_data['result']['item']:
                        csv_writer.writerow([each['author'], each['content']])
                        print(each['author'])
                        print(each['content'])
                        print()

                    print()
                csv_file.close()
            except Exception as e:
                pass

            page_no= page_no+ 1

print(activity_ids)
print(review_counts)