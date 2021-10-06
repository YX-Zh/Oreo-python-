import requests,bs4,os,re

begin_url = 'https://brbr9.com/PIC06/index.html'
os.makedirs('girl_photos',exist_ok=True)

# 查找第一组图片的地址
begin_res = requests.get(begin_url)
begin_res.raise_for_status()
begin_soup = bs4.BeautifulSoup(begin_res.text,'html.parser')

comicElem = begin_soup.select('div[class="row col6 clearfix"] dl dt a')
if comicElem == []:
    print("Error:未找到第一组图片！")
else:
    comicURL = "https://brbr9.com" + comicElem[0].get('href')

    # 得到起始页的页码
    regex = re.compile(r'\d+')
    first_page = int(regex.findall(comicURL)[2])

    url = comicURL
    now_page = regex.findall(url)[2]
    while int(now_page) >= (first_page-10):
        print("Downloading...")
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text,'html.parser')

        # dir_name = soup.select('div[class="main"] h1')
        os.makedirs(f'girl_photos/{now_page}',exist_ok=True)

        # 抓取当前页的所有图片
        photoList = soup.select('div[class="content"] a')
        # 循环爬取该页的每张图片
        for item_photo in photoList:
            photoURL = item_photo.get('href')
            res = requests.get(photoURL)
            res.raise_for_status()

            with open(os.path.join(f'girl_photos/{now_page}',os.path.basename(photoURL)),'wb') as imageFile:
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)

        print("Successfully!")

        nextLink = soup.select('a[class="next"]')[0]
        url = 'https://brbr9.com' + nextLink.get('href')
        now_page = regex.findall(url)[2]