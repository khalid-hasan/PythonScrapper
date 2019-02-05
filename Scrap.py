from bs4 import BeautifulSoup
import requests
import math
import csv

url_list= []
activity_names= []
review_counts= []
activity_ids= []

hasReview= True

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

a=""
for urls in url_list:
    url=urls
    headers = {'user-agent': 'my-app/0.0.1'}
    source= requests.get(url, headers=headers).text

    review_parse= BeautifulSoup(source, 'lxml')

    # try:
    package_name = review_parse.find('h1', class_='t32').text
    activity_names.append(package_name)
    print(package_name)

    if review_parse.find('button', class_='j_goto_review more m_bg_white t14') != None:
        no_of_reviews= review_parse.find('button', class_='j_goto_review more m_bg_white t14').text.split(" ")[2]
        review_count_comma_strip= str(no_of_reviews).replace(',', '')
        review_counts.append(review_count_comma_strip)
        a=no_of_reviews
        #print(no_of_reviews)
    else:
        review_counts.append(0)
        hasReview = False
        print("Hola!")



review_count = len(review_counts) - 1
activity_id_count = len(activity_ids) - 1
activity_name_count = len(activity_names) - 1

r_count = 0
a_id_count = 0
a_name_count = 0

page_no = 1

print(review_counts)
print(activity_ids)

while r_count <= review_count:
    count= int(review_counts[r_count])/10
    total_page_count= math.ceil(count)

    csv_file = open("page_1/" + activity_ids[a_id_count] + ".csv", 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['author', 'content'])
    print("---ACTIVITY_TITLE--- " + activity_names[a_name_count])
    while total_page_count >= page_no:
        try:
            main_api = f'https://www.klook.com/xos_api/v1/usrcsrv/activities/{activity_ids[a_id_count]}/reviews?page={page_no}&limit=10'
            json_data = requests.get(main_api).json()
            for each in json_data['result']['item']:
                csv_writer.writerow([each['author'], each['content']])
                print(each['author'])
                print(each['content'])
                print()
            page_no += 1
            print("PAGE_NO - " + str(page_no))
        except Exception as e:
            break

    page_no = 0
    r_count += 1
    a_id_count += 1
    a_name_count += 1

    print("R_COUNT - " + str(r_count))
    print("A_ID_COUNT - " + str(a_id_count))
    print("A_NAME_COUNT - " + str(a_name_count))

# print(url_list)
# print(review_counts)
# print(activity_ids)
