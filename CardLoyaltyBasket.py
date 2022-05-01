import json

import CardLoyaltyBasic


def dump(value):
    print((json.dumps(value, indent=4, sort_keys=True)))



# "cart":
# [
#     {
#         "nid": "36ACB48C-438D-F241",    # ID номенклатуры
#         "groupId": "BEA57842-935",    # ID группы номенклатуры
#         "groupName": "Стейки",    # Наименование группы номенклатуры
#         "name": "Мексика\/Чойс 240\/30гр",    # Наименование номенклатуры
#         "price": 1300,    # Стоимость номенклатуры
#         "priceWithDiscount": 1300,    # Стоимость номенклатуры с учетом скидки
#     },
#     {
#         "amount": 1    # Количество
#         "nid":"7882EAF6-B08E-1041-8B8B-8F4CEDDB3B80",
#         "groupId":"F2FD3F09-96D6-9441-99E5-FF65505F6980",
#         "groupName":"Салаты\/Закуски",
#         "name":"Салат с розовыми помидорами и домашним сыром 270гр",
#         "price":390,
#         "priceWithDiscount":390,
#     }
# ]


class Basket(CardLoyaltyBasic.Basic):
    def __init__(self):
        super().__init__()
        self._basket = {}
        self._navigate = {}

    def add_item(self,
                 product_id: str,
                 name: str,
                 amount: int,
                 price: float,
                 discount_price: float,
                 group_id: str = "",
                 group_name: str = "",
                 ) -> bool:
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
        if self.is_item_in_basket(product_id):
            self._basket.pop(product_id)
            return True
        else:
            return False

    def is_item_in_basket(self, product_id: str) -> bool:
        return True if product_id in self._basket else False

    def get_basket(self):
        return self._basket

    def get_basket_for_order(self):
        return list(map(lambda x: self._basket[x], self._basket))

    def get_item_from_basket(self, product_id: str) -> dict:
        if self.is_item_in_basket(product_id):
            return self._basket.get(product_id)
        else:
            return {}

    def update_item_amount(self, product_id: str, new_amount: int) -> bool:
        if self.is_item_in_basket(product_id) and new_amount > 0:
            self._basket[product_id]["amount"] = new_amount
            return True
        else:
            return False

    def update_item_price(self, product_id: str, new_price: float) -> bool:
        if self.is_item_in_basket(product_id) and new_price > 0:
            self._basket[product_id]["price"] = new_price
            return True
        else:
            return False

    def update_item_price_with_discount(self, product_id: str, new_price_with_discount: float) -> bool:
        if self.is_item_in_basket(product_id) and new_price_with_discount > 0:
            self._basket[product_id]["priceWithDiscount"] = new_price_with_discount
            return True
        else:
            return False

    def get_basket_price(self):
        basket = self.get_basket_for_order()
        basket_price = 0.00
        for item in basket:
            basket_price += round(item["amount"] * item["price"], 2)

        return basket_price

    def get_basket_price_with_discount(self):
        basket = self.get_basket_for_order()
        basket_price = 0.00
        for item in basket:
            basket_price += round(item["amount"] * item["priceWithDiscount"], 2)

        return basket_price


b = Basket()
dump(b.get_basket_price())
dump(b.get_basket_price_with_discount())
b.add_item(
    product_id="111",
    name="Картошка",
    amount=5,
    price=10.0,
    discount_price=0.0,
)
b.add_item(
    product_id="22",
    name="Морковка",
    amount=2,
    price=15.17,
    discount_price=0.0,
)

dump(b.get_basket_for_order())
dump(b.get_basket_price())
dump(b.get_basket_price_with_discount())

