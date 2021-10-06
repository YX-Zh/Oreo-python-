import requests,bs4,os

url = 'https://xkcd.com/50/'
os.makedirs('xkcd',exist_ok=True)

while not url.endswith('#'):
    print(f'Downloading page {url}...')
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text,'html.parser')

    comicElem = soup.select('#comic img')
    if comicElem == []:
        print('Could not find comic image.')
    else:
        comicURL = 'https:' + comicElem[0].get('src')

        print('Downloading image %s...' % (comicURL))
        res = requests.get(comicURL)
        res.raise_for_status()

        with open(os.path.join('xkcd',os.path.basename(comicURL)),'wb') as imageFile:
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)

    prevLink = soup.select('a[rel="prev"]')[0]
    url = 'https://xkcd.com' + prevLink.get('href')

print('Done.')