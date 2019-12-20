import requests
import os
import bs4

url_list = []
base_url = 'https://www.webtoons.com/en/action/the-god-of-high-school/ep-440/viewer?title_no=66&episode_no=443'

res = requests.get(base_url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text)

img_list = soup.select('img._images')

for image in img_list:
    url_list.append(image.get('data-url'))

for index, img_url in enumerate(url_list):
    r = requests.get(img_url, headers={'Referer': base_url})
    file = open(str(index)+'.JPEG', 'wb')
    file.write(r.content)
    file.close()
