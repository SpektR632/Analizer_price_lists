import os
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
        for i in os.listdir(file_path):
            if 'price' in i:
                with open(f'{file_path}/{i}', encoding='utf-8') as f:
                    rows = csv.DictReader(f, delimiter=',')
                    for row in rows:
                        price.append(dict(название=row.get('название', '') + row.get('продукт', '') +
                                                   row.get('наименование', '') + row.get('товар', ''),
                                          цена=row.get('цена', '') + row.get('розница', ''),
                                          вес=row.get('фасовка', '') + row.get('масса', '') + row.get('вес', ''),
                                          файл=i,
                                          )
                                     )

        self.data = price
        return self.data

    def export_to_html(self, fname='output.html'):
        self.result = '''
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
        number = 0
        for product in self.data:
            number = self._search_product_price_weight(number)
            self.result += f"""
                    <tr>
                        <td>{number}</td>
                        <td>{product['название']}</td>
                        <td>{product['цена']}</td>
                        <td>{product['вес']}</td>
                        <td>{product['файл']}</td>
                        <td>{round(int(product['цена']) / int(product['вес']), 2)}</td>
                    </tr>
                """

        self.result += """
                </table>
            </body>
            </html>
            """

        with open(fname, 'w', encoding='utf-8') as file:
            file.write(self.result)
        return 'Файл успешно создан!'

    def _search_product_price_weight(self, headers):
        """
            Возвращает номера столбцов
        """
        headers += 1
        return headers

    def find_text(self, text):
        while text.lower() != 'exit':
            products = list(filter(lambda x: text.lower() in x['название'].lower(), self.data))
            if products:
                self.name_length = max([max(len(str(row[i])) for row in products) for i in products[0].keys()])
                header = ['Наименование', 'Цена', 'Вес', 'Файл', 'Цена за кг.']
                print('№', end=' ')
                for column in header:
                    print(f'{column}{' ' * (self.name_length - len(column))}', end=' ')
                else:
                    print()
                number = 0
                for product in sorted(products, key=lambda x: int(x['цена']) / int(x['вес'])):
                    number = self._search_product_price_weight(number)
                    print(f'{number}', end=' ')
                    for attr in product:
                        print(f'{product[attr]}{' ' * (self.name_length - len(product[attr]))}', end=' ')
                    else:
                        print(f'{round(int(product['цена']) / int(product['вес']), 2)}')
            text = input("Введите текст для поиска:\n").strip()


"""
    Логика работы программы
"""
pm = PriceMachine()
pm.load_prices('C:/Users/Роман/PycharmProjects/Analizer_price_lists/'
               'Практическое задание _Анализатор прайс-листов._')
pm.find_text(input("Введите текст для поиска:\n"))

print(pm.export_to_html())
print('The end!')
