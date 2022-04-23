import requests

from settings import TOKEN


class CardLoyaltySDK:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    api = "https://app.cardloyalty.ru/api/v2"

    def __init__(self):
        self.request_data = {
            "token": TOKEN
        }

    def _send_request(self, method: str, url: str, headers: dict, params: dict,
                      data: dict):
        params.update(self.request_data)
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=data
        )
        return self.__validate(response=response, params=params)

    def ping(self) -> dict:
        """
        Проверка токена

        :return:
        Пример return:
        {
            "response":
            {
                "status": "1",    # 1 – Токен валидный
                "message": "Token ok"    # Сообщение
            }
        }
        """
        return self._send_request(
            method="get",
            url=f"{self.api}/ping",
            headers=self.headers,
            params=dict(),
            data=dict()
        )

    def add_organisation(self, organisation: dict) -> dict:
        """
        Регистрация организации

        :param organisation: данныне об организации
        Пример organisation
        {
            "organisationId": "6v8-y4hsjg-n45try",    # Идентификатор организации (Магазина, ресторана)
            "organisationName": "Василек",    # Наименование организации (Магазина, ресторана)
            "versionPlugin": "8.0 ",    # Версия интеграции
            "integrationSoftName": "1C:Розница",    # Наименование ПО с которым проводится интеграции
            "versionIntegrationSoft": "8.6.3 "    # Версия ПО, с которым проводится интеграции
        }

        :return:
        """
        return self._send_request(
            method="post",
            url=f"{self.api}/updateRegistrationOrganisation",
            headers=self.headers,
            params=dict(),
            data=organisation
        )

    def get_templates(self) -> dict:
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
        return self._send_request(
            method="get",
            url=f"{self.api}/getTemplates",
            headers=self.headers,
            params=dict(),
            data=dict()
        )

    def get_client_info(self, type: str, id: str) -> dict:
        """
        Получить информацию по клиенту

        :param type: параметр транзакции. Возможные значения:
                clientId – ID клиента
                cardBarcode – Токен/Баркод карты
                cardNumber – Номер карты
                phone – Телефон
        :param id: значение поля, указанного в type

        :return:
        Пример return:
        {
            "clientId": 1234,    # ID клиента
            "templateId": 123,    # ID макета
            "cardNumber": "1234",    # Номер карты
            "cardBarcode": "dld123s",    # Токен/трек номер карты – только латиницы и цифры
            "phone": "79777121350",    # Телефон
            "lastName": " Чехов",    # Фамилия
            "firstName": "Антон",    # Имя
            "patronymic": "Павлович",    # Отчество
            "email": "mail@mail.ru",    # E-mail
            "sex": 1,    # 1 – мужской, 2 – женский, 0 – не определен
            "birthday": "2018-01-01",    # Дата рождения
            "templateName": "Скидка 5%",    # Наименование макета
            "comment": "Жадный на чаевые",    # Произвольный комментарий к клиенту
            "tags": [123, 124],    # ID тегов
            "bonusBalance": "125.00",    # Бонусный баланс клиента
            "maxPercentBonusWriteOff": "10",    # Максимальный процент оплаты бонусами
            "depositBalance": "10.00",    # Депозитный баланс клиента
            "sumAllDisсount": "1200.00"    # Сумма всех визитов с учетом скидок
        }
        """
        params = {
            "type": type,
            "id": id
        }
        return self._send_request(
            method="get",
            url=f"{self.api}/clientInfo",
            headers=self.headers,
            params=params,
            data=dict()
        )

    def get_client_info_by_client_id(self, client_id: int) -> dict:
        """
        Получить информацию по клиенту по ID клиента

        :param client_id: ID клиента

        :return:
        Пример return:
        {
            "clientId": 1234,    # ID клиента
            "templateId": 123,    # ID макета
            "cardNumber": "1234",    # Номер карты
            "cardBarcode": "dld123s",    # Токен/трек номер карты – только латиницы и цифры
            "phone": "79777121350",    # Телефон
            "lastName": " Чехов",    # Фамилия
            "firstName": "Антон",    # Имя
            "patronymic": "Павлович",    # Отчество
            "email": "mail@mail.ru",    # E-mail
            "sex": 1,    # 1 – мужской, 2 – женский, 0 – не определен
            "birthday": "2018-01-01",    # Дата рождения
            "templateName": "Скидка 5%",    # Наименование макета
            "comment": "Жадный на чаевые",    # Произвольный комментарий к клиенту
            "tags": [123, 124],    # ID тегов
            "bonusBalance": "125.00",    # Бонусный баланс клиента
            "maxPercentBonusWriteOff": "10",    # Максимальный процент оплаты бонусами
            "depositBalance": "10.00",    # Депозитный баланс клиента
            "sumAllDisсount": "1200.00"    # Сумма всех визитов с учетом скидок
        }
        """
        return self.get_client_info(
            type="clientId",
            id=str(client_id)
        )

    def get_client_info_by_card_barcode(self, card_barcode: str) -> dict:
        """
        Получить информацию по клиенту по токену / баркоду карты

        :param card_barcode: токен / баркод карты

        :return:
        Пример return:
        {
            "clientId": 1234,    # ID клиента
            "templateId": 123,    # ID макета
            "cardNumber": "1234",    # Номер карты
            "cardBarcode": "dld123s",    # Токен/трек номер карты – только латиницы и цифры
            "phone": "79777121350",    # Телефон
            "lastName": " Чехов",    # Фамилия
            "firstName": "Антон",    # Имя
            "patronymic": "Павлович",    # Отчество
            "email": "mail@mail.ru",    # E-mail
            "sex": 1,    # 1 – мужской, 2 – женский, 0 – не определен
            "birthday": "2018-01-01",    # Дата рождения
            "templateName": "Скидка 5%",    # Наименование макета
            "comment": "Жадный на чаевые",    # Произвольный комментарий к клиенту
            "tags": [123, 124],    # ID тегов
            "bonusBalance": "125.00",    # Бонусный баланс клиента
            "maxPercentBonusWriteOff": "10",    # Максимальный процент оплаты бонусами
            "depositBalance": "10.00",    # Депозитный баланс клиента
            "sumAllDisсount": "1200.00"    # Сумма всех визитов с учетом скидок
        }
        """
        return self.get_client_info(
            type="cardBarcode",
            id=card_barcode
        )

    def get_client_info_by_card_number(self, card_number: str) -> dict:
        """
        Получить информацию по клиенту по номеру карты

        :param card_number: номер карты

        :return:
        Пример return:
        {
            "clientId": 1234,    # ID клиента
            "templateId": 123,    # ID макета
            "cardNumber": "1234",    # Номер карты
            "cardBarcode": "dld123s",    # Токен/трек номер карты – только латиницы и цифры
            "phone": "79777121350",    # Телефон
            "lastName": " Чехов",    # Фамилия
            "firstName": "Антон",    # Имя
            "patronymic": "Павлович",    # Отчество
            "email": "mail@mail.ru",    # E-mail
            "sex": 1,    # 1 – мужской, 2 – женский, 0 – не определен
            "birthday": "2018-01-01",    # Дата рождения
            "templateName": "Скидка 5%",    # Наименование макета
            "comment": "Жадный на чаевые",    # Произвольный комментарий к клиенту
            "tags": [123, 124],    # ID тегов
            "bonusBalance": "125.00",    # Бонусный баланс клиента
            "maxPercentBonusWriteOff": "10",    # Максимальный процент оплаты бонусами
            "depositBalance": "10.00",    # Депозитный баланс клиента
            "sumAllDisсount": "1200.00"    # Сумма всех визитов с учетом скидок
        }
        """
        return self.get_client_info(
            type="cardNumber",
            id=card_number
        )

    def get_client_info_by_phone(self, phone: str) -> dict:
        """
        Получить информацию по клиенту по телефону

        :param phone: телефон

        :return:
        Пример return:
        {
            "clientId": 1234,    # ID клиента
            "templateId": 123,    # ID макета
            "cardNumber": "1234",    # Номер карты
            "cardBarcode": "dld123s",    # Токен/трек номер карты – только латиницы и цифры
            "phone": "79777121350",    # Телефон
            "lastName": " Чехов",    # Фамилия
            "firstName": "Антон",    # Имя
            "patronymic": "Павлович",    # Отчество
            "email": "mail@mail.ru",    # E-mail
            "sex": 1,    # 1 – мужской, 2 – женский, 0 – не определен
            "birthday": "2018-01-01",    # Дата рождения
            "templateName": "Скидка 5%",    # Наименование макета
            "comment": "Жадный на чаевые",    # Произвольный комментарий к клиенту
            "tags": [123, 124],    # ID тегов
            "bonusBalance": "125.00",    # Бонусный баланс клиента
            "maxPercentBonusWriteOff": "10",    # Максимальный процент оплаты бонусами
            "depositBalance": "10.00",    # Депозитный баланс клиента
            "sumAllDisсount": "1200.00"    # Сумма всех визитов с учетом скидок
        }
        """
        return self.get_client_info(
            type="phone",
            id=phone
        )

    def get_tags(self) -> dict:
        """
        Получить список тегов

        :return:
        Пример return:
        {
            "tags":
            [
                {
                    "tagId": 123,   # ID тегов
                    "tagName": "Москва"   # Наименование тега
                },
                {
                    "tagId": 124,
                    "tagName": "VIP"
                }
            ]
        }
        """
        return self._send_request(
            method="get",
            url=f"{self.api}/getTags",
            headers=self.headers,
            params=dict(),
            data=dict()
        )

    def get_tag(self, tag_id: int) -> dict:
        """
        Получить наименование тега

        :param tag_id: ID тега

        :return:
        Пример return
        {
            "tagName": "Москва"    # Наименование тега
        }
        """
        params = {
            "id": tag_id
        }
        return self._send_request(
            method="get",
            url=f"{self.api}/getTag",
            headers=self.headers,
            params=params,
            data=dict()
        )

    def get_clients_all(self, limit: int = 100, offset: int = 0) -> dict:
        """
        Получить всех клиентов

        :param limit: по сколько клиентов возвращать
        :param offset: смещение

        :return:
        Пример return:
        {
            "clients":
            [
                {
                    "clientId": 1234,    # ID клиента
                    "hash": "7e95e3b4b3",    # Ссылка на карту
                    "status": 1,    # 0 – создана, 1 – активна, 2 – удалена
                    "lastName": " Чехов",    # Фамилия
                    "firstName": "Антон ",    # Имя
                    "patronymic": "Павлович",    # Отчество
                    "phone": "79777121350",    # Телефон
                    "email": "mail@mail.ru",    # E-mail
                    "sex": 1,    # 1 – мужской, 2 – женский, 0 – не определен
                    "birthday": "2018-01-01",    # Дата рождения
                    "templateId": 123,    # ID макета
                    "cardNumber": "1234",    # Номер карты
                    "cardBarcode": "dld123s",    # Токен/Баркод – только латиницы и цифры
                    "comment": "Жадный на чаевые",    # Произвольный комментарий к клиенту
                    "tags": [123, 124]    # Идентификаторы тегов
                },
                {
                    "clientId": 1235,
                    "hash": "7e95e3b4b3d12672c15846632421",
                    "status": 1,
                    "lastName": "Пушкин",
                    "firstName": "Александр",
                    "patronymic": "Сергеевич",
                    "phone": "79777121351",
                    "email": "mail@mail.ru",
                    "sex": 1,
                    "birthday": "2019-01-01",
                    "templateId": 123,
                    "cardNumber": "1235",
                    "cardBarcode": "dld223s",
                    "comment": "Жадный на чаевые",
                    "tags": [123, 124]
                }
            ]
        }

        Если клиентов нет:
        {
            "clients": NULL
        }
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        return self._send_request(
            method="get",
            url=f"{self.api}/getAllClients",
            headers=self.headers,
            params=params,
            data=dict()
        )

    def get_clients_new(self, limit: int = 100) -> dict:
        """
        Получить только новых клиентов

        :param limit: по сколько клиентов возвращать

        :return:
        Пример return:
        {
            "clients":
            [
                {
                    "clientId": 1234,    # ID клиента
                    "hash": "7e95e3b4b3",    # Ссылка на карту
                    "status": 1,    # 0 – создана, 1 – активна, 2 – удалена
                    "lastName": " Чехов",    # Фамилия
                    "firstName": "Антон ",    # Имя
                    "patronymic": "Павлович",    # Отчество
                    "phone": "79777121350",    # Телефон
                    "email": "mail@mail.ru",    # E-mail
                    "sex": 1,    # 1 – мужской, 2 – женский, 0 – не определен
                    "birthday": "2018-01-01",    # Дата рождения
                    "templateId": 123,    # ID макета
                    "cardNumber": "1234",    # Номер карты
                    "cardBarcode": "dld123s",    # Токен/Баркод – только латиницы и цифры
                    "comment": "Жадный на чаевые",    # Произвольный комментарий к клиенту
                    "tags": [123, 124]    # Идентификаторы тегов
                },
                {
                    "clientId": 1235,
                    "hash": "7e95e3b4b3d12672c15846632421",
                    "status": 1,
                    "lastName": "Пушкин",
                    "firstName": "Александр",
                    "patronymic": "Сергеевич",
                    "phone": "79777121351",
                    "email": "mail@mail.ru",
                    "sex": 1,
                    "birthday": "2019-01-01",
                    "templateId": 123,
                    "cardNumber": "1235",
                    "cardBarcode": "dld223s",
                    "comment": "Жадный на чаевые",
                    "tags": [123, 124]
                }
            ]
        }

        Если клиентов нет:
        {
            "clients": NULL
        }
        """
        params = {
            "limit": limit
        }
        return self._send_request(
            method="get",
            url=f"{self.api}/getNewClients",
            headers=self.headers,
            params=params,
            data=dict()
        )

    def create_client(self, client: dict) -> dict:
        """
        Создать клиента

        :param client: клиент
        Пример client:
        {
            "lastName": "Чехов",    # Фамилия
            "firstName": "Антон ",    # Имя
            "patronymic": "Павлович",    # Отчество
            "phone": "79777121350",    # Телефон (Обязательное и уникальное)
            "email": "mail@mail.ru",    # E-mail
            "sex": 1,    # 1 – мужской, 2 – женский, 0 – не определен
            "birthday": "2018-01-01",    # Дата рождения
            "templateId": 123,    # ID макета
            "cardNumber": "1234",    # Номер карты (Уникальный)
            "cardBarcode": "dld123s",    # Токен/Баркод – только латиницы и цифры
            "comment": "Жадный на чаевые",    # Произвольный комментарий к клиенту
            "tags": [123, 124]    # ID тегов
        }

        :return:
        Пример return:
        {
            "response":
            [
                {
                    "clientId": 4321,    # ID клиента
                    "phone": "79777121350",    # Телефон
                    "cardNumber": "1234",    # Номер карты
                    "cardBarcode": "dld123s",    # Токен/Баркод
                    "hash": "q386v8y4hsjgn45y8ehy45try"    # hash карты
                }
            ]
        }

        Пример return в случае ошибки:
        {
            "error":
            [
                {
                "phone": "79777121350",    # Телефон
                "cardNumber": "1234",    # Номер карты
                "cardBarcode": "dld123s",    # Токен/Баркод
                "errorId": 702,    # Код ошибки
                "message": "invalid ..."    # Сообщение
                }
            ]
        }
        """
        return self.create_clients(
            clients=[client]
        )

    def create_clients(self, clients: list) -> dict:
        """
        Создать клиентов

        :param clients: список клиентов
        Пример clients:
        [
            {
                "lastName": "Чехов",    # Фамилия
                "firstName": "Антон ",    # Имя
                "patronymic": "Павлович",    # Отчество
                "phone": "79777121350",    # Телефон (Обязательное и уникальное)
                "email": "mail@mail.ru",    # E-mail
                "sex": 1,    # 1 – мужской, 2 – женский, 0 – не определен
                "birthday": "2018-01-01",    # Дата рождения
                "templateId": 123,    # ID макета
                "cardNumber": "1234",    # Номер карты (Уникальный)
                "cardBarcode": "dld123s",    # Токен/Баркод – только латиницы и цифры
                "comment": "Жадный на чаевые",    # Произвольный комментарий к клиенту
                "tags": [123, 124]    # ID тегов
            },
            {
                "lastName": "Пушкин",
                "firstName": "Александр",
                "patronymic": "Сергеевич",
                "phone": "79999999991",
                "email": "mail@mail.ru",
                "sex": 1,
                "birthday": "2018-01-01",
                "templateId": 124,
                "cardNumber": "1235",
                "cardBarcode": "dld123s1",
                "comment": "Жадный на чаевые",
                "tags": [123, 124]
            }
        ]

        :return:
        Пример return:
        {
            "response":
            [
                {
                    "clientId": 4321,    # ID клиента
                    "phone": "79777121350",    # Телефон
                    "cardNumber": "1234",    # Номер карты
                    "cardBarcode": "dld123s",    # Токен/Баркод
                    "hash": "q386v8y4hsjgn45y8ehy45try"    # hash карты
                },
                {
                    "clientId": 4321,
                    "phone": "79999999991",
                    "cardNumber": "1235",
                    "cardBarcode": "dld123s1",
                    "hash": "ivhp495hhdighw9595ig984df"
                }
            ],
            "error":
            [
                {
                "phone": "79777121350",    # Телефон
                "cardNumber": "1234",    # Номер карты
                "cardBarcode": "dld123s",    # Токен/Баркод
                "errorId": 702,    # Код ошибки
                "message": "invalid ..."    # Сообщение
                }
            ]
        }
        """
        data = {
            "clients": clients
        }
        return self._send_request(
            method="post",
            url=f"{self.api}/createClients",
            headers=self.headers,
            params=dict(),
            data=data
        )

    def create_tag(self, tag_name: str) -> dict:
        """
        Создать тег

        :param tag_name: название тега

        :return:
        Пример return:
        [
            {
                "name": "Пушкинская",    # наименование тега
                "id": "2",    # id тега
                "status": "exists"    # exists – тег существует, new – тег создан
            }
        ]
        """
        return self.create_tags(
            tag_names=[tag_name]
        )

    def create_tags(self, tag_names: list) -> dict:
        """
        Создать теги

        :param tag_names: список названий тегов
        Пример tag_names:
        [
            "Пушкинская",    # наименование тега
            "Веган",
            "VIP
        }

        :return:
        Пример return:
        [
            {
                "name": "Пушкинская",    # наименование тега
                "id": "2",    # id тега
                "status": "exists"    # exists – тег существует, new – тег создан
            },
            {
                "name": "Веган",
                "id": "1837",
                "status": "new"
            },
            {
                "name": "VIP",
                "id": "1838",
                "status": "new"
            }
        ]
        """
        data = {
            "tags": tag_names
        }
        return self._send_request(
            method="post",
            url=f"{self.api}/createTags",
            headers=self.headers,
            params=dict(),
            data=data
        )

    def update_clients(self, clients: list) -> dict:
        """
        Обновить клиентов

        :param clients: список клиентов
        Пример clients:
        {
            "clients":
            [
                {
                    "clientId": 1234,    # ID клиента
                    "lastName": " Чехов",    # Фамилия (Обязательное)
                    "firstName": "Антон ",    # Имя
                    "patronymic": "Павлович",    # Отчество
                    "phone": "79777121350",    # Телефон (Обязательное и уникальное)
                    "email": "mail@mail.ru",    # E-mail
                    "sex": 1,    # 1 – мужской, 2 – женский, 0 – не определен
                    "birthday": "2018-01-01",    # Дата рождения
                    "templateId": 123,    # ID макета
                    "cardNumber": "1234",    # Номер карты (Уникальный)
                    "cardBarcode": "dld123s",    # Токен/Баркод – только латиницы и цифры
                    "comment": "Жадный на чаевые",    # Произвольный комментарий к клиенту
                    "tags": [123, 124]    # ID тегов
                },
                {
                    "clientId": 1235,
                    "lastName": "Пушкин",
                    "firstName": "Александр",
                    "patronymic": "Сергеевич",
                    "phone": "79999999991",
                    "email": "mail@mail.ru",
                    "sex": 1,
                    "birthday": "2018-01-01",
                    "templateId": 124,
                    "cardNumber": "1235",
                    "cardBarcode": "dld123s1",
                    "comment": "Жадный на чаевые",
                    "tags": [123, 124]
                }
            ]
        }

        :return:
        Пример return:
        {
            "response":
            [
                {
                    "clientId": 1234,    # ID успешно обработанного клиента
                    "phone": "79777121350",    # Номер телефона клиента
                    "cardNumber": "11234",    # Номер карты
                    "cardBarcode": "rr-34566"    # Токен/Баркод – только латиницы и цифры
                },
                {
                    "clientId": 1235,
                    "phone": "79999999991",
                    "cardNumber": "11654",
                    "cardBarcode": "rr-34556"
                }
            ],
            "error":
            [
                {
                    "сlientId": 431,    # ID не успешно обработанного клиента
                    "errorId": 12,    # Код ошибки
                    "message": "invalid phone number"    # Сообщение
                }
            ]
        }
        """
        data = {
            "clients": clients
        }
        return self._send_request(
            method="post",
            url=f"{self.api}/updateClients",
            headers=self.headers,
            params=dict(),
            data=data
        )

    def update_client(self, client: dict) -> dict:
        """
        Обновить клиента

        :param client: данные клиента
        Пример client:
        {
            "clientId": 1234,    # ID клиента
            "lastName": " Чехов",    # Фамилия (Обязательное)
            "firstName": "Антон ",    # Имя
            "patronymic": "Павлович",    # Отчество
            "phone": "79777121350",    # Телефон (Обязательное и уникальное)
            "email": "mail@mail.ru",    # E-mail
            "sex": 1,    # 1 – мужской, 2 – женский, 0 – не определен
            "birthday": "2018-01-01",    # Дата рождения
            "templateId": 123,    # ID макета
            "cardNumber": "1234",    # Номер карты (Уникальный)
            "cardBarcode": "dld123s",    # Токен/Баркод – только латиницы и цифры
            "comment": "Жадный на чаевые",    # Произвольный комментарий к клиенту
            "tags": [123, 124]    # ID тегов
        }

        :return:
        Пример return:
        {
            "response":
            [
                {
                    "clientId": 1234,    # ID успешно обработанного клиента
                    "phone": "79777121350",    # Номер телефона клиента
                    "cardNumber": "11234",    # Номер карты
                    "cardBarcode": "rr-34566"    # Токен/Баркод – только латиницы и цифры
                }
            ]
        }

        Пример return в случае ошибки:
        {
            "error":
            [
                {
                    "сlientId": 431,    # ID не успешно обработанного клиента
                    "errorId": 12,    # Код ошибки
                    "message": "invalid phone number"    # Сообщение
                }
            ]
        }
        """
        data = {
            "clients": [client]
        }
        return self._send_request(
            method="post",
            url=f"{self.api}/updateClients",
            headers=self.headers,
            params=dict(),
            data=data
        )

    def create_order(self, type: str, id: str, order: dict) -> dict:
        """
        Создать заказ (записать транзакцию)

        :param type: параметр транзакции. Возможные значения:
                clientId – ID клиента
                cardBarcode – Токен/Баркод карты
                cardNumber – Номер карты
                phone – Телефон
        :param id: значение поля, указанного в type
        :param order: параметры заказа
        Пример order:
        {
            "guid": "123",    # ID транзакции
            "number": "213",    # Номер транзакции
            "date": "2018-01-01 00:00:00",    # Дата транзакции
            "sum": 1200.00,    # Сумма транзакции без скидки
            "sumDiscount": 1100.00,    # Сумма транзакции со скидкой
            "bonusAdd": 200.00,    # Начислено бонусов
            "bonusWriteOff": 200.00,    # Списано бонусов
            "depositAdd": 0.00,    # Пополнение депозита
            "depositWriteOff": 0.00,    # Списание с депозита
            "cart":
            [
                {
                    "nid": "123",    # ID номенклатуры
                    "groupId": "145",    # ID группы номенклатуры
                    "groupName": "Печенье",    # Наименование группы номенклатуры
                    "name": "Печенька",    # Наименование номенклатуры
                    "price": 100.00,    # Стоимость номенклатуры
                    "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
                    "amount": 1.0    # Количество
                },
                {
                    "nid": "124",
                    "groupId": "145",
                    "groupName": "Мороженное",
                    "name": "Мороженка",
                    "price": 900.00,
                    "priceWithDiscount": 900.00,
                    "amount": 0.51
                }
            ]
        }

        :return:
        Пример return:
        {
            "response":
            {
                "guid": "123"    # id транзакции
            }
        }
        """
        params = {
            "type": type,
            "id": id
        }
        return self._send_request(
            method="post",
            url=f"{self.api}/createOrder",
            headers=self.headers,
            params=params,
            data=order
        )

    def create_oder_by_client_id(self, client_id: int, order: dict) -> dict:
        """
        Создать заказ по ID клиента

        :param client_id: ID клиента
        :param order: параметры заказа
        Пример order:
        {
            "guid": "123",    # ID транзакции
            "number": "213",    # Номер транзакции
            "date": "2018-01-01 00:00:00",    # Дата транзакции
            "sum": 1200.00,    # Сумма транзакции без скидки
            "sumDiscount": 1100.00,    # Сумма транзакции со скидкой
            "bonusAdd": 200.00,    # Начислено бонусов
            "bonusWriteOff": 200.00,    # Списано бонусов
            "depositAdd": 0.00,    # Пополнение депозита
            "depositWriteOff": 0.00,    # Списание с депозита
            "cart":
            [
                {
                    "nid": "123",    # ID номенклатуры
                    "groupId": "145",    # ID группы номенклатуры
                    "groupName": "Печенье",    # Наименование группы номенклатуры
                    "name": "Печенька",    # Наименование номенклатуры
                    "price": 100.00,    # Стоимость номенклатуры
                    "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
                    "amount": 1.0    # Количество
                },
                {
                    "nid": "124",
                    "groupId": "145",
                    "groupName": "Мороженное",
                    "name": "Мороженка",
                    "price": 900.00,
                    "priceWithDiscount": 900.00,
                    "amount": 0.51
                }
            ]
        }

        :return:
        Пример return:
        {
            "response":
            {
                "guid": "123"    # id транзакции
            }
        }
        """
        return self.create_order(
            type="clientId",
            id=str(client_id),
            order=order
        )

    def create_oder_by_card_barcode(self, card_barcode: str, order: dict) -> dict:
        """
        Создать заказ по токену / баркоду карты

        :param card_barcode: токен / баркод карты
        :param order: параметры заказа
        Пример order:
        {
            "guid": "123",    # ID транзакции
            "number": "213",    # Номер транзакции
            "date": "2018-01-01 00:00:00",    # Дата транзакции
            "sum": 1200.00,    # Сумма транзакции без скидки
            "sumDiscount": 1100.00,    # Сумма транзакции со скидкой
            "bonusAdd": 200.00,    # Начислено бонусов
            "bonusWriteOff": 200.00,    # Списано бонусов
            "depositAdd": 0.00,    # Пополнение депозита
            "depositWriteOff": 0.00,    # Списание с депозита
            "cart":
            [
                {
                    "nid": "123",    # ID номенклатуры
                    "groupId": "145",    # ID группы номенклатуры
                    "groupName": "Печенье",    # Наименование группы номенклатуры
                    "name": "Печенька",    # Наименование номенклатуры
                    "price": 100.00,    # Стоимость номенклатуры
                    "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
                    "amount": 1.0    # Количество
                },
                {
                    "nid": "124",
                    "groupId": "145",
                    "groupName": "Мороженное",
                    "name": "Мороженка",
                    "price": 900.00,
                    "priceWithDiscount": 900.00,
                    "amount": 0.51
                }
            ]
        }

        :return:
        Пример return:
        {
            "response":
            {
                "guid": "123"    # id транзакции
            }
        }
        """
        return self.create_order(
            type="cardBarcode",
            id=card_barcode,
            order=order
        )

    def create_oder_by_card_number(self, card_number: str, order: dict) -> dict:
        """
        Создать заказ по номеру карты

        :param card_number: номер карты
        :param order: параметры заказа
        Пример order:
        {
            "guid": "123",    # ID транзакции
            "number": "213",    # Номер транзакции
            "date": "2018-01-01 00:00:00",    # Дата транзакции
            "sum": 1200.00,    # Сумма транзакции без скидки
            "sumDiscount": 1100.00,    # Сумма транзакции со скидкой
            "bonusAdd": 200.00,    # Начислено бонусов
            "bonusWriteOff": 200.00,    # Списано бонусов
            "depositAdd": 0.00,    # Пополнение депозита
            "depositWriteOff": 0.00,    # Списание с депозита
            "cart":
            [
                {
                    "nid": "123",    # ID номенклатуры
                    "groupId": "145",    # ID группы номенклатуры
                    "groupName": "Печенье",    # Наименование группы номенклатуры
                    "name": "Печенька",    # Наименование номенклатуры
                    "price": 100.00,    # Стоимость номенклатуры
                    "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
                    "amount": 1.0    # Количество
                },
                {
                    "nid": "124",
                    "groupId": "145",
                    "groupName": "Мороженное",
                    "name": "Мороженка",
                    "price": 900.00,
                    "priceWithDiscount": 900.00,
                    "amount": 0.51
                }
            ]
        }

        :return:
        Пример return:
        {
            "response":
            {
                "guid": "123"    # id транзакции
            }
        }
        """
        return self.create_order(
            type="cardNumber",
            id=card_number,
            order=order
        )

    def create_oder_by_phone(self, phone: str, order: dict) -> dict:
        """
        Создать заказ по телефону

        :param phone: номер телефона
        :param order: параметры заказа
        Пример order:
        {
            "guid": "123",    # ID транзакции
            "number": "213",    # Номер транзакции
            "date": "2018-01-01 00:00:00",    # Дата транзакции
            "sum": 1200.00,    # Сумма транзакции без скидки
            "sumDiscount": 1100.00,    # Сумма транзакции со скидкой
            "bonusAdd": 200.00,    # Начислено бонусов
            "bonusWriteOff": 200.00,    # Списано бонусов
            "depositAdd": 0.00,    # Пополнение депозита
            "depositWriteOff": 0.00,    # Списание с депозита
            "cart":
            [
                {
                    "nid": "123",    # ID номенклатуры
                    "groupId": "145",    # ID группы номенклатуры
                    "groupName": "Печенье",    # Наименование группы номенклатуры
                    "name": "Печенька",    # Наименование номенклатуры
                    "price": 100.00,    # Стоимость номенклатуры
                    "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
                    "amount": 1.0    # Количество
                },
                {
                    "nid": "124",
                    "groupId": "145",
                    "groupName": "Мороженное",
                    "name": "Мороженка",
                    "price": 900.00,
                    "priceWithDiscount": 900.00,
                    "amount": 0.51
                }
            ]
        }

        :return:
        Пример return:
        {
            "response":
            {
                "guid": "123"    # id транзакции
            }
        }
        """
        return self.create_order(
            type="phone",
            id=phone,
            order=order
        )

    def update_order(self, type: str, id: str, order: dict) -> dict:
        """
        Обновить заказ (записать транзакцию)

        :param type: параметр транзакции. Возможные значения:
                clientId – ID клиента
                cardBarcode – Токен/Баркод карты
                cardNumber – Номер карты
                phone – Телефон
        :param id: значение поля, указанного в type
        :param order: параметры заказа
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
        :return:
        Пример return:
        {
            "response":
            {
                "guid": "123"    # id возврата
            }
        }
        """
        params = {
            "type": type,
            "id": id
        }
        return self._send_request(
            method="post",
            url=f"{self.api}/updateOrder",
            headers=self.headers,
            params=params,
            data=order
        )

    def update_oder_by_client_id(self, client_id: int, order: dict) -> dict:
        """
        Обновить заказ по ID клиента

        :param client_id: ID клиента
        :param order: параметры заказа
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
        :return:
        Пример return:
        {
            "response":
            {
                "guid": "123"    # id возврата
            }
        }
        """
        return self.update_order(
            type="clientId",
            id=str(client_id),
            order=order
        )

    def update_oder_by_card_barcode(self, card_barcode: str, order: dict) -> dict:
        """
        Обновить заказ по токену / баркоду карты

        :param card_barcode: токен / баркод карты
        :param order: параметры заказа
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
        :return:
        Пример return:
        {
            "response":
            {
                "guid": "123"    # id возврата
            }
        }
        """
        return self.update_order(
            type="cardBarcode",
            id=card_barcode,
            order=order
        )

    def update_oder_by_card_number(self, card_number: str, order: dict) -> dict:
        """
        Обновить заказ по номеру карты

        :param card_number: номер карты
        :param order: параметры заказа
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
        :return:
        Пример return:
        {
            "response":
            {
                "guid": "123"    # id возврата
            }
        }
        """
        return self.update_order(
            type="cardNumber",
            id=card_number,
            order=order
        )

    def update_oder_by_phone(self, phone: str, order: dict) -> dict:
        """
        Обновить заказ по телефону

        :param phone: номер телефона
        :param order: параметры заказа
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
        :return:
        Пример return:
        {
            "response":
            {
                "guid": "123"    # id возврата
            }
        }
        """
        return self.update_order(
            type="phone",
            id=phone,
            order=order
        )

    def return_order(self, order: dict) -> dict:
        """
        Отменить / вернуть заказ (отменить транзакци)

        :param order:
        Пример order:
        {
            "guid": "123",    # ID транзакции
            "date": "2018-01-01 00:00:00",    # Дата транзакции
            "sum": 1200.00    # Сумма транзакции без скидки
        }

        :return:
        Пример return:
        {
            "response":
            {
                "guid": "123"    # id транзакции
            }
        }
        """
        return self._send_request(
            method="post",
            url=f"{self.api}/returnOrder",
            headers=self.headers,
            params=dict(),
            data=order
        )

    def return_cart(self, type: str, id: str, cart: dict) -> dict:
        """
        Возврат товара

        :param type: параметр транзакции. Возможные значения:
                clientId – ID клиента
                cardBarcode – Токен/Баркод карты
                cardNumber – Номер карты
                phone – Телефон
        :param id: значение поля, указанного в type
        :param cart: параметры товара
        Пример cart:
        {
            "guid": "123",    # ID возврата
            "number": "213",    # Номер возврата
            "date": "2018-01-01 00:00:00",    # Дата возврата
            "sum": 1200.00,    # Сумма возврата без скидки
            "sumDiscount": 1100.00,    # Сумма возврата со скидкой
            "bonusAdd": 200.00,    # Начислено бонусов
            "bonusWriteOff": 200.00,    # Списано бонусов
            "depositAdd": 0.00,    # Пополнение депозита
            "depositWriteOff": 0.00,    # Списание с депозита
            "cart":
            [
                {
                    "nid": "123",    # ID номенклатуры
                    "groupId": "145",    # ID группы номенклатуры
                    "groupName": "Печенье",    # Наименование группы номенклатуры
                    "name": "Печенька",    # Наименование номенклатуры
                    "price": 100.00,    # Стоимость номенклатуры
                    "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
                    "amount": 1.0    # Количество
                },
                {
                    "nid": "124",
                    "groupId": "145",
                    "groupName": "Мороженное",
                    "name": "Мороженка",
                    "price": 900.00,
                    "priceWithDiscount": 900.00,
                    "amount": 0.51
                }
            ]
        }

        :return:
        Пример return
        {
            "response":
            {
                "guid": "123"    # id возврата
            }
        }
        """
        params = {
            "type": type,
            "id": id
        }
        return self._send_request(
            method="post",
            url=f"{self.api}/returnCart",
            headers=self.headers,
            params=params,
            data=cart
        )

    def return_cart_by_client_id(self, client_id: int, cart: dict) -> dict:
        """
        Возврат товара по ID клиента

        :param client_id: ID клиента
        :param cart: параметры товара
        Пример cart:
        {
            "guid": "123",    # ID возврата
            "number": "213",    # Номер возврата
            "date": "2018-01-01 00:00:00",    # Дата возврата
            "sum": 1200.00,    # Сумма возврата без скидки
            "sumDiscount": 1100.00,    # Сумма возврата со скидкой
            "bonusAdd": 200.00,    # Начислено бонусов
            "bonusWriteOff": 200.00,    # Списано бонусов
            "depositAdd": 0.00,    # Пополнение депозита
            "depositWriteOff": 0.00,    # Списание с депозита
            "cart":
            [
                {
                    "nid": "123",    # ID номенклатуры
                    "groupId": "145",    # ID группы номенклатуры
                    "groupName": "Печенье",    # Наименование группы номенклатуры
                    "name": "Печенька",    # Наименование номенклатуры
                    "price": 100.00,    # Стоимость номенклатуры
                    "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
                    "amount": 1.0    # Количество
                },
                {
                    "nid": "124",
                    "groupId": "145",
                    "groupName": "Мороженное",
                    "name": "Мороженка",
                    "price": 900.00,
                    "priceWithDiscount": 900.00,
                    "amount": 0.51
                }
            ]
        }

        :return:
        Пример return
        {
            "response":
            {
                "guid": "123"    # id возврата
            }
        }
        """
        return self.return_cart(
            type="clientId",
            id=str(client_id),
            cart=cart
        )

    def return_cart_by_card_barcode(self, card_barcode: str, cart: dict) -> dict:
        """
        Возврат товара по токену / баркоду карты

        :param card_barcode: токен / баркод карты
        :param cart: параметры товара
        Пример cart:
        {
            "guid": "123",    # ID возврата
            "number": "213",    # Номер возврата
            "date": "2018-01-01 00:00:00",    # Дата возврата
            "sum": 1200.00,    # Сумма возврата без скидки
            "sumDiscount": 1100.00,    # Сумма возврата со скидкой
            "bonusAdd": 200.00,    # Начислено бонусов
            "bonusWriteOff": 200.00,    # Списано бонусов
            "depositAdd": 0.00,    # Пополнение депозита
            "depositWriteOff": 0.00,    # Списание с депозита
            "cart":
            [
                {
                    "nid": "123",    # ID номенклатуры
                    "groupId": "145",    # ID группы номенклатуры
                    "groupName": "Печенье",    # Наименование группы номенклатуры
                    "name": "Печенька",    # Наименование номенклатуры
                    "price": 100.00,    # Стоимость номенклатуры
                    "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
                    "amount": 1.0    # Количество
                },
                {
                    "nid": "124",
                    "groupId": "145",
                    "groupName": "Мороженное",
                    "name": "Мороженка",
                    "price": 900.00,
                    "priceWithDiscount": 900.00,
                    "amount": 0.51
                }
            ]
        }

        :return:
        Пример return
        {
            "response":
            {
                "guid": "123"    # id возврата
            }
        }
        """
        return self.return_cart(
            type="cardBarcode",
            id=card_barcode,
            cart=cart
        )

    def return_cart_by_card_number(self, card_number: str, cart: dict) -> dict:
        """
        Возврат товара по номеру карты

        :param card_number: номер карты
        :param cart: параметры товара
        Пример cart:
        {
            "guid": "123",    # ID возврата
            "number": "213",    # Номер возврата
            "date": "2018-01-01 00:00:00",    # Дата возврата
            "sum": 1200.00,    # Сумма возврата без скидки
            "sumDiscount": 1100.00,    # Сумма возврата со скидкой
            "bonusAdd": 200.00,    # Начислено бонусов
            "bonusWriteOff": 200.00,    # Списано бонусов
            "depositAdd": 0.00,    # Пополнение депозита
            "depositWriteOff": 0.00,    # Списание с депозита
            "cart":
            [
                {
                    "nid": "123",    # ID номенклатуры
                    "groupId": "145",    # ID группы номенклатуры
                    "groupName": "Печенье",    # Наименование группы номенклатуры
                    "name": "Печенька",    # Наименование номенклатуры
                    "price": 100.00,    # Стоимость номенклатуры
                    "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
                    "amount": 1.0    # Количество
                },
                {
                    "nid": "124",
                    "groupId": "145",
                    "groupName": "Мороженное",
                    "name": "Мороженка",
                    "price": 900.00,
                    "priceWithDiscount": 900.00,
                    "amount": 0.51
                }
            ]
        }

        :return:
        Пример return
        {
            "response":
            {
                "guid": "123"    # id возврата
            }
        }
        """
        return self.return_cart(
            type="cardNumber",
            id=card_number,
            cart=cart
        )

    def return_cart_by_phone(self, phone: str, cart: dict) -> dict:
        """
        Возврат товара по телефону

        :param phone: номер телефона
        :param cart: параметры товара
        Пример cart:
        {
            "guid": "123",    # ID возврата
            "number": "213",    # Номер возврата
            "date": "2018-01-01 00:00:00",    # Дата возврата
            "sum": 1200.00,    # Сумма возврата без скидки
            "sumDiscount": 1100.00,    # Сумма возврата со скидкой
            "bonusAdd": 200.00,    # Начислено бонусов
            "bonusWriteOff": 200.00,    # Списано бонусов
            "depositAdd": 0.00,    # Пополнение депозита
            "depositWriteOff": 0.00,    # Списание с депозита
            "cart":
            [
                {
                    "nid": "123",    # ID номенклатуры
                    "groupId": "145",    # ID группы номенклатуры
                    "groupName": "Печенье",    # Наименование группы номенклатуры
                    "name": "Печенька",    # Наименование номенклатуры
                    "price": 100.00,    # Стоимость номенклатуры
                    "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
                    "amount": 1.0    # Количество
                },
                {
                    "nid": "124",
                    "groupId": "145",
                    "groupName": "Мороженное",
                    "name": "Мороженка",
                    "price": 900.00,
                    "priceWithDiscount": 900.00,
                    "amount": 0.51
                }
            ]
        }

        :return:
        Пример return
        {
            "response":
            {
                "guid": "123"    # id возврата
            }
        }
        """
        return self.return_cart(
            type="phone",
            id=phone,
            cart=cart
        )

    def update_return_cart(self, type: str, id: str, cart: dict) -> dict:
        """
        Возврат товара

        :param type: параметр транзакции. Возможные значения:
                clientId – ID клиента
                cardBarcode – Токен/Баркод карты
                cardNumber – Номер карты
                phone – Телефон
        :param id: значение поля, указанного в type
        :param cart: параметры товара
        Пример cart:
        {
            "guid": "123",    # ID возврата
            "number": "213",    # Номер возврата
            "date": "2018-01-01 00:00:00",    # Дата возврата
            "sum": 1200.00,    # Сумма возврата без скидки
            "sumDiscount": 1100.00,    # Сумма возврата со скидкой
            "bonusAdd": 200.00,    # Начислено бонусов
            "bonusWriteOff": 200.00,    # Списано бонусов
            "depositAdd": 0.00,    # Пополнение депозита
            "depositWriteOff": 0.00,    # Списание с депозита
            "cart":
            [
                {
                    "nid": "123",    # ID номенклатуры
                    "groupId": "145",    # ID группы номенклатуры
                    "groupName": "Печенье",    # Наименование группы номенклатуры
                    "name": "Печенька",    # Наименование номенклатуры
                    "price": 100.00,    # Стоимость номенклатуры
                    "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
                    "amount": 1.0    # Количество
                },
                {
                    "nid": "B9AD56BF-9D5B-AE4C-BA8B-2D724E2FEFC7",
                    "groupId": "AC977305-F43E-8049-A233-15487AC4392A",
                    "groupName": "Лимонады соб.\/пр-ва",
                    "name": "Лимонад Малина-Маракуйя 400мл",
                    "price": 200,
                    "priceWithDiscount": 150,
                    "amount": 1.0
                }
            ]
        }

        :return:
        Пример return
        {
            "response":
            {
                "guid": "123"    # id транзакции
            }
        }
        """
        params = {
            "type": type,
            "id": id
        }
        return self._send_request(
            method="post",
            url=f"{self.api}/updateReturnCart",
            headers=self.headers,
            params=params,
            data=cart
        )

    def update_return_cart_by_client_id(self, client_id: int, cart: dict) -> dict:
        """
        Возврат товара по ID клиента

        :param client_id: ID клиента
        :param cart: параметры товара
        Пример cart:
        {
            "guid": "123",    # ID возврата
            "number": "213",    # Номер возврата
            "date": "2018-01-01 00:00:00",    # Дата возврата
            "sum": 1200.00,    # Сумма возврата без скидки
            "sumDiscount": 1100.00,    # Сумма возврата со скидкой
            "bonusAdd": 200.00,    # Начислено бонусов
            "bonusWriteOff": 200.00,    # Списано бонусов
            "depositAdd": 0.00,    # Пополнение депозита
            "depositWriteOff": 0.00,    # Списание с депозита
            "cart":
            [
                {
                    "nid": "123",    # ID номенклатуры
                    "groupId": "145",    # ID группы номенклатуры
                    "groupName": "Печенье",    # Наименование группы номенклатуры
                    "name": "Печенька",    # Наименование номенклатуры
                    "price": 100.00,    # Стоимость номенклатуры
                    "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
                    "amount": 1.0    # Количество
                },
                {
                    "nid": "B9AD56BF-9D5B-AE4C-BA8B-2D724E2FEFC7",
                    "groupId": "AC977305-F43E-8049-A233-15487AC4392A",
                    "groupName": "Лимонады соб.\/пр-ва",
                    "name": "Лимонад Малина-Маракуйя 400мл",
                    "price": 200,
                    "priceWithDiscount": 150,
                    "amount": 1.0
                }
            ]
        }

        :return:
        Пример return
        {
            "response":
            {
                "guid": "123"    # id транзакции
            }
        }
        """
        return self.update_return_cart(
            type="clientId",
            id=str(client_id),
            cart=cart
        )

    def update_return_cart_by_card_barcode(self, card_barcode: str, cart: dict) -> dict:
        """
        Возврат товара по токену / баркоду карты

        :param card_barcode: токен / баркод карты
        :param cart: параметры товара
        Пример cart:
        {
            "guid": "123",    # ID возврата
            "number": "213",    # Номер возврата
            "date": "2018-01-01 00:00:00",    # Дата возврата
            "sum": 1200.00,    # Сумма возврата без скидки
            "sumDiscount": 1100.00,    # Сумма возврата со скидкой
            "bonusAdd": 200.00,    # Начислено бонусов
            "bonusWriteOff": 200.00,    # Списано бонусов
            "depositAdd": 0.00,    # Пополнение депозита
            "depositWriteOff": 0.00,    # Списание с депозита
            "cart":
            [
                {
                    "nid": "123",    # ID номенклатуры
                    "groupId": "145",    # ID группы номенклатуры
                    "groupName": "Печенье",    # Наименование группы номенклатуры
                    "name": "Печенька",    # Наименование номенклатуры
                    "price": 100.00,    # Стоимость номенклатуры
                    "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
                    "amount": 1.0    # Количество
                },
                {
                    "nid": "B9AD56BF-9D5B-AE4C-BA8B-2D724E2FEFC7",
                    "groupId": "AC977305-F43E-8049-A233-15487AC4392A",
                    "groupName": "Лимонады соб.\/пр-ва",
                    "name": "Лимонад Малина-Маракуйя 400мл",
                    "price": 200,
                    "priceWithDiscount": 150,
                    "amount": 1.0
                }
            ]
        }

        :return:
        Пример return
        {
            "response":
            {
                "guid": "123"    # id транзакции
            }
        }
        """
        return self.update_return_cart(
            type="cardBarcode",
            id=card_barcode,
            cart=cart
        )

    def update_return_cart_by_card_number(self, card_number: str, cart: dict) -> dict:
        """
        Возврат товара по номеру карты

        :param card_number: номер карты
        :param cart: параметры товара
        Пример cart:
        {
            "guid": "123",    # ID возврата
            "number": "213",    # Номер возврата
            "date": "2018-01-01 00:00:00",    # Дата возврата
            "sum": 1200.00,    # Сумма возврата без скидки
            "sumDiscount": 1100.00,    # Сумма возврата со скидкой
            "bonusAdd": 200.00,    # Начислено бонусов
            "bonusWriteOff": 200.00,    # Списано бонусов
            "depositAdd": 0.00,    # Пополнение депозита
            "depositWriteOff": 0.00,    # Списание с депозита
            "cart":
            [
                {
                    "nid": "123",    # ID номенклатуры
                    "groupId": "145",    # ID группы номенклатуры
                    "groupName": "Печенье",    # Наименование группы номенклатуры
                    "name": "Печенька",    # Наименование номенклатуры
                    "price": 100.00,    # Стоимость номенклатуры
                    "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
                    "amount": 1.0    # Количество
                },
                {
                    "nid": "B9AD56BF-9D5B-AE4C-BA8B-2D724E2FEFC7",
                    "groupId": "AC977305-F43E-8049-A233-15487AC4392A",
                    "groupName": "Лимонады соб.\/пр-ва",
                    "name": "Лимонад Малина-Маракуйя 400мл",
                    "price": 200,
                    "priceWithDiscount": 150,
                    "amount": 1.0
                }
            ]
        }

        :return:
        Пример return
        {
            "response":
            {
                "guid": "123"    # id транзакции
            }
        }
        """
        return self.update_return_cart(
            type="cardNumber",
            id=card_number,
            cart=cart
        )

    def update_return_cart_by_phone(self, phone: str, cart: dict) -> dict:
        """
        Возврат товара по телефону

        :param phone: номер телефона
        :param cart: параметры товара
        Пример cart:
        {
            "guid": "123",    # ID возврата
            "number": "213",    # Номер возврата
            "date": "2018-01-01 00:00:00",    # Дата возврата
            "sum": 1200.00,    # Сумма возврата без скидки
            "sumDiscount": 1100.00,    # Сумма возврата со скидкой
            "bonusAdd": 200.00,    # Начислено бонусов
            "bonusWriteOff": 200.00,    # Списано бонусов
            "depositAdd": 0.00,    # Пополнение депозита
            "depositWriteOff": 0.00,    # Списание с депозита
            "cart":
            [
                {
                    "nid": "123",    # ID номенклатуры
                    "groupId": "145",    # ID группы номенклатуры
                    "groupName": "Печенье",    # Наименование группы номенклатуры
                    "name": "Печенька",    # Наименование номенклатуры
                    "price": 100.00,    # Стоимость номенклатуры
                    "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
                    "amount": 1.0    # Количество
                },
                {
                    "nid": "B9AD56BF-9D5B-AE4C-BA8B-2D724E2FEFC7",
                    "groupId": "AC977305-F43E-8049-A233-15487AC4392A",
                    "groupName": "Лимонады соб.\/пр-ва",
                    "name": "Лимонад Малина-Маракуйя 400мл",
                    "price": 200,
                    "priceWithDiscount": 150,
                    "amount": 1.0
                }
            ]
        }

        :return:
        Пример return
        {
            "response":
            {
                "guid": "123"    # id транзакции
            }
        }
        """
        return self.update_return_cart(
            type="phone",
            id=phone,
            cart=cart
        )

    def get_new_orders(self, limit: int = 100) -> dict:
        """
        Получить новые заказы

        :param limit: по сколько новых заказов возвращать (не обязательный)

        :return:
        Пример return:
        {
            "newOrder":
            [
                {
                    "clientId": 1234,    # ID клиента
                    "guid": "123",    # ID транзакции
                    "number": "213",    # Номер транзакции
                    "date": "2018-01-01 00:00:00",    # Дата транзакции
                    "sum": 1200.0,    # Сумма транзакции без скидки
                    "sumDiscount": 1000.0,    # Сумма транзакции со скидкой
                    "bonusAdd": 200.0,    # Начислено бонусов
                    "bonusWriteOff": 200.0,    # Списано бонусов
                    "bonusAfter": 1200.0,    # Бонусный баланс после визита
                    "depositAdd": 0.0,    # Пополнение депозита
                    "depositWriteOff": 0.0    # Списание с депозита
                    "depositAfter": 1200.0,    # Бонусный баланс после визита
                },
                {
                    "clientId": 1234,
                    "guid": "124",
                    "number": "214",
                    "date": "2018-01-01 00:00:00",
                    "sum": 1200.0,
                    "sumDiscount": 1100.0,
                    "bonusAdd": 0.0,
                    "bonusWriteOff": 100.0,
                    "bonusAfter": 1200.0,
                    "depositAdd": 0.0,
                    "depositWriteOff": 0.0
                    "depositAfter": 1200.0,
                }
            ]
        }
        """
        params = {
            "limit": limit,
        }
        return self._send_request(
            method="get",
            url=f"{self.api}/getNewOrder",
            headers=self.headers,
            params=params,
            data=dict()
        )

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
        clients = [
            {
                "clientId": client_id
            }
        ]
        clients[0].update(variables)
        data = {
            "clients": clients
        }

        return self._send_request(
            method="post",
            url=f"{self.api}/updateVars",
            headers=self.headers,
            params=dict(),
            data=data
        )

    def send_card_sms(self, client_id: int, message: str, unix_time: str):
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
        return self._send_request(
            method="post",
            url=f"{self.api}/sendCardSMS",
            headers=self.headers,
            params=dict(),
            data=data
        )

    def update_integration(self, integration: dict):
        """
        Обновление интеграции

        :param integration: данные интеграции
        Пример integration:
        {
            "integrationSoftName":"НазваниеПО",
            "versionIntegrationSoft":"2.3.2.28",
            "additionModul" :
            {
                "unloadingNewClients":"1.0.0.1",    # Выгрузка новых клиентов
                "loadingTypesCards":"1.0.0.1",    # Загрузка видов карт
                "loadingNewClients":"1.0.0.1",    # Получить клиентов
                "synchronizationOrder":"1.0.0.1"    # Синхронизация транзакций
            }
        }

        :return:
        Пример return:
        {
            "integrationSoftName":"ИмяКонфигурации",
            "versionIntegrationSoft":"2.3.2.28",
            "update" :
            [
                "unloadingNewClients":
                [
                    "version":"0.3",    # Доступная версия обновления
                    "'base64":"",    # Двоичный код новой версии
                    "url":"",    # Ссылка на файл с обновлением
                ],
                "synchronizationOrder":
                [
                    "version":"0.3"
                    "'base64":"",
                    "url":"",
                ]
            ]
        }

        Пример return, если нет обновлений:
        {
            "integrationSoftName": "Розница",
            "versionIntegrationSoft":"2.3.2.28",
            "update" : null,
            "error":
            {
                "errorId": 715,
                "message": "No updates"
            }
        }

        Другие варианты ответа:
        {
            "integrationSoftName": "Розница",
            "versionIntegrationSoft":"2.3.2.28",
            "update" : null,
            "error":
            {
                "errorId": 716,
                "message": "No settings found"    # Нет настройки для конфигурации
            }
        }


        {
            "integrationSoftName": "Розница",
            "versionIntegrationSoft":"2.3.2.28",
            "update" : null,
            "error":
            {
                "errorId": 717,
                "message": "No settings found for this version"    # Нет настроек для версии
            }
        }
        """
        return self._send_request(
            method="post",
            url=f"{self.api}/getUpdateIntegration",
            headers=self.headers,
            params=dict(),
            data=integration
        )

    def __validate(self, response, params):
        if response.status_code == 200:
            data = response.json()
            if data.get('error'):
                print("status_code", response.status_code)
                print("headers", self.headers)
                print("params", params)
                print("response", data)
            else:
                return data
        else:
            print(response.status_code, response.text)
