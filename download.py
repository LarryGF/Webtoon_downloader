import requests
import os
import bs4
import fire
import json
from itertools import chain

webtoonurl = 'https://www.webtoons.com'
genreurl = 'https://www.webtoons.com/en/genre'

thumbnails_dir = 'thumbnails'


def get_all_comics_by_genre():
    os.makedirs(thumbnails_dir, exist_ok=True)
    res = requests.get(genreurl)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    contents = soup.find('div', class_='card_wrap genre').contents
    count = contents.count('\n')
    i = 0
    while i < count:
        contents.remove('\n')
        i += 1
    genres = {}
    for index, i in enumerate(contents):
        if index % 2 == 1:
            info_dict = {}
            li_list = i.find_all('li')
            for li in li_list:
                title = li.find('p', class_="subj").text
                info_dict.setdefault(title, {})
                info_dict[title]['href'] = li.find('a').get('href')
                info_dict[title]['author'] = li.find(
                    'p', class_="author").text
                info_dict[title]['likes'] = li.find(
                    'em', class_="grade_num").text
                info_dict[title]['img_url'] = li.find('img').get('src')
                info_dict[title]['img_path'] = os.path.join(
                    thumbnails_dir, title+'.jpg')

            genres[contents[index-1].text] = info_dict
    json.dump(genres, open('genres.json', 'w'), indent=2)


def get_base_values(url='https://www.webtoons.com/en/fantasy/tower-of-god/', number='95', download_folder='./'):
    return url, number, download_folder


def get_episodes(url):
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'lxml')

    episode_list = soup.find('ul', id='_listUl')
    return (a.get('href') for a in episode_list.find_all('a'))


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


def download_episode(url: str, db: dict, name: str, chapter: str):
    url_list = []

    print('Downloading episode: '+url+'\n')
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'lxml')

    img_list = soup.select('img._images')

    for image in img_list:
        url_list.append(image.get('data-url'))

    for index, img_url in enumerate(url_list):
        if db[name][chapter].setdefault(img_url, False):
            print(str(index)+'.JPEG ', 'has already been downloaded')
            continue

        print('\t Downloading '+img_url)
        r = requests.get(img_url, headers={'Referer': url})
        file = open(os.path.join(episode_dir, str(index)+'.JPEG'), 'wb')
        print('\t Saving image in: ' +
              str(os.path.join(episode_dir, str(index)+'.JPEG'))+'\n')

        file.write(r.content)
        file.close()
        db[name][chapter][img_url] = True
        db_file = open('db.json', 'w')
        json.dump(db, db_file)
        db_file.close()


if __name__ == "__main__":
    fire.Fire()
    episode_dir = ''
    # baseurl, title, download_folder = fire.Fire(get_base_values)
    # extra = 'list?title_no='+str(title)
    # if not os.path.exists('db.json'):
    #     webtoon_db = {}
    # else:
    #     webtoon_db = json.load(open('db.json'))

    # if baseurl.endswith('/'):
    #     name = baseurl.split('/')[-2]
    # else:
    #     name = baseurl.split('/')[-1]
    #     baseurl = baseurl + '/'

    # pages = map(
    #     lambda href: f'{webtoonurl}{href}',
    #     get_pages(baseurl + extra),
    # )

    # episodes = chain.from_iterable(
    #     map(get_episodes, pages),
    # )
    # webtoon_db.setdefault(name.replace('-', ' '), {})
    # # you can get the full list of episodes with
    # # es = set(episodes)

    # webtoon_dir = os.path.join(download_folder, name.replace('-', ' '))
    # os.makedirs(webtoon_dir, exist_ok=True)
    # print('Created ', webtoon_dir, '\n')

    # # or lazy iterate with
    # for e in episodes:
    #     episode = str(e.split('/')[7].split('&')[-1][len('episode_no='):])
    #     webtoon_db[name.replace('-', ' ')].setdefault(episode, {})

    #     episode_dir = os.path.join(
    #         webtoon_dir, episode)
    #     os.makedirs(episode_dir, exist_ok=True)
    #     print('Created '+episode_dir+'\n')
    #     download_episode(url=e, db=webtoon_db,
    #                      name=name.replace('-', ' '), chapter=episode)
