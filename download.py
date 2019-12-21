import requests
import os
import bs4
import fire
from itertools import chain

all_episodes = []
webtoonurl = 'https://www.webtoons.com'


def get_base_values(url='https://www.webtoons.com/en/fantasy/tower-of-god/', number='95', download_folder='./'):
    return url, number, download_folder


def get_episodes(url):
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'lxml')

    episode_list = soup.find('ul', id='_listUl')
    for href in (a.get('href') for a in episode_list.find_all('a')):
        yield href


def get_pages(url):
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'lxml')

    paginator = soup.find('div', class_='paginate')

    for href in (a.get('href') for a in paginator.find_all('a')):
        if href == '#':
            continue
        yield href

    if paginator.find('a', class_='pg_next'):
        href = paginator.find('a', class_='pg_next').get('href')
        return get_pages(f'{webtoonurl}{href}')


def download_episode(url):
    url_list = []

    print('Downloading episode: '+url+'\n')

    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'lxml')

    img_list = soup.select('img._images')

    for image in img_list:
        url_list.append(image.get('data-url'))

    for index, img_url in enumerate(url_list):
        print('\t Downloading '+img_url)
        r = requests.get(img_url, headers={'Referer': url})
        file = open(os.path.join(episode_dir, str(index)+'.JPEG'), 'wb')
        print('\t Saving image in: ' +
              str(os.path.join(episode_dir, str(index)+'.JPEG'))+'\n')
        file.write(r.content)
        file.close()


if __name__ == "__main__":
    baseurl, title, download_folder = fire.Fire(get_base_values)
    extra = 'list?title_no='+str(title)

    if baseurl.endswith('/'):
        name = baseurl.split('/')[-2]
    else:
        name = baseurl.split('/')[-1]

    pages = map(
        lambda href: f'{webtoonurl}{href}',
        get_pages(baseurl + extra),
    )

    episodes = chain.from_iterable(
        map(get_episodes, pages),
    )

    # you can get the full list of episodes with
    # es = set(episodes)

    webtoon_dir = os.path.join(download_folder, name.replace('-', ' '))
    os.makedirs(webtoon_dir, exist_ok=True)
    print('Created ', webtoon_dir, '\n')

    # or lazy iterate with
    for e in episodes:
        episode_dir = os.path.join(
            webtoon_dir, str(e.split('/')[7].split('&')[-1]))
        os.makedirs(episode_dir, exist_ok=True)
        print('Created '+episode_dir+'\n')
        download_episode(url=e)
        print(e)

    # while latest_episode > 0:
    #     latest_episode -= 1
