import requests, os
from bs4 import BeautifulSoup
import re

path = './outFile'
os.makedirs(path, exist_ok=True)

url = 'https://developer.android.com/reference/android/app/package-summary'
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')
print('Downloading page ', url, '...')
folderNameS = soup.findAll("td", {"class": "jd-linkcol"})
folderName = [re.findall('([A-Za-z]+.+)', x.text.strip())[0] for x in folderNameS]

for folder in folderName:
    subUrl = 'https://developer.android.com/reference/android/app/' + folder
    subPage = requests.get(subUrl).text
    subSoup = BeautifulSoup(subPage, 'html.parser')

    print("Scraping in progress... Please wait for a 'Done!' message")

    divs = subSoup.select('div[data-version-added]')
    list = []
    for elem in divs:
        if elem.findAll("p", {"class": "caution"}) != []:
            list.append(elem)
        elif elem.findAll("p", {"class": "note"}) != []:
            list.append(elem)
        if list != []:
            if list[0].has_attr('id'):
                list.pop(0)

        if list != []:
            output = ''
            for elem in list:
                # name = [re.findall('([A-Za-z]+.+)', x.text.strip())[0] for x in nameS]
                caution = elem.findAll("p", {"class": "caution"})
                note = elem.findAll("p", {"class": "note"})
                if caution != []:
                    name = elem.find("h3")
                    output += name.text.strip() + ":\n"
                    for c in caution:
                        output += c.text.strip()+"\n"
                elif note != []:
                    name = elem.find("h3")
                    output += name.text.strip() + ":\n"
                    for n in note:
                        output += n.text.strip()+"\n"
            file = open(path + '/' + folder, 'w')
            file.write(output)

print("Done!")
