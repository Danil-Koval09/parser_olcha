

class ProductDetailMixin:

    def get_detail(self, soup):
        detail = soup.find('div', class_='product-details__row').get_text()
        return detail