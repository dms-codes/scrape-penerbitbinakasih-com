import requests,csv
from bs4 import BeautifulSoup as bs
import pandas as pd
PHONE = '6287899000416'

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

HEADERS = {
    'authority': 'www.dickssportinggoods.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
}

UI_FILENAME = 'price_comparator.ui'
DATA_FILENAME = 'data-binakasih.csv'
START_ROW_NUM = 0
SEARCH_STRING = "https://www.tokopedia.com/search?fcity=174%2C175%2C176%2C177%2C178%2C179&navsource=&ob=3&shop_tier=1%233%232&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=product&q="
SS1 = "https://www.tokopedia.com/search?condition=1&fcity=174%2C175%2C176%2C177%2C178%2C179&navsource=&ob=3&pmin="
SS2 = "&rf=true&shop_tier=1%233%232&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=product&q="

def get_dataframe(filename=FILENAME,columns=COLUMNS, start_row_num = START_ROW_NUM):
    orig_df = pd.read_csv(f'{filename}')
    df = orig_df[start_row_num-1:]
    df.columns = columns
    return df

def read_data_csv():
    col_names = COLUMNS
    df = get_dataframe(filename=DATA_FILENAME, columns=col_names,start_row_num=1)
    return df

def get_search_query_from_title(title):
    #title = title.replace('-',' ')
    title = title.replace('.',' ')
    title = title.replace(':',' ')
    title = title.replace('(',' ')
    title = title.replace(')',' ')
    title = title.lstrip()
    title = title.rstrip()
    title = title.strip()
    title = title.replace(' & ','%20%26%20')
    if len(title)<=70:
        return title
    else:
        res = ''
        _ = title.split(' ')
        for __ in _:
            if len(res)>=70:
                return res
            else:
                res += __

def scrape():
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
                                 
def runQt():
    from PyQt6 import uic
    from PyQt6 import QtCore
    from PyQt6.QtWidgets import QMainWindow,QApplication,QLineEdit,QTextEdit,QPushButton,QLabel,QFileDialog
    from PyQt6.QtGui import QPixmap,QImage
    import os
    import sys

    class UI(QMainWindow):
        def __init__(self):
            super(UI,self).__init__()
            
            uic.loadUi(UI_FILENAME,self)
            
            self.getChildren()
            self.index = 0
            self.price_comparator_qt()
            self.updateData()

            #self.startBtn.clicked.connect(self.onStart)    
            self.show()
        
        def getChildren(self):
            self.cb = QApplication.clipboard()
            self.cb.clear()
            self.totalRowsLbl = self.findChild(QLabel,'totalRowsLbl')
            self.nomorLE = self.findChild(QLineEdit,'nomorLE')
            self.nomorLE.returnPressed.connect(self.onPressed)
            
            self.titleTE = self.findChild(QTextEdit,'titleTE')
            
            self.normalPriceLE = self.findChild(QLineEdit,'normalPriceLE')
            self.discountLE = self.findChild(QLineEdit,'discLE')
            self.bepLE = self.findChild(QLineEdit,'bepLE')
            self.stockLE = self.findChild(QLineEdit,'stockLE')
            self.descTE = self.findChild(QTextEdit,'descTE')
            self.searchURLTE = self.findChild(QTextEdit,'searchURLTE')
            self.searchResultsLE = self.findChild(QLineEdit,'searchResultsLE')
            self.searchDetailsTE = self.findChild(QTextEdit,'searchDetailsTE')
            self.beratLE = self.findChild(QLineEdit,'beratLE')
            self.backBtn = self.findChild(QPushButton,'backBtn')
            self.backBtn.clicked.connect(self.onBack) 
            
            self.nextBtn = self.findChild(QPushButton,'nextBtn')
            self.nextBtn.clicked.connect(self.onNext) 
            
            #self.startBtn = self.findChild(QPushButton,'startBtn') 

            self.imgLabel = self.findChild(QLabel,'imgLabel')

            self.saveImageBtn = self.findChild(QPushButton,'saveImageBtn') 
            self.saveImageBtn.clicked.connect(self.onSaveImage) 
            
            self.copyLibrariURLBtn = self.findChild(QPushButton,'copyLibrariURLBtn')
            self.copyLibrariURLBtn.clicked.connect(self.onCopyURL) 
            
            self.tweetBtn = self.findChild(QPushButton,'tweetBtn')
            self.tweetBtn.clicked.connect(self.onTweet)
            
            self.copyTitleBtn = self.findChild(QPushButton,'copyTitleBtn')
            self.copyTitleBtn.clicked.connect(self.onCopyTitleBtnClicked)
                       
            self.copyDescBtn = self.findChild(QPushButton,'copyDescBtn')           
            self.copyDescBtn.clicked.connect(self.onCopyDescBtnClicked)


        def onCopyTitleBtnClicked(self):
            text = f'{self.titleTE.toPlainText()}'
            try:
                self.cb.setText(text)
            except:
                pass

        def onCopyDescBtnClicked(self):
            text = f'{self.descTE.toPlainText()}'
            try:
                self.cb.setText(text)
            except:
                pass
            
        def onTweet(self):
            hashtags = ''
            self.data['Penulis'][self.index] = self.data['Penulis'][self.index].strip().replace('.','')
            for t in self.titleTE.toPlainText().split(' '):
                hashtags += '#'+t.replace(':','')+' '
            if '&' in self.data['Penulis'][self.index]:
                penuliss = self.data['Penulis'][self.index].split('&')
                for penulis in penuliss:
                    hashtags +='#'+''.join(penulis.replace('.','').split(' '))+' '
            else:
                hashtags +='#'+''.join(self.data['Penulis'][self.index].split(' '))
            #tweet = f'{self.titleTE.toPlainText()} {hashtags} {self.copyLibrariURLBtn.text()}'
            tweet2 = f"""{self.titleTE.toPlainText()}\n{hashtags}\nOrder via WA: """ 
            tweet2 += f"""https://wa.me/{PHONE}?text=Hi, Toko Buku Librari. Apakah {self.titleTE.toPlainText()} masih ada? {self.li_url}""".replace(' ','%20')
            #tweet2 += f"\n{self.data['Thumbnail URL'][self.index]}"
            try:
                self.cb.setText(tweet2)
            except:
                pass

        def onCopyURL(self):
            try:
                self.cb.setText(self.li_url)
            except:
                pass
            
        def onSaveImage(self):
            default_fname = self.data['Thumbnail URL'][self.index].split('/')[-1]
            fname,_ = QFileDialog.getSaveFileName(self, 'Save File',default_fname)
            import requests
            try:
                with open(fname, 'wb') as f:
                    f.write(requests.get(self.data['Thumbnail URL'][self.index]).content)
            except:
                pass 
            
        def onPressed(self):
            self.index = int(self.nomorLE.text())-1
            self.updateData()

        def onStart(self):
            self.price_comparator_qt()
            if self.nomorLE.text()=='':
                self.index = 0
            else: 
                self.index = int(self.nomorLE.text())-1
            self.updateData()
                    
        def onNext(self):
            if self.index == len(self.data):
                self.index = self.index
            else:
                self.index += 1
            self.updateData()

        def onBack(self):
            if self.index == 0:
                self.index = self.index
            else:
                self.index -= 1
            self.updateData()
            
        def updateData(self):
            self.image = QImage()
            try:
                self.image.loadFromData(requests.get(self.data['Thumbnail URL'][self.index]).content)
            except:
                pass
            self.imgLabel.setPixmap(QPixmap(self.image).scaled(551,511,QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            self.imgLabel.show()
            
            self.totalRowsLbl.setText(f'Total Number of Data : {str(int(len(self.data)))}')
            self.nomorLE.setText(str(self.index+1))
            self.titleTE.setText(str(self.data['Judul'][self.index]).strip())
            normalprice = self.data['Harga'][self.index]
            self.normalPriceLE.setText(str(f'{normalprice}'))
            self.discountLE.setText('30%')
            price = float(self.data['Harga'][self.index].replace('Rp.',''))*1000
            #print(price)
            breakevenprice = price*(1-(0.3))*1.03
            self.bepLE.setText(f'Rp.{breakevenprice:,.0f}')
            self.stockLE.setText(str(self.data['Sub Judul'][self.index]).strip())
            self.beratLE.setText(str(self.data['Berat Buku'][self.index]).strip())
            self.descTE.setText(str(self.data['Deskripsi'][self.index]).strip())
            
            self.data['Judul'][self.index] = self.data['Judul'][self.index].strip()
            self.data['Judul'][self.index] = self.data['Judul'][self.index].replace(':',' ')
            self.data['Judul'][self.index] = self.data['Judul'][self.index].replace('?',' ')
            if len(self.data['Judul'][self.index])>70:
                self.data['Judul'][self.index] = self.data['Judul'][self.index][:70]
            search_query = SS1+str(breakevenprice)+SS2+'"'+get_search_query_from_title(self.data['Judul'][self.index].strip())+'"'
            self.searchURLTE.setText(search_query)
            
            html = requests.get(search_query,headers=HEADERS).content
            soup = bs(html, 'html.parser')
            products_soup = soup.find_all('div', class_='css-974ipl')  #css-12sieg3
            search_details_data = []
            shop_name_list = []
            res = ""
            librari_url = ''
            for product_soup in products_soup:
                
                try:
                    #product information 
                    product_url = product_soup.find('a')['href']
                    #shop location and name
                    shop_info_soup = product_soup.find('div', class_ = 'css-1rn0irl' )
                    shop_name = shop_info_soup.find('span',class_ = 'prd_link-shop-name css-1kdc32b flip').text
                    if shop_name not in shop_name_list:
                        shop_name_list.append(shop_name)
                    else: continue
                    shop_location = shop_info_soup.find('span',class_ ='prd_link-shop-loc css-1kdc32b flip').text

                    price = product_soup.find('div',class_="prd_link-product-price css-1ksb19c").text.replace("Rp","").replace(".","")
                    terjual = ""
                    try:
                        terjual = product_soup.find('span', class_="prd_label-integrity css-1duhs3e").text
                    except:pass
                    
                    if shop_name == "Librari":
                        librari_url = product_url

                    search_details_data.append([shop_name,float(price),terjual])
                except:
                    pass
            self.searchDetailsTE.setText('')
            if search_details_data: 
                try:
                    self.pricingQt(search_details_data,breakevenprice,self.data['Judul'][self.index],librari_url)
                except:
                    self.searchDetailsTE.setText('')    
                    self.copyLibrariURLBtn.setText('No URL to copy.')
            self.searchResultsLE.setText(str(len(search_details_data)))
            #self.searchDetailsTE.setText(self.data['Description'][self.index])
        
        def pricingQt(self,data,breakevenprice,title,url):
            self.li_url = url.split('?')[0]
            self.copyLibrariURLBtn.setText(self.li_url)
            url = url.split("?")[0]
            #ress = f'Search results: {len(data)}.\n'
            ress = ''
            res = []
            #put data to result if price>breakevenprice
            librari_index = 100
            for d in data:
                shop_name,price,terjual = d
                if terjual == "":
                    n = 0
                else: n = terjual.split(" ")[1]
                profit_if_price_follow = price - 50 - breakevenprice 
                if shop_name == 'Librari':
                    res.append(d)
                else:
                    if profit_if_price_follow>0:# and n :
                        res.append(d)     
            if len(res)>0:           
                for i,r in enumerate(res):
                    ress += f'{r[0]}\t{r[1]:,.2f}\t{r[2]}\n'
                    if r[0] == 'Librari':
                        librari_index = i
                        li_profit = r[1] - 50 - breakevenprice 
                        print('r[1]',r[1],breakevenprice)
                        
                #print(librari_index)
                if librari_index == 0:
                    #print(res[librari_index])
                    li_price = res[librari_index][1]
                    ress +=f'Our price is already the best @{li_price:,.2f}\n'
                    #if profit_if_price_follow>0:
                    if li_profit>0:
                        ress +=f'Profit: {li_profit:,.2f}\n'
                    else:
                        ress +=f'Loss: {li_profit:,.2f}\n'
                    
                    if len(res)>1:
                        next_price = res[librari_index+1][1] 
                        if next_price - li_price > 50:
                            ress +=f"Price can be increased to {next_price -50:,.2f}\n"
            else: print("No results.")
            print(ress)
            self.searchDetailsTE.setText(ress) 
        
        
        def price_comparator_qt(self):
            df = read_data_csv()
            if self.nomorLE.text()=='':
                startsfrom = 1
                self.nomorLE.setText(str(startsfrom))
            else: startsfrom = int(self.nomorLE.text())
            
            self.data = df[startsfrom-1:]
            
            
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec()
    
if __name__ == '__main__':
    #scrape_seller_mizanmu()
    #price_comparator(213)
    runQt()
    #pass                                
                                    


