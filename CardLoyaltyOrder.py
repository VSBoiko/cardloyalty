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
            "guid": guid,    # ID ����������
            "number": number,    # ����� ����������
            "date": date.strftime("%Y-%m-%d %H:%M:%S"),    # ���� ����������
            "sum": basket.get_basket_price(),    # ����� ���������� ��� ������
            "sumDiscount": basket.get_basket_price_with_discount(),    # ����� ���������� �� �������
            "bonusAdd": round(bonus_add, 2),    # ��������� �������
            "bonusWriteOff": round(bonus_write_off, 2),    # ������� �������
            "depositAdd": round(deposit_add, 2),    # ���������� ��������
            "depositWriteOff": round(deposit_write_off, 2),    # �������� � ��������
            "cart": basket.get_basket_for_order()
        }

    def get_to_create_order(self) -> dict:
        """
        ���������� ������ ������ � ������� ��� �������� ������

        :return:
        ������ return:
        ������ order:
        {
            "guid": "2-43F2-4148-A264-8787414DC88",    # ID ����������
            "number": "005",    # ����� ����������
            "date": "2020-02-18 18:18:18",    # ���� ����������
            "sum": 1690,    # ����� ���������� ��� ������
            "sumDiscount": 1690,    # ����� ���������� �� �������
            "bonusAdd": "0",    # ��������� �������
            "bonusWriteOff": "20",    # ������� �������
            "depositAdd": "0",    # ���������� ��������
            "depositWriteOff": "20",    # �������� � ��������
            "cart":
            [
                {
                    "nid": "36ACB48C-438D-F241",    # ID ������������
                    "groupId": "BEA57842-935",    # ID ������ ������������
                    "groupName": "������",    # ������������ ������ ������������
                    "name": "�������\/���� 240\/30��",    # ������������ ������������
                    "price": 1300,    # ��������� ������������
                    "priceWithDiscount": 1300,    # ��������� ������������ � ������ ������
                },
                {
                    "amount": 1    # ����������
                    "nid":"7882EAF6-B08E-1041-8B8B-8F4CEDDB3B80",
                    "groupId":"F2FD3F09-96D6-9441-99E5-FF65505F6980",
                    "groupName":"������\/�������",
                    "name":"����� � �������� ���������� � �������� ����� 270��",
                    "price":390,
                    "priceWithDiscount":390,
                }
            ]
        }
        """
        return self._order
