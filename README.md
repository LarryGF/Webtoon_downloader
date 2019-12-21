# WEBTOON DOWNLOADER

## Summary

This scripts downloads full webtoons from [Naver Webtoon](https://www.webtoons.com). It keeps them sorted in folders in the way: `{download folder}/{webtoon title}/{episode}` for easier browsing.

## Usage

- First install the necessary requirements:
  ```
  pip install -r requirements.txt
  ```
- After that run the `download` script:

  ```
  python download {webtoon url} {title number} {download folder}
  ```

  You can check for the `webtoon url` and the `title number` in the url of the webtoon you want to download, just go to [Naver Webtoon](https://www.webtoons.com) and search for the webtoon you want and copy its' _url_. It should be something like this: `https://www.webtoons.com/en/action/the-god-of-high-school/list?title_no=66`. As you can see the _url_ is in the form: `https://www.webtoons.com/{language}/{genre}/{webtoon title}/list?title_no={title number}`. The `webtoon url` is everything up to the `webtoon title`, in this case it would be: `https://www.webtoons.com/en/action/the-god-of-high-school/`, and the `title number` would be `66`.

  ## Important notice

  In case you didn't read this README and just ran the script, every parameter has a default value:

  - **webtoon url**: https://www.webtoons.com/en/fantasy/tower-of-god/
  - **title number**: 95
  - **download folder**: ./

## Thanks

Special thanks to [@frndmg](https://github.com/frndmg) for his help on fetching all episodes' urls in a smarter, simpler way.
