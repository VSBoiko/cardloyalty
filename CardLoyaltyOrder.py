import json
from datetime import datetime

import CardLoyaltyBasic
import CardLoyaltyBasket


def dump(value):
    print((json.dumps(value, indent=4, sort_keys=True)))


class Order(CardLoyaltyBasic.Basic):
    def __init__(self,
                 guid: str,
                 number: str,
                 date: datetime,
                 basket: CardLoyaltyBasket.Basket,
                 bonus_add: float = 0.00,
                 bonus_write_off: float = 0.00,
                 deposit_add: float = 0.00,
                 deposit_write_off: float = 0.00,
                 ):
        super().__init__()
        self._order = {
            "guid": guid,    # ID транзакции
            "number": number,    # Номер транзакции
            "date": date.strftime("%Y-%m-%d %H:%M:%S"),    # Дата транзакции
            "sum": basket.get_basket_price(),    # Сумма транзакции без скидки
            "sumDiscount": basket.get_basket_price_with_discount(),    # Сумма транзакции со скидкой
            "bonusAdd": round(bonus_add, 2),    # Начислено бонусов
            "bonusWriteOff": round(bonus_write_off, 2),    # Списано бонусов
            "depositAdd": round(deposit_add, 2),    # Пополнение депозита
            "depositWriteOff": round(deposit_write_off, 2),    # Списание с депозита
            "cart": basket.get_basket_for_order()
        }

    def get_to_create_order(self) -> dict:
        """
        Возвращает данные заказа в формате для создания заказа

        :return:
        Пример return:
        Пример order:
        {
            "guid": "2-43F2-4148-A264-8787414DC88",    # ID транзакции
            "number": "005",    # Номер транзакции
            "date": "2020-02-18 18:18:18",    # Дата транзакции
            "sum": 1690,    # Сумма транзакции без скидки
            "sumDiscount": 1690,    # Сумма транзакции со скидкой
            "bonusAdd": "0",    # Начислено бонусов
            "bonusWriteOff": "20",    # Списано бонусов
            "depositAdd": "0",    # Пополнение депозита
            "depositWriteOff": "20",    # Списание с депозита
            "cart":
            [
                {
                    "nid": "36ACB48C-438D-F241",    # ID номенклатуры
                    "groupId": "BEA57842-935",    # ID группы номенклатуры
                    "groupName": "Стейки",    # Наименование группы номенклатуры
                    "name": "Мексика\/Чойс 240\/30гр",    # Наименование номенклатуры
                    "price": 1300,    # Стоимость номенклатуры
                    "priceWithDiscount": 1300,    # Стоимость номенклатуры с учетом скидки
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
        }
        """
        return self._order
