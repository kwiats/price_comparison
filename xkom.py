import requests
from bs4 import BeautifulSoup


def xkom_finder(search_terms, headers):
    items = []
    response = requests.get(url=f"https://www.x-kom.pl/",
                            headers=headers)

    if not response:
        print('No found')
    else:
        print('Success!')
        response = requests.get(
            url=f"https://www.x-kom.pl/szukaj?page=1&sort_by"
                f"=accuracy_desc&q={search_terms}",
            headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')

        found_pages = soup.find(
            class_="sc-11oikyw-1 eeUhwh sc-1s2eiz4-0 hkZjZe", max=True)

        if found_pages:
            for i in range(1, int(found_pages['max']) + 1):

                response = requests.get(
                    url=f"https://www.x-kom.pl/szukaj?page={i}&sort_by"
                        f"=accuracy_desc&q={search_terms}",
                    headers=headers)
                soup = BeautifulSoup(response.content, 'lxml')

                found_product = soup.find_all(
                    class_="sc-162ysh3-1 dAqvUz sc-fBuWsC iSVGRw")

                for product in found_product[:]:
                    product = product.find_next(
                        class_="sc-1h16fat-0 sc-1yu46qn-7 kaqYqE", href=True)
                    link = product['href']

                    items.append(xkom_product(link, headers))

                print(f"Page number {i} is finished!")
        else:
            response = requests.get(
                url=f"https://www.x-kom.pl/szukaj?page=1&sort_by"
                    f"=accuracy_desc&q={search_terms}",
                headers=headers)
            soup = BeautifulSoup(response.content, 'lxml')

            found_product = soup.find_all(
                class_="sc-162ysh3-1 dAqvUz sc-fBuWsC iSVGRw")

            for product in found_product[:]:
                product = product.find_next(
                    class_="sc-1h16fat-0 sc-1yu46qn-7 kaqYqE", href=True)
                link = product['href']

                items.append(xkom_product(link, headers))

            print(f"Page number 1 is finished!")

    # save_to_csv(items)
    return items


def xkom_product(link, headers):
    product_url = f"https://www.x-kom.pl{link}"
    response = requests.get(url=product_url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    access = "Brak informacji."
    # tytuł
    title = soup.find(class_='sc-1bker4h-10 bdhgIb')
    product_title = str(title.h1).split(">")[1].split("<")[0]

    # dostep
    if soup.find(class_="fvs7b3-1 hQyNnf"):
        access = \
            str(soup.find(class_="fvs7b3-1 hQyNnf")).split('>')[1].split("<")[0]

    elif soup.find(class_="fvs7b3-2 jPHdZA"):
        access = \
            str(soup.find(class_="fvs7b3-1 ktMQYh")).split('>')[1].split("<")[0]


    # cena
    price = soup.find(class_="n4n86h-4 eKNYud")
    if price:
        product_price = float(
            str(price).split(">")[1].split("<")[0].replace(',', '.').replace(
                "zł", "").replace(" ", ""))
    else:
        product_price = 0

    product = {"title": product_title,
               "price": product_price,
               "access": access,
               "link": product_url, }

    return product