import CardLoyaltyBasic


class Basket(CardLoyaltyBasic.Basic):
    def __init__(self):
        super().__init__()
        self._basket = {}

    def add_item(self,
                 product_id: str,
                 name: str,
                 amount: int,
                 price: float,
                 discount_price: float,
                 group_id: str = "",
                 group_name: str = "",
                 ) -> bool:
        """
        Добавить позицию товара в корзину

        :param product_id: ID товара
        :param name: название товара
        :param amount: количество товара
        :param price: цена 1 единицы товара
        :param discount_price: цена 1 единицы товара со скидкой
        :param group_id: ID группы товара
        :param group_name: название группы товара

        :return: True / False
        """
        new_item = {
            "nid": product_id,
            "name": name,
            "amount": amount,
            "price": round(price, 2),
            "priceWithDiscount": round(discount_price, 2),
            "groupId": group_id,
            "groupName": group_name
        }
        if not self.is_item_in_basket(product_id) and amount > 0 \
                and price >= 0 and discount_price >= 0:
            self._basket.update({product_id: new_item})
            return True
        else:
            return False

    def delete_item(self, product_id: str) -> bool:
        """
        Удаляет позицию товара из корзины

        :param product_id: ID товара

        :return: True / False
        """
        if self.is_item_in_basket(product_id):
            self._basket.pop(product_id)
            return True
        else:
            return False

    def is_item_in_basket(self, product_id: str) -> bool:
        """
        Проверяет есть ли в корзине товар

        :param product_id: ID товара

        :return: True / False
        """
        return True if product_id in self._basket else False

    def get_basket(self) -> dict:
        """
        Получить корзину

        :return:
        Пример return:
        {
            "36ACB48C-438D-F241": {
                "nid": "36ACB48C-438D-F241",    # ID номенклатуры
                "groupId": "BEA57842-935",      # ID группы номенклатуры
                "groupName": "Стейки",          # наименование группы номенклатуры
                "name": "Мексика\/Чойс 240\/30гр",    # наименование номенклатуры
                "price": 1300,                  # стоимость номенклатуры
                "priceWithDiscount": 1300,      # стоимость номенклатуры с учетом скидки
            },
            "7882EAF6-B08E-1041-8B8B-8F4CEDDB3B80": {
                "amount": 1    # Количество
                "nid":"7882EAF6-B08E-1041-8B8B-8F4CEDDB3B80",
                "groupId":"F2FD3F09-96D6-9441-99E5-FF65505F6980",
                "groupName":"Салаты\/Закуски",
                "name":"Салат с розовыми помидорами и домашним сыром 270гр",
                "price":390,
                "priceWithDiscount":390,
            }
        }
        """
        return self._basket

    def get_basket_for_order(self) -> list:
        """
        Получить корзину в формате для создания заказа

        :return:
        Пример return:
        [
            {
                "nid": "36ACB48C-438D-F241",    # ID номенклатуры
                "groupId": "BEA57842-935",      # ID группы номенклатуры
                "groupName": "Стейки",          # наименование группы номенклатуры
                "name": "Мексика\/Чойс 240\/30гр",    # наименование номенклатуры
                "price": 1300,                  # стоимость номенклатуры
                "priceWithDiscount": 1300,      # стоимость номенклатуры с учетом скидки
            },
            {
                "amount": 1    # Количество
                "nid":"7882EAF6-B08E-1041-8B8B-8F4CEDDB3B80",
                "groupId":"F2FD3F09-96D6-9441-99E5-FF65505F6980",
                "groupName":"Салаты\/Закуски",
                "name":"Салат с розовыми помидорами и домашним сыром 270гр",
                "price":390,
                "priceWithDiscount":390,
            }
        ]
        """
        return list(map(lambda x: self._basket[x], self._basket))

    def get_basket_price(self) -> float:
        """
        Получить стоимость корзины

        :return: float
        """
        basket = self.get_basket_for_order()
        basket_price = 0.00
        for item in basket:
            basket_price += round(item["amount"] * item["price"], 2)

        return basket_price

    def get_basket_price_with_discount(self):
        """
        Получить стоимость корзины c учетом скидок

        :return: float
        """
        basket = self.get_basket_for_order()
        basket_price = 0.00
        for item in basket:
            basket_price += round(item["amount"] * item["priceWithDiscount"], 2)

        return basket_price

    def get_item_from_basket(self, product_id: str) -> dict:
        """
        Получить позицию товара в корзине

        :param product_id: ID товара

        :return:
        Пример return:
        {
            "nid": "36ACB48C-438D-F241",    # ID номенклатуры
            "groupId": "BEA57842-935",      # ID группы номенклатуры
            "groupName": "Стейки",          # наименование группы номенклатуры
            "name": "Мексика\/Чойс 240\/30гр",    # наименование номенклатуры
            "price": 1300,                  # стоимость номенклатуры
            "priceWithDiscount": 1300,      # стоимость номенклатуры с учетом скидки
        }
        """
        if self.is_item_in_basket(product_id):
            return self._basket.get(product_id)
        else:
            return {}

    def update_item_amount(self, product_id: str, new_amount: int) -> bool:
        """
        Обновить количество позиции товара в корзине

        :param product_id: ID товара
        :param new_amount: новое количество товара

        :return: True / False
        """
        if self.is_item_in_basket(product_id) and new_amount > 0:
            self._basket[product_id]["amount"] = new_amount
            return True
        else:
            return False

    def update_item_price(self, product_id: str, new_price: float) -> bool:
        """
        Обновить стоимость позиции товара в корзине

        :param product_id: ID товара
        :param new_price: новая стоимость товара

        :return: True / False
        """
        if self.is_item_in_basket(product_id) and new_price > 0:
            self._basket[product_id]["price"] = new_price
            return True
        else:
            return False

    def update_item_price_with_discount(self, product_id: str, new_price_with_discount: float) -> bool:
        """
        Обновить стоимость позиции товара с учетом скидки в корзине

        :param product_id: ID товара
        :param new_price_with_discount: новая стоимость товара с учетом скидки

        :return: True / False
        """
        if self.is_item_in_basket(product_id) and new_price_with_discount > 0:
            self._basket[product_id]["priceWithDiscount"] = new_price_with_discount
            return True
        else:
            return False
