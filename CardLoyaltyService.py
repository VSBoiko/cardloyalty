import json

import CardLoyaltyBasic


def dump(value):
    print((json.dumps(value, indent=4, sort_keys=True)))


class Service(CardLoyaltyBasic.Basic):
    def __init__(self):
        super().__init__()

    def add_tag(self, tag_name: str) -> dict:
        """
        ������� ���

        :param tag_name: �������� ����

        :return:
        ������ return:
        {
            "name": "����������",    # ������������ ����
            "id": "2",    # id ����
            "status": "exists"    # exists � ��� ����������, new � ��� ������
        }
        """
        return self._create_tags(
            tag_names=[tag_name]
        )

    def get_all_tags(self) -> list:
        """
        �������� ������ �����

        :return:
        ������ return:
        [
            {
                "tagId": 123,   # ID ���a
                "tagName": "������"   # ������������ ����
            },
            {
                "tagId": 124,
                "tagName": "VIP"
            }
        ]
        """
        tags = self._get_tags()
        if "tags" in tags:
            return tags.get("tags")
        else:
            return []

    def get_all_templates(self) -> dict:
        """
        �������� ������ �������

        :return:
        ������ return:
        {
            "id": "4",    # ID ������
            "name": "������ 5%"    # ������������ ������
        },
        {
            "id": "16",
            "name": "������ 10%"
        },
        {
            "id": "18",
            "name": "�������� �����"
        }
        """
        return self._get_templates()

    def get_tag_name(self, tag_id: int) -> str:
        """
        �������� ������������ ����

        :param tag_id: ID ����

        :return:
        ������ return: "������ -10%"
        """
        tag = self._get_tag(tag_id)
        if "tagName" in tag:
            return tag.get("tagName")
        else:
            return ""

    def send_sms(self, client_id: int, message: str, unix_time: str) -> bool:
        """
        ��������� SMS

        :param client_id: ID ������� � CARDLOYALTY, ����� �������� ����� ��������� �� SMS
        :param message: ����� SMS ���������, ��� %LINK% - ������ �� ����
        :param unix_time: ����� �������� � ������� Unixtime (��������, 1543415640)

        :return:
        ������ return:
        {
            "response": ok
        }
        """
        data = {
            "clientId": client_id,
            "message": message,
            "time": unix_time,
        }
        result = self._send_request(
            method="post",
            url=f"{self.api}/sendCardSMS",
            headers=self.headers,
            params=dict(),
            data=data
        )

        if "response" in result and result.get("response") == "ok":
            return True
        else:
            return False

    def update_vars(self, client_id: int, variables: dict):
        """
        ���������� ���������x

        :param client_id: ID �������
        :param variables: ������ ���������� (����� 15 - �� var1 �� var15)
        ������ variables:
        {
            "var1": "100 ������",    # ���������� (����� 15)
            "var2": "10%",
            "var3": "����� ��������� � ����������",
            "var4": "",
            "var5": "",
            "var6": "",
            "var7": "",
            "var8": "",
            "var9": "",
            "var10": "",
            "var11": "",
            "var12": "",
            "var13": "",
            "var14": "",
            "var15": ""
        }

        :return:
        ������ return:
        {
            "response": ok
        }
        """
        return self._update_vars(client_id, variables)
