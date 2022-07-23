
from bs4 import BeautifulSoup
import requests
import pandas as pd


base_url = 'https://www.wellydiecast.com/'

item = []
item_no = []
item_scale = []
item_image = []

for p in range(1,82):
    print(f'Scraping page {p}')
    response = requests.get(f'https://www.wellydiecast.com/product.php?&keyword=&type=&scale=&mode=search&page={p}')
    soup = BeautifulSoup(response.text, 'html5lib')
    # Let's find the container
    container = soup.find('div', {'class':'product_list_container'})

    for i in range(16):
        try:
            name = container.find_all('div',{'class':'name'})
            item.append(name[i].text)
        except:
            item.append('')

        try:
            item_num = container.find_all('div',{'class':'item_no'})
            item_no.append(item_num[i].text)
        except:
            item_no.append('')

        try:
            scale = container.find_all('div',{'class':'scale'})
            item_scale.append(scale[i].text)
        except:
            item_scale.append('')

        try:
            image = container.find_all('img')
            item_image.append(base_url + image[i]['src'])
        except:
            item_image.append('')

data = pd.DataFrame({
    'Item name':item, 
    'Item Scale':item_scale,
    'Item image':item_image,
    'Item no':item_no
})

data.to_csv('wellydiecast_toys.csv')
print(data)








