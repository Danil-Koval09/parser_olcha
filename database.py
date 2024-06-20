import sqlite3


class DataBase:
    def __init__(self):
        self.database = sqlite3.connect('olcha.db', check_same_thread=False)
        # Чтобы база не задерживала очередь запросов

    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                commit: bool = False):
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                result = db.commit()
            if fetchone:
                result = cursor.fetchone()
            if fetchall:
                result = cursor.fetchall()
            return result

    def create_categories_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS categories(
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_title VARCHAR(100) UNIQUE
        )
        '''
        self.manager(sql, commit=True)

    def create_products_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_title TEXT UNIQUE,
            product_detail TEXT,
            product_price INTEGER,
            product_discount INTEGER,
            product_link TEXT,
            category_id INTEGER REFERENCES categories(category_id)
        )
        '''
        self.manager(sql, commit=True)

    def save_category(self, category_title):
        sql = '''
        INSERT INTO categories(category_title) VALUES (?)
        ON CONFLICT DO NOTHING
        '''
        self.manager(sql, category_title, commit=True)

    def get_category_id(self, category_title):
        sql = '''
        SELECT category_id FROM categories WHERE category_title = ?
        '''
        return self.manager(sql, category_title, fetchone=True)


    def save_product(self, product_title, product_detail, product_price,
                     product_discount, product_link, category_id):
        sql = '''
        INSERT INTO products(product_title, product_detail, product_price,
        product_discount, product_link, category_id) VALUES (?,?,?,?,?,?)
        ON CONFLICT DO NOTHING
        '''
        self.manager(sql, product_title, product_detail, product_price,
                     product_discount, product_link, category_id, commit=True)
