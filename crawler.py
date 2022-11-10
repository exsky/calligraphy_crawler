import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup


# To fetch all calligraphy pics
def fetch_calligraphy_links():
    links = {}
    # 米芾 7699
    url = 'http://163.20.160.14/~word/modules/myalbum/viewcat.php?pos=0&cid=10&num=7700&orderby=dateD'
    resp = requests.get(url)    # Check status_code != 200
    soup = BeautifulSoup(resp.text, 'html.parser')
    imgs = soup.find_all('img')
    for img in imgs:
        if img.get('title') is not None and img.get('src') is not None:
            ch = img.get('title')[0]
            pic_src = img.get('src')
            if ch not in links: # new ch word
                links[ch] = [pic_src]
            else:
                links[ch].append(pic_src)
    return links


async def download_ch_word_pics(ch, links, session):
    # first ch word -> just let the file name eq to ch
    # more than one links -> count and set serial
    count = 1
    for link in links:
        try:
            async with session.get(url=link) as response:
                resp_img = await response.content.read()
                if count == 1:
                    with open(f'pics/{ch}.gif', 'wb') as handler:
                        handler.write(resp_img)
                else:
                    with open(f'pics/{ch}_{count}.gif', 'wb') as handler:
                        handler.write(resp_img)
                count += 1
        except Exception as e:
            print(e)
    return True


async def download_all_calligraphy():
    all_links = fetch_calligraphy_links()
    ch_words = list(all_links.keys())
    print('Ready to download calligraphy ...')
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[download_ch_word_pics(ch, all_links[ch], session) for ch in ch_words])
    if not False in ret:
        print('Success')
