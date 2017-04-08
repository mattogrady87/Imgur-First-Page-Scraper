import requests, os, bs4, datetime, time

extTuple = ('.png', '.jpg')
date = datetime.date.today().strftime("%m-%d-%Y")
os.makedirs("imgur" + date, exist_ok=True)
imgur = 'http://www.imgur.com'
html = requests.get(imgur)

soup = bs4.BeautifulSoup(html.text, 'html.parser')

linkList = []

# Gets all post links from first page of imgur
# find all 'anchor' tags. take out the 'href' from each. get rid of weirdos
for link in soup.find_all('a'):
    imgLink = link.get('href')
    if 'gallery' in imgLink and 'comment' not in imgLink and 'random'\
    not in imgLink and 'custom' not in imgLink:
        linkList.append(imgLink)

for item in linkList:
    itemHTML = requests.get(imgur+item)
    soup = bs4.BeautifulSoup(itemHTML.text, 'html.parser')
    itemTitle = soup.find('h1', attrs={'class': 'post-title'})

    # Get all imgs and all mp4 sources, where available
    imgTitle = soup.findAll('img')
    mp4Title = soup.find_all('source', attrs = {'type': 'video/mp4'})

    if imgTitle:

        srcName = str(itemTitle.text)
        # Forward slashes in post names cause errors under UNIX fs
        if '/' in srcName:
            srcName = srcName.replace('/', ' or ')

        i = 1
        for item in imgTitle:
            srcLink = item.get('src')
            # Beginning of links aren't applicable, so omitting
            srcLink = srcLink[4:]

            if srcLink.endswith(extTuple):
                # Imgur will add a random character at end of img name sometimes
                if len(srcLink) > 21:
                    srcLink = srcLink[:17] + srcLink[18:]

                res = requests.get('http://'+srcLink)
                res.raise_for_status()
                imageFile = open(os.path.join('imgur' + date, (srcName + ' '
                         +  str(i))), 'wb')
                print(srcLink)
                print(imageFile)
                i += 1
                # Save in chunks
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()

    if mp4Title:
        mp4Name = str(itemTitle.text)
        if '/' in mp4Name:
            mp4Name = mp4Name.replace('/', ' or ')

        i = 1
        for item in mp4Title:
            mp4Link = item.get('src')
            if 'imgur.com' in mp4Link:
                mp4Link = 'http://' + mp4Link[4:]
                res = requests.get(mp4Link)
                imageFile = open(os.path.join('imgur' + date,
                        mp4Name + ' ' +  str(i) + '.mp4'), 'wb')
                print(mp4Link)
                print(imageFile)
                i += 1
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()


