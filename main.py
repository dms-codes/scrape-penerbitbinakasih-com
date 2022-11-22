import requests
from bs4 import BeautifulSoup as bs

HOMEPAGE = 'http://www.penerbitbinakasih.com/'
kategori_urls = []
html = requests.get(HOMEPAGE).content 
soup = bs(html, 'html.parser')
res = soup.find_all('ul',id='catalog')

for r in res:
    li = r.find_all('li')
    for l in li:
        a = l.find('a')
        if a!='#':
            full_url = HOMEPAGE+a['href']
            if full_url not in kategori_urls:
                kategori_urls.append(full_url)
                print(full_url)
