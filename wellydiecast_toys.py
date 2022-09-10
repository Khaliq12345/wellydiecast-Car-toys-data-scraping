

# Import the librabries
from bs4 import BeautifulSoup
import pandas as pd
import aiohttp
import asyncio
import time



base_url = 'https://www.wellydiecast.com/'

item = []
item_no = []
item_scale = []
item_image = []


start = int(input(f'From page: '))
end = int(input(f'To page: ' ))
urls = []

start_time = time.time()

for x in range(start, end):
    url = f'https://www.wellydiecast.com/product.php?&keyword=&type=&scale=&mode=search&page={x}'
    urls.append(url)
    
print(urls)

# The code to parse and scrape the website
async def scrape(soup):
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



async def get_data(session, url):
    async with session.get(url) as r:
        html = await r.text()
        soup = BeautifulSoup(html, 'html5lib')
        page = await scrape(soup)
        return page


async def get_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_data(session, url))
        tasks.append(task)
    result = await asyncio.gather(*tasks)
    return result


async def main(urls):
    async with aiohttp.ClientSession() as session:
        data = await get_all(session, urls)
        return data


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = asyncio.run(main(urls))
    print(result)



data = pd.DataFrame({
    'Item name':item, 
    'Item Scale':item_scale,
    'Item image':item_image,
    'Item no':item_no
})

data.to_csv('wellydiecast_toys.csv')
print(data)

print("--- %s seconds ---" % (time.time() - start_time))