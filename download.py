import requests
import os
import bs4

all_episodes = []
webtoonurl = 'https://www.webtoons.com'
baseurl = 'https://www.webtoons.com/en/action/the-god-of-high-school/'
if baseurl.endswith('/'):
    name = baseurl.split('/')[-2]
else:
    name = baseurl.split('/')[-1]

title = '66'
extra = 'list?title_no='+title


def get_all_episodes(url):
    pages_list = []
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    episode_list = soup.find('ul', id='_listUl')
    paginator = soup.find('div', class_='paginate')
    for i in (a.get('href') for a in paginator.find_all('a')):
        if i != '#':
            res = requests.get(webtoonurl + i)
            print(webtoonurl + i)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, 'lxml')
            episode_list = soup.find('ul', id='_listUl')
            episode_list = (a.get('href') for a in episode_list.find_all('a'))
            # print(list(episode_list))
        yield episode_list
    if paginator.find('a', class_='pg_next'):

        for i in get_all_episodes(webtoonurl + paginator.find('a',
                                                              class_='pg_next').get('href')):
            yield i


def lazy_iterator(n=0):
    for i in range(n):
        yield i


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
    # latest_episode, diff = get_episode_diff(baseurl+extra)
            # global all_episodes
    print('Getting all episodes\n')
    fernan = list(get_all_episodes(baseurl+extra))
    print('Blame', fernan)
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
