import requests
import os
import bs4

url_list = []
base_url = 'https://www.webtoons.com/en/action/the-god-of-high-school/ep-440/viewer?title_no=66&episode_no=443'
baseurl = 'https://www.webtoons.com/en/action/the-god-of-high-school/'
extra = 'list?title_no=66'


def get_episode_diff(url):
    print('Getting episode difference')
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    episode_list = soup.find('ul', id='_listUl')
    latest_episode_url = episode_list.find_all('li')[0].find('a').get('href')
    latest_episode = int(latest_episode_url.split('/')[6][3:])
    latest_real_episode = int(latest_episode_url.split(
        '/')[7].split('&')[-1][len('episode_no='):])
    episode_diff = latest_real_episode - latest_episode
    return (latest_episode, episode_diff)


def download_episode(url, episode):
    print('Downloading: '+url)
    os.makedirs(str(episode), exist_ok=True)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'lxml')

    img_list = soup.select('img._images')

    for image in img_list:
        url_list.append(image.get('data-url'))

    for index, img_url in enumerate(url_list):
        r = requests.get(img_url, headers={'Referer': url})
        file = open(os.path.join(str(episode), str(index)+'.JPEG'), 'wb')
        print('Saving image in: ' +
              str(os.path.join(str(episode), str(index)+'.JPEG')))
        file.write(r.content)
        file.close()


if __name__ == "__main__":
    latest_episode, diff = get_episode_diff(baseurl+extra)
    download_episode(url=baseurl+'ep-{}/viewer?title_no=66&episode_no={}'.format(
        latest_episode, latest_episode+diff), episode=latest_episode)
