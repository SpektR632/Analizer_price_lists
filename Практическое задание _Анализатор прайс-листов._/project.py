import os
import json
import csv


class PriceMachine:
    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0
    
    def load_prices(self, file_path=''):
        """
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        """
        price = []
        for i in os.listdir(self.folder_path):
            if 'price' in i:
                with open(f'{self.folder}/{i}', encoding='utf-8') as file:
                    rows = csv.DictReader(file)
                    for row in rows:
                        dict_ = json.loads(row)
                        price.append(dict(название=dict_.get('название', '') + dict_.get('продукт', '') +
                                                   dict_.get('наименование', ''),
                                          цена=dict_.get('цена', 0) + dict_.get('розница', 0),
                                          файл=i,
                                          вес=dict_.get('фасовка', 0) + dict_.get('масса', 0) + dict_.get('вес', 0),
                                          )
                                     )

        self.data = price

    def _search_product_price_weight(self, headers=0):
        """
            Возвращает номера столбцов
        """
        headers += 1
        return headers

    def export_to_html(self, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
    
    def find_text(self, text):
        while text.lower() != 'exit':
            products = list(filter(lambda x: text.lower() in x['название'], self.data))
            self.name_length = max([max(len(str(row[i])) for row in products) for i in products[0].keys()])
            header = ['Наименование', 'цена', 'вес', 'файл', 'вес за кг.']
            print('№ ')
            for column in header:
                print(f'{column}{' ' * (self.name_length - len(column))}', end=' ')
            else:
                print()
                print(f'{self._search_product_price_weight()}', end=' ')
            for product in sorted(products, key=lambda x: x['цена']/x['вес']):
                print('')
                for attr in product:
                    print(f'{product[attr]}', end=' ')
                else:
                    print(f'{product['цена']/product['вес']}')
            text = input().strip()


pm = PriceMachine()
print(pm.load_prices())

'''
    Логика работы программы
'''
print('the end')
print(pm.export_to_html())
