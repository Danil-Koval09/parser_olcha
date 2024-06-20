from baseparser import BaseParser
from database import DataBase
from mixins import ProductDetailMixin
from time import time


class OlchaParser(BaseParser, ProductDetailMixin, DataBase):
    def __init__(self):
        BaseParser.__init__(self)
        ProductDetailMixin.__init__(self)
        DataBase.__init__(self)
        self.create_categories_table()
        self.create_products_table()


    def get_data(self):
        soup = self.get_soup(self.get_html())
        aside = soup.find('div', class_='catalog-page__content-aside')
        categories = aside.find_all('li', class_='filter__title')
        for category in categories:
            category_title = category.find('a').get_text()
            print(category_title)
            self.save_category(category_title)
            category_link = self.host + category.find('a').get('href')
            print(category_link)
            self.products_page_parser(category_link, category_title)

    def products_page_parser(self, category_link, category_title):
        soup = self.get_soup(self.get_html(category_link))
        catalog = soup.find('div', class_='all-products-catalog')
        products = catalog.find_all('div', class_='product-card')
        category_id = self.get_category_id(category_title)[0]  # (1, ) -> 1
        for product in products:
            product_title = product.find('div', class_='product-card__brand-name').get_text()
            print(product_title)
            product_price_new = product.find('div', class_='price__main').get_text() # '1 000 000 сум'
            # '1 000 000 сум' -> ['1', '0', '0'] -> '100' -> 100
            product_price_new = int(''.join([i for i in product_price_new if i.isdigit()]))
            print(product_price_new)
            try:
                product_price_discount = product.find('div', class_='product-card__sale').get_text(strip=True)
                product_price_discount = int(''.join([i for i in product_price_discount if i.isdigit()]))
            except:
                product_price_discount = 0
            print(product_price_discount)
            product_link = self.host + product.find('a').get('href')
            print(product_link)
            product_soup = self.get_soup(self.get_html(product_link))
            detail = self.get_detail(product_soup)
            self.save_product(product_title=product_title,
                              product_detail=detail,
                              product_price=product_price_new,
                              product_discount=product_price_discount,
                              product_link=product_link,
                              category_id=category_id)



def start_parsing():
    parser = OlchaParser()
    start = time()
    parser.get_data()
    finish = time()
    print(f'Парсер отработал за {finish - start} секунд')


start_parsing()


