import requests,csv
from bs4 import BeautifulSoup as bs

HOMEPAGE = 'http://www.penerbitbinakasih.com/'
FILENAME = 'data-binakasih.csv'
COLUMNS = ['Judul',
'Sub Judul',
'No. ISBN',
'Penulis',
'Jumlah Halaman',
'Berat Buku',
'Jenis Cover',
'Isi',
'Dimensi (L x P)',
'Harga',
'Deskripsi',
'URL',
'Thumbnail URL'
]
kategori_urls = []
html = requests.get(HOMEPAGE).content 
soup = bs(html, 'html.parser')
res = soup.find_all('ul',id='catalog')

with open(FILENAME, 'a+', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    col_names = COLUMNS
    writer.writerow(col_names)
    f.flush()
    for r in res:
        li = r.find_all('li')
        for l in li:
            a = l.find('a')
            if '#' not in a:
                full_url = HOMEPAGE+a['href']
                if full_url not in kategori_urls:
                    kategori_urls.append(full_url)
                    #print(full_url)
                    category_html = requests.get(full_url).content
                    category_soup = bs(category_html,'html.parser')
                    content_soup = category_soup.find_all('div',class_='content-1')
                    #print(content_soup)
                    for content in content_soup:
                        book_info = {}
                        book_url = HOMEPAGE+content.find('a')['href']
                        book_info['URL'] = book_url
                        book_html = requests.get(book_url).content
                        book_soup = bs(book_html,'html.parser')
                        tbody = book_soup.find('tbody')
                        desc_soup = book_soup.find('span', class_='content-1')
                        book_info['Deskripsi'] = desc_soup.text.strip()
                        thumbnail_url = HOMEPAGE+book_soup.find('img', class_='uiMediaThumb')['src']
                        book_info['Thumbnail URL'] = thumbnail_url
                        for tr in tbody.find_all('tr'):
                            try:
                                cat, info = tr.text.strip().replace('\n','').split(':')
                            except:
                                print(tr.text.strip().replace('\n','').split(':'))
                            book_info[cat] = info
                        print(book_info)
                        res = [book_info[x] for x in COLUMNS]
                        writer.writerow(res)
                        f.flush()
                                 
                                
                                    


