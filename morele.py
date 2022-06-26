import requests
from bs4 import BeautifulSoup


def morele_finder(search_terms, headers):
    items = []
    response = requests.get(url=f"https://www.morele.net/",
                            headers=headers)

    if not response:
        print('No found')
    else:
        print('Success!')
        response = requests.get(
            url=f"https://www.morele.net/wyszukiwarka/0/0/,,,,,,,,0,,,,/1/?q={search_terms}",
            headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        with open('morele_site.html', 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

        if found_pages := soup.find_all(class_="pagination-btn-nolink-anchor"):
            pages = int(str(found_pages).split(">")[1].split("<")[0])
            print(pages)
            for i in range(1, pages + 1):
                respnse = requests.get(
                    f"https://www.morele.net/wyszukiwarka/0/0/,,,,,,,,,,,,/{i}/?q={search_terms}",
                    headers=headers)
                soup = BeautifulSoup(respnse.content, 'lxml')

                found_products = soup.find_all(lambda tag: tag.name == 'p' and
                                                           tag.get('class') == [
                                                               'cat-product'
                                                               '-name'])
                for product in found_products[:]:
                    product = product.find_next(class_='productLink', href=True)

                    items.append(morele_product(product['href'], headers))

                print(f"Page number {i} is finished!")
        else:
            response = requests.get(
                f"https://www.morele.net/wyszukiwarka/0/0/,,,,,,,,,,,,/1/?q={search_terms}",
                headers=headers)
            soup = BeautifulSoup(response.content, 'lxml')

            found_products = soup.find_all(lambda tag: tag.name == 'p' and
                                                       tag.get('class') == [
                                                           'cat-product'
                                                           '-name'])
            if not found_products:
                items.append(morele_product(
                    f"/wyszukiwarka/0/0/,,,,,,,,,,,,/1/?q={search_terms}",
                    headers))

            for product in found_products[:]:
                product = product.find_next(class_='productLink', href=True)

                items.append(morele_product(product['href'], headers))

            print(f"Page number 1 is finished!")

        # save_to_csv(items)
        return items


def morele_product(link, headers):
    product_url = f"https://www.morele.net{link}"
    response = requests.get(url=product_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        # tytuł
        title = soup.find(class_='prod-name')
        product_title = str(title).split(">")[1].split("<")[0]

        # dostep
        access = soup.find(class_='prod-available-items')

        product_access = int(
            str(access).split("<")[1].split(">")[1].split(" ")[-3])

        if product_access > 0:
            access = 'Dostepny'
        else:
            access = 'Niedostępny'

        # cena
        price = soup.find(class_='product-price')
        product_price = float(str(price).split('"')[3])

        product = {"title": product_title,
                   "access": access,
                   "price": product_price,
                   "link": product_url}

        return product
