import CardLoyaltyBasic


class Service(CardLoyaltyBasic.Basic):
    def __init__(self):
        super().__init__()

    def add_tag(self, tag_name: str) -> dict:
        """
        Создать тег

        :param tag_name: название тега

        :return:
        Пример return:
        {
            "name": "Пушкинская",    # наименование тега
            "id": "2",    # id тега
            "status": "exists"    # exists – тег существует, new – тег создан
        }
        """
        return self._create_tags(
            tag_names=[tag_name]
        )

    def get_all_tags(self) -> list:
        """
        Получить список тегов

        :return:
        Пример return:
        [
            {
                "tagId": 123,   # ID тегa
                "tagName": "Москва"   # наименование тега
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
        Получить список макетов

        :return:
        Пример return:
        {
            "id": "4",    # ID Макета
            "name": "Скидка 5%"    # Наименование макета
        },
        {
            "id": "16",
            "name": "Скидка 10%"
        },
        {
            "id": "18",
            "name": "Бонусный макет"
        }
        """
        return self._get_templates()

    def get_tag_name(self, tag_id: int) -> str:
        """
        Получить наименование тега

        :param tag_id: ID тега

        :return:
        Пример return: "Москва -10%"
        """
        tag = self._get_tag(tag_id)
        if "tagName" in tag:
            return tag.get("tagName")
        else:
            return ""

    def send_sms(self, client_id: int, message: str, unix_time: str) -> bool:
        """
        Отправить SMS

        :param client_id: ID клиента в CARDLOYALTY, карту которого нужно отправить по SMS
        :param message: текст SMS сообщения, где %LINK% - ссылка на карт
        :param unix_time: время отправки в формате Unixtime (например, 1543415640)

        :return:
        Пример return:
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
        Обновление переменныx

        :param client_id: ID клиента
        :param variables: список переменных (всего 15 - от var1 до var15)
        Пример variables:
        {
            "var1": "100 рублей",    # Переменная (всего 15)
            "var2": "10%",
            "var3": "Текст выводимый в переменную",
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
        Пример return:
        {
            "response": ok
        }
        """
        return self._update_vars(client_id, variables)
