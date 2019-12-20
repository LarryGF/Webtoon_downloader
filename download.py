import requests
import os
import bs4

from itertools import chain

all_episodes = []
webtoonurl = 'https://www.webtoons.com'
baseurl = 'https://www.webtoons.com/en/action/the-god-of-high-school/'
if baseurl.endswith('/'):
    name = baseurl.split('/')[-2]
else:
    name = baseurl.split('/')[-1]

title = '66'
extra = 'list?title_no='+title


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


def prune_list(episode_list):
    episode_list = episode_list.sort()


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
    print('Episode difference is '+str(episode_diff)+'\n')
    return (latest_episode, episode_diff)


def download_episode(url, episode):
    url_list = []

    print('Downloading episode: '+url+'\n')

    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'lxml')

    img_list = soup.select('img._images')

    for image in img_list:
        url_list.append(image.get('data-url'))

    for index, img_url in enumerate(url_list[:2]):
        print('\t Downloading '+img_url)
        r = requests.get(img_url, headers={'Referer': url})
        file = open(os.path.join(episode_dir, str(index)+'.JPEG'), 'wb')
        print('\t Saving image in: ' +
              str(os.path.join(episode_dir, str(index)+'.JPEG'))+'\n')
        file.write(r.content)
        file.close()


if __name__ == "__main__":
    pages = map(
        lambda href: f'{webtoonurl}{href}',
        get_pages(baseurl + extra),
    )

    episodes = chain.from_iterable(
        map(get_episodes, pages),
    )

    # you can get the full list of episodes with
    # es = set(episodes)

    # or lazy iterate with
    for e in episodes:
        print(e)

    # print('Blame', list(episodes))
    # print(all_episodes)
    # all_episodes = prune_list(all_episodes)
    # print(all_episodes)
    # webtoon_dir = name.replace('-', ' ')
    # os.makedirs(webtoon_dir, exist_ok=True)
    # print('Created ' + webtoon_dir+'\n')
    # while latest_episode > 0:
    #     episode_dir = os.path.join(
    #         webtoon_dir, str(latest_episode))
    #     os.makedirs(episode_dir, exist_ok=True)
    #     print('Created '+episode_dir+'\n')
    #     download_episode(url=baseurl+'ep-{}/viewer?{}&episode_no={}'.format(
    #         latest_episode, title, latest_episode+diff), episode=latest_episode)
    #     latest_episode -= 1
