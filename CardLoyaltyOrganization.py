import json
from datetime import datetime

import CardLoyaltyBasic
import CardLoyaltyOrder


class Organization(CardLoyaltyBasic.Basic):
    def __init__(self):
        super().__init__()

    def add_client(self,
                   first_name: str,
                   last_name: str,
                   phone: str,
                   card_number: str,
                   card_barcode: str,
                   patronymic: str = "",
                   email: str = "",
                   sex: int = 0,
                   birthday: datetime = "",
                   template_id: int = 0,
                   tags: tuple = (),
                   comment: str = "",
                   ) -> dict:
        """
        Добавить клиента

        :param first_name: фамилия
        :param last_name: имя
        :param phone: телефон (уникальный)
        :param card_number: номер карты (уникальный)
        :param card_barcode: токен или баркод (только латиница и цифры)

        :param (необязат.) patronymic: отчество
        :param (необязат.) email: e-mail
        :param (необязат.) sex: 1 – мужской, 2 – женский, 0 – не определен
        :param (необязат.) birthday: дата рождения
        :param (необязат.) template_id: ID макета
        :param (необязат.) tags: список с ID тегов
        :param (необязат.) comment: произвольный комментарий к клиенту

        :return:
        Пример return:
        {
            "clientId": 4321,    # ID клиента
            "phone": "79777121350",    # Телефон
            "cardNumber": "1234",    # Номер карты
            "cardBarcode": "dld123s",    # Токен/Баркод
            "hash": "q386v8y4hsjgn45y8ehy45try"    # hash карты
        }

        Пример return в случае ошибки:
        {
            "phone": "79777121350",    # Телефон
            "cardNumber": "1234",    # Номер карты
            "cardBarcode": "dld123s",    # Токен/Баркод
            "errorId": 702,    # Код ошибки
            "message": "invalid ..."    # Сообщение
        }

        В остальных случаях: {}
        """
        if isinstance(birthday, datetime):
            birthday_format = birthday.strftime("%Y-%m-%d")
        else:
            birthday_format = birthday

        new_client = {
            "lastName": last_name,
            "firstName": first_name,
            "patronymic": patronymic,
            "phone": phone,
            "email": email,
            "sex": sex,
            "birthday": birthday_format,
            "templateId": template_id,
            "cardNumber": card_number,
            "cardBarcode": card_barcode,
            "comment": comment,
            "tags": list(tags)
        }
        result = self._create_clients(
            clients=[new_client]
        )

        if "response" in result:
            return result.get("response").pop()
        elif "error" in result:
            return result.get("error").pop()
        else:
            return {}

    def create_order_by_client_id(self, client_id: int, order: CardLoyaltyOrder.Order) -> dict:
        """
        Создать заказ по ID клиента

        :param client_id: ID клиента
        :param order: заказ

        :return:
        Пример return:
        {
            "guid": "123"    # id транзакции
        }
        """
        result = self._create_order(
            type="clientId",
            id=str(client_id),
            order=order.get_to_create_order()
        )

        if "response" in result:
            return result.get("response")
        elif "error" in result:
            return result.get("error")
        else:
            return {}

    def create_order_by_barcode(self, card_barcode: str, order: CardLoyaltyOrder.Order) -> dict:
        """
        Создать заказ по токену / баркоду карты

        :param card_barcode: токен / баркод карты
        :param order: заказ

        :return:
        Пример return:
        {
            "guid": "123"    # id транзакции
        }
        """
        result = self._create_order(
            type="cardBarcode",
            id=card_barcode,
            order=order.get_to_create_order()
        )

        if "response" in result:
            return result.get("response")
        elif "error" in result:
            return result.get("error")
        else:
            return {}

    def create_order_by_card(self, card_number: str, order: CardLoyaltyOrder.Order) -> dict:
        """
        Создать заказ по номеру карты

        :param card_number: номер карты
        :param order: заказ

        :return:
        {
            "guid": "123"    # id транзакции
        }
        """
        result = self._create_order(
            type="cardNumber",
            id=card_number,
            order=order.get_to_create_order()
        )

        if "response" in result:
            return result.get("response")
        elif "error" in result:
            return result.get("error")
        else:
            return {}

    def create_order_by_phone(self, phone: str, order: CardLoyaltyOrder.Order) -> dict:
        """
        Создать заказ по телефону

        :param phone: номер телефона
        :param order: заказ

        :return:
        {
            "guid": "123"    # id транзакции
        }
        """
        result = self._create_order(
            type="phone",
            id=phone,
            order=order.get_to_create_order()
        )

        if "response" in result:
            return result.get("response")
        elif "error" in result:
            return result.get("error")
        else:
            return {}

    def get_all_clients(self, limit: int = 100, offset: int = 0) -> list:
        """
        Получить всех клиентов

        :param limit: по сколько клиентов возвращать
        :param offset: смещение (например, смещение 2 - будет передан 3 и 4 клиент)

        :return:
        Пример return:
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

        Если клиентов нет: []
        """
        clients = self._get_clients_all(
            limit=limit,
            offset=offset
        )
        if "clients" in clients:
            return clients.get("clients")
        else:
            return []

    def get_client_by_id(self, client_id: int) -> dict:
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
        client = self._client_info(
            type="clientId",
            id=str(client_id)
        )
        return client if client else {}

    def get_client_by_barcode(self, card_barcode: str) -> dict:
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
        client = self._client_info(
            type="cardBarcode",
            id=card_barcode
        )
        return client if client else {}

    def get_client_by_card(self, card_number: str) -> dict:
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
        client = self._client_info(
            type="cardNumber",
            id=card_number
        )
        return client if client else {}

    def get_client_by_phone(self, phone: str) -> dict:
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
        client = self._client_info(
            type="phone",
            id=phone
        )
        return client if client else {}

    def get_new_clients(self, limit: int = 100) -> list:
        """
        Получить только новых клиентов

        :param limit: по сколько клиентов возвращать

        :return:
        Пример return:
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
                "cardBarcode": "dld123s",    # токен или баркод – только латиницы и цифры
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

        Если клиентов нет: []
        """
        clients = self._get_clients_new(
            limit=limit,
        )
        if "clients" in clients:
            return clients.get("clients")
        else:
            return []

    def get_new_orders(self, limit: int = 100) -> list:
        """
        Получить новые заказы

        :param limit: по сколько новых заказов возвращать (не обязательный)

        :return:
        Пример return:
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
        """
        result = self._get_orders_new(limit)
        if "newOrder" in result:
            return result.get("newOrder")
        else:
            return []

    def registration(self, id: str, name: str, plugin_version: str,
                     soft_name: str, soft_version: str) -> bool:
        """
        Регистрация организации

        :param id: идентификатор организации (например, "6v8-y4hsjg-n45try")
        :param name: наименование организации (например, "Василек")
        :param plugin_version: версия интеграции (например, "8.0")
        :param soft_name: наименование ПО, с которым проводится интеграция (например, "1C:Розница")
        :param soft_version: версия ПО, с которым проводится интеграция (например, "8.6.3")

        :return:
        True (в случае успеха) или False (в случае ошибки)
        """
        organization = {
            "organisationId": id,
            "organisationName": name,
            "versionPlugin": plugin_version,
            "integrationSoftName": soft_name,
            "versionIntegrationSoft": soft_version
        }
        result = self._update_registration_organisation(organization).get("response")

        if "status" in result and result.get("status") == "1":
            return True
        else:
            return False

    def update_integration(self, soft_name: str, soft_version: str,
                           unloading_new_clients: str, loading_types_cards: str,
                           loading_new_clients: str, synchronization_order: str) -> dict:
        """
        Обновление интеграции

        :param soft_name: наименование ПО, с которым проводится интеграция (например, "НазваниеПО")
        :param soft_version: версия ПО, с которым проводится интеграция (например, "2.3.2.28")
        :param unloading_new_clients: выгрузка новых клиентов (например, "1.0.0.1")
        :param loading_types_cards: загрузка видов карт (например, "1.0.0.1")
        :param loading_new_clients: получить клиентов (например, "1.0.0.1")
        :param synchronization_order: синхронизация транзакций (например, "1.0.0.1")

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
        integration = {
            "integrationSoftName": soft_name,
            "versionIntegrationSoft": soft_version,
            "additionModul":
                {
                    "unloadingNewClients": unloading_new_clients,
                    "loadingTypesCards": loading_types_cards,
                    "loadingNewClients": loading_new_clients,
                    "synchronizationOrder": synchronization_order
                }
        }
        result = self._get_update_integration(integration)

        return result if result else {}

    def update_client(self, client_id: int, client_info: dict) -> dict:
        """
        Обновить клиента

        :param client_id: ID клиента
        :param client_info: данные клиента
        Пример client_info:
        {
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
            "clientId": 1234,    # ID успешно обработанного клиента
            "phone": "79777121350",    # Номер телефона клиента
            "cardNumber": "11234",    # Номер карты
            "cardBarcode": "rr-34566"    # Токен/Баркод – только латиницы и цифры
        }

        Пример return в случае ошибки:
        {
            "сlientId": 431,    # ID не успешно обработанного клиента
            "errorId": 12,    # Код ошибки
            "message": "invalid phone number"    # Сообщение
        }

        В остальных случаях: {}
        """
        client_info.update({'clientId': client_id})
        result = self._update_clients([client_info])
        if "response" in result:
            return result.get("response").pop()
        elif "error" in result:
            return result.get("error").pop()
        else:
            return {}


    # WIP
    # def _update_order_by_client_id(self, client_id: int, order: CardLoyaltyOrder.Order) -> dict:
    #     """
    #     Обновить заказ по ID клиента
    #
    #     :param client_id: ID клиента
    #     :param order: параметры заказа
    #     Пример order:
    #     {
    #         "guid": "2-43F2-4148-A264-8787414DC88",    # ID транзакции
    #         "number": "005",    # Номер транзакции
    #         "date": "2020-02-18 18:18:18",    # Дата транзакции
    #         "sum": 1690,    # Сумма транзакции без скидки
    #         "sumDiscount": 1690,    # Сумма транзакции со скидкой
    #         "bonusAdd": "0",    # Начислено бонусов
    #         "bonusWriteOff": "20",    # Списано бонусов
    #         "depositAdd": "0",    # Пополнение депозита
    #         "depositWriteOff": "20",    # Списание с депозита
    #         "cart":
    #         [
    #             {
    #                 "nid": "36ACB48C-438D-F241",    # ID номенклатуры
    #                 "groupId": "BEA57842-935",    # ID группы номенклатуры
    #                 "groupName": "Стейки",    # Наименование группы номенклатуры
    #                 "name": "Мексика\/Чойс 240\/30гр",    # Наименование номенклатуры
    #                 "price": 1300,    # Стоимость номенклатуры
    #                 "priceWithDiscount": 1300,    # Стоимость номенклатуры с учетом скидки
    #             },
    #             {
    #                 "amount": 1    # Количество
    #                 "nid":"7882EAF6-B08E-1041-8B8B-8F4CEDDB3B80",
    #                 "groupId":"F2FD3F09-96D6-9441-99E5-FF65505F6980",
    #                 "groupName":"Салаты\/Закуски",
    #                 "name":"Салат с розовыми помидорами и домашним сыром 270гр",
    #                 "price":390,
    #                 "priceWithDiscount":390,
    #             }
    #         ]
    #     }
    #     :return:
    #     Пример return:
    #     {
    #         "response":
    #         {
    #             "guid": "123"    # id возврата
    #         }
    #     }
    #     """
    #     return self._update_order(
    #         type="clientId",
    #         id=str(client_id),
    #         order=order
    #     )
    #
    # def _update_order_by_card_barcode(self, card_barcode: str, order: CardLoyaltyOrder.Order) -> dict:
    #     """
    #     Обновить заказ по токену / баркоду карты
    #
    #     :param card_barcode: токен / баркод карты
    #     :param order: параметры заказа
    #     Пример order:
    #     {
    #         "guid": "2-43F2-4148-A264-8787414DC88",    # ID транзакции
    #         "number": "005",    # Номер транзакции
    #         "date": "2020-02-18 18:18:18",    # Дата транзакции
    #         "sum": 1690,    # Сумма транзакции без скидки
    #         "sumDiscount": 1690,    # Сумма транзакции со скидкой
    #         "bonusAdd": "0",    # Начислено бонусов
    #         "bonusWriteOff": "20",    # Списано бонусов
    #         "depositAdd": "0",    # Пополнение депозита
    #         "depositWriteOff": "20",    # Списание с депозита
    #         "cart":
    #         [
    #             {
    #                 "nid": "36ACB48C-438D-F241",    # ID номенклатуры
    #                 "groupId": "BEA57842-935",    # ID группы номенклатуры
    #                 "groupName": "Стейки",    # Наименование группы номенклатуры
    #                 "name": "Мексика\/Чойс 240\/30гр",    # Наименование номенклатуры
    #                 "price": 1300,    # Стоимость номенклатуры
    #                 "priceWithDiscount": 1300,    # Стоимость номенклатуры с учетом скидки
    #             },
    #             {
    #                 "amount": 1    # Количество
    #                 "nid":"7882EAF6-B08E-1041-8B8B-8F4CEDDB3B80",
    #                 "groupId":"F2FD3F09-96D6-9441-99E5-FF65505F6980",
    #                 "groupName":"Салаты\/Закуски",
    #                 "name":"Салат с розовыми помидорами и домашним сыром 270гр",
    #                 "price":390,
    #                 "priceWithDiscount":390,
    #             }
    #         ]
    #     }
    #     :return:
    #     Пример return:
    #     {
    #         "response":
    #         {
    #             "guid": "123"    # id возврата
    #         }
    #     }
    #     """
    #     return self._update_order(
    #         type="cardBarcode",
    #         id=card_barcode,
    #         order=order
    #     )
    #
    # def _update_order_by_card_number(self, card_number: str, order: CardLoyaltyOrder.Order) -> dict:
    #     """
    #     Обновить заказ по номеру карты
    #
    #     :param card_number: номер карты
    #     :param order: параметры заказа
    #     Пример order:
    #     {
    #         "guid": "2-43F2-4148-A264-8787414DC88",    # ID транзакции
    #         "number": "005",    # Номер транзакции
    #         "date": "2020-02-18 18:18:18",    # Дата транзакции
    #         "sum": 1690,    # Сумма транзакции без скидки
    #         "sumDiscount": 1690,    # Сумма транзакции со скидкой
    #         "bonusAdd": "0",    # Начислено бонусов
    #         "bonusWriteOff": "20",    # Списано бонусов
    #         "depositAdd": "0",    # Пополнение депозита
    #         "depositWriteOff": "20",    # Списание с депозита
    #         "cart":
    #         [
    #             {
    #                 "nid": "36ACB48C-438D-F241",    # ID номенклатуры
    #                 "groupId": "BEA57842-935",    # ID группы номенклатуры
    #                 "groupName": "Стейки",    # Наименование группы номенклатуры
    #                 "name": "Мексика\/Чойс 240\/30гр",    # Наименование номенклатуры
    #                 "price": 1300,    # Стоимость номенклатуры
    #                 "priceWithDiscount": 1300,    # Стоимость номенклатуры с учетом скидки
    #             },
    #             {
    #                 "amount": 1    # Количество
    #                 "nid":"7882EAF6-B08E-1041-8B8B-8F4CEDDB3B80",
    #                 "groupId":"F2FD3F09-96D6-9441-99E5-FF65505F6980",
    #                 "groupName":"Салаты\/Закуски",
    #                 "name":"Салат с розовыми помидорами и домашним сыром 270гр",
    #                 "price":390,
    #                 "priceWithDiscount":390,
    #             }
    #         ]
    #     }
    #     :return:
    #     Пример return:
    #     {
    #         "response":
    #         {
    #             "guid": "123"    # id возврата
    #         }
    #     }
    #     """
    #     return self._update_order(
    #         type="cardNumber",
    #         id=card_number,
    #         order=order
    #     )
    #
    # def _update_order_by_phone(self, phone: str, order: CardLoyaltyOrder.Order) -> dict:
    #     """
    #     Обновить заказ по телефону
    #
    #     :param phone: номер телефона
    #     :param order: параметры заказа
    #     Пример order:
    #     {
    #         "guid": "2-43F2-4148-A264-8787414DC88",    # ID транзакции
    #         "number": "005",    # Номер транзакции
    #         "date": "2020-02-18 18:18:18",    # Дата транзакции
    #         "sum": 1690,    # Сумма транзакции без скидки
    #         "sumDiscount": 1690,    # Сумма транзакции со скидкой
    #         "bonusAdd": "0",    # Начислено бонусов
    #         "bonusWriteOff": "20",    # Списано бонусов
    #         "depositAdd": "0",    # Пополнение депозита
    #         "depositWriteOff": "20",    # Списание с депозита
    #         "cart":
    #         [
    #             {
    #                 "nid": "36ACB48C-438D-F241",    # ID номенклатуры
    #                 "groupId": "BEA57842-935",    # ID группы номенклатуры
    #                 "groupName": "Стейки",    # Наименование группы номенклатуры
    #                 "name": "Мексика\/Чойс 240\/30гр",    # Наименование номенклатуры
    #                 "price": 1300,    # Стоимость номенклатуры
    #                 "priceWithDiscount": 1300,    # Стоимость номенклатуры с учетом скидки
    #             },
    #             {
    #                 "amount": 1    # Количество
    #                 "nid":"7882EAF6-B08E-1041-8B8B-8F4CEDDB3B80",
    #                 "groupId":"F2FD3F09-96D6-9441-99E5-FF65505F6980",
    #                 "groupName":"Салаты\/Закуски",
    #                 "name":"Салат с розовыми помидорами и домашним сыром 270гр",
    #                 "price":390,
    #                 "priceWithDiscount":390,
    #             }
    #         ]
    #     }
    #     :return:
    #     Пример return:
    #     {
    #         "response":
    #         {
    #             "guid": "123"    # id возврата
    #         }
    #     }
    #     """
    #     return self._update_order(
    #         type="phone",
    #         id=phone,
    #         order=order
    #     )
    #
    #
    # def _update_return_cart_by_client_id(self, client_id: int, cart: dict) -> dict:
    #     """
    #     Возврат товара по ID клиента
    #
    #     :param client_id: ID клиента
    #     :param cart: параметры товара
    #     Пример cart:
    #     {
    #         "guid": "123",    # ID возврата
    #         "number": "213",    # Номер возврата
    #         "date": "2018-01-01 00:00:00",    # Дата возврата
    #         "sum": 1200.00,    # Сумма возврата без скидки
    #         "sumDiscount": 1100.00,    # Сумма возврата со скидкой
    #         "bonusAdd": 200.00,    # Начислено бонусов
    #         "bonusWriteOff": 200.00,    # Списано бонусов
    #         "depositAdd": 0.00,    # Пополнение депозита
    #         "depositWriteOff": 0.00,    # Списание с депозита
    #         "cart":
    #         [
    #             {
    #                 "nid": "123",    # ID номенклатуры
    #                 "groupId": "145",    # ID группы номенклатуры
    #                 "groupName": "Печенье",    # Наименование группы номенклатуры
    #                 "name": "Печенька",    # Наименование номенклатуры
    #                 "price": 100.00,    # Стоимость номенклатуры
    #                 "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
    #                 "amount": 1.0    # Количество
    #             },
    #             {
    #                 "nid": "B9AD56BF-9D5B-AE4C-BA8B-2D724E2FEFC7",
    #                 "groupId": "AC977305-F43E-8049-A233-15487AC4392A",
    #                 "groupName": "Лимонады соб.\/пр-ва",
    #                 "name": "Лимонад Малина-Маракуйя 400мл",
    #                 "price": 200,
    #                 "priceWithDiscount": 150,
    #                 "amount": 1.0
    #             }
    #         ]
    #     }
    #
    #     :return:
    #     Пример return
    #     {
    #         "response":
    #         {
    #             "guid": "123"    # id транзакции
    #         }
    #     }
    #     """
    #     return self._update_return_cart(
    #         type="clientId",
    #         id=str(client_id),
    #         cart=cart
    #     )
    #
    # def _update_return_cart_by_card_barcode(self, card_barcode: str, cart: dict) -> dict:
    #     """
    #     Возврат товара по токену / баркоду карты
    #
    #     :param card_barcode: токен / баркод карты
    #     :param cart: параметры товара
    #     Пример cart:
    #     {
    #         "guid": "123",    # ID возврата
    #         "number": "213",    # Номер возврата
    #         "date": "2018-01-01 00:00:00",    # Дата возврата
    #         "sum": 1200.00,    # Сумма возврата без скидки
    #         "sumDiscount": 1100.00,    # Сумма возврата со скидкой
    #         "bonusAdd": 200.00,    # Начислено бонусов
    #         "bonusWriteOff": 200.00,    # Списано бонусов
    #         "depositAdd": 0.00,    # Пополнение депозита
    #         "depositWriteOff": 0.00,    # Списание с депозита
    #         "cart":
    #         [
    #             {
    #                 "nid": "123",    # ID номенклатуры
    #                 "groupId": "145",    # ID группы номенклатуры
    #                 "groupName": "Печенье",    # Наименование группы номенклатуры
    #                 "name": "Печенька",    # Наименование номенклатуры
    #                 "price": 100.00,    # Стоимость номенклатуры
    #                 "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
    #                 "amount": 1.0    # Количество
    #             },
    #             {
    #                 "nid": "B9AD56BF-9D5B-AE4C-BA8B-2D724E2FEFC7",
    #                 "groupId": "AC977305-F43E-8049-A233-15487AC4392A",
    #                 "groupName": "Лимонады соб.\/пр-ва",
    #                 "name": "Лимонад Малина-Маракуйя 400мл",
    #                 "price": 200,
    #                 "priceWithDiscount": 150,
    #                 "amount": 1.0
    #             }
    #         ]
    #     }
    #
    #     :return:
    #     Пример return
    #     {
    #         "response":
    #         {
    #             "guid": "123"    # id транзакции
    #         }
    #     }
    #     """
    #     return self._update_return_cart(
    #         type="cardBarcode",
    #         id=card_barcode,
    #         cart=cart
    #     )
    #
    # def _update_return_cart_by_card_number(self, card_number: str, cart: dict) -> dict:
    #     """
    #     Возврат товара по номеру карты
    #
    #     :param card_number: номер карты
    #     :param cart: параметры товара
    #     Пример cart:
    #     {
    #         "guid": "123",    # ID возврата
    #         "number": "213",    # Номер возврата
    #         "date": "2018-01-01 00:00:00",    # Дата возврата
    #         "sum": 1200.00,    # Сумма возврата без скидки
    #         "sumDiscount": 1100.00,    # Сумма возврата со скидкой
    #         "bonusAdd": 200.00,    # Начислено бонусов
    #         "bonusWriteOff": 200.00,    # Списано бонусов
    #         "depositAdd": 0.00,    # Пополнение депозита
    #         "depositWriteOff": 0.00,    # Списание с депозита
    #         "cart":
    #         [
    #             {
    #                 "nid": "123",    # ID номенклатуры
    #                 "groupId": "145",    # ID группы номенклатуры
    #                 "groupName": "Печенье",    # Наименование группы номенклатуры
    #                 "name": "Печенька",    # Наименование номенклатуры
    #                 "price": 100.00,    # Стоимость номенклатуры
    #                 "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
    #                 "amount": 1.0    # Количество
    #             },
    #             {
    #                 "nid": "B9AD56BF-9D5B-AE4C-BA8B-2D724E2FEFC7",
    #                 "groupId": "AC977305-F43E-8049-A233-15487AC4392A",
    #                 "groupName": "Лимонады соб.\/пр-ва",
    #                 "name": "Лимонад Малина-Маракуйя 400мл",
    #                 "price": 200,
    #                 "priceWithDiscount": 150,
    #                 "amount": 1.0
    #             }
    #         ]
    #     }
    #
    #     :return:
    #     Пример return
    #     {
    #         "response":
    #         {
    #             "guid": "123"    # id транзакции
    #         }
    #     }
    #     """
    #     return self._update_return_cart(
    #         type="cardNumber",
    #         id=card_number,
    #         cart=cart
    #     )
    #
    # def _update_return_cart_by_phone(self, phone: str, cart: dict) -> dict:
    #     """
    #     Возврат товара по телефону
    #
    #     :param phone: номер телефона
    #     :param cart: параметры товара
    #     Пример cart:
    #     {
    #         "guid": "123",    # ID возврата
    #         "number": "213",    # Номер возврата
    #         "date": "2018-01-01 00:00:00",    # Дата возврата
    #         "sum": 1200.00,    # Сумма возврата без скидки
    #         "sumDiscount": 1100.00,    # Сумма возврата со скидкой
    #         "bonusAdd": 200.00,    # Начислено бонусов
    #         "bonusWriteOff": 200.00,    # Списано бонусов
    #         "depositAdd": 0.00,    # Пополнение депозита
    #         "depositWriteOff": 0.00,    # Списание с депозита
    #         "cart":
    #         [
    #             {
    #                 "nid": "123",    # ID номенклатуры
    #                 "groupId": "145",    # ID группы номенклатуры
    #                 "groupName": "Печенье",    # Наименование группы номенклатуры
    #                 "name": "Печенька",    # Наименование номенклатуры
    #                 "price": 100.00,    # Стоимость номенклатуры
    #                 "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
    #                 "amount": 1.0    # Количество
    #             },
    #             {
    #                 "nid": "B9AD56BF-9D5B-AE4C-BA8B-2D724E2FEFC7",
    #                 "groupId": "AC977305-F43E-8049-A233-15487AC4392A",
    #                 "groupName": "Лимонады соб.\/пр-ва",
    #                 "name": "Лимонад Малина-Маракуйя 400мл",
    #                 "price": 200,
    #                 "priceWithDiscount": 150,
    #                 "amount": 1.0
    #             }
    #         ]
    #     }
    #
    #     :return:
    #     Пример return
    #     {
    #         "response":
    #         {
    #             "guid": "123"    # id транзакции
    #         }
    #     }
    #     """
    #     return self._update_return_cart(
    #         type="phone",
    #         id=phone,
    #         cart=cart
    #     )
    #
    #
    # def _return_cart_by_client_id(self, client_id: int, cart: dict) -> dict:
    #     """
    #     Возврат товара по ID клиента
    #
    #     :param client_id: ID клиента
    #     :param cart: параметры товара
    #     Пример cart:
    #     {
    #         "guid": "123",    # ID возврата
    #         "number": "213",    # Номер возврата
    #         "date": "2018-01-01 00:00:00",    # Дата возврата
    #         "sum": 1200.00,    # Сумма возврата без скидки
    #         "sumDiscount": 1100.00,    # Сумма возврата со скидкой
    #         "bonusAdd": 200.00,    # Начислено бонусов
    #         "bonusWriteOff": 200.00,    # Списано бонусов
    #         "depositAdd": 0.00,    # Пополнение депозита
    #         "depositWriteOff": 0.00,    # Списание с депозита
    #         "cart":
    #         [
    #             {
    #                 "nid": "123",    # ID номенклатуры
    #                 "groupId": "145",    # ID группы номенклатуры
    #                 "groupName": "Печенье",    # Наименование группы номенклатуры
    #                 "name": "Печенька",    # Наименование номенклатуры
    #                 "price": 100.00,    # Стоимость номенклатуры
    #                 "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
    #                 "amount": 1.0    # Количество
    #             },
    #             {
    #                 "nid": "124",
    #                 "groupId": "145",
    #                 "groupName": "Мороженное",
    #                 "name": "Мороженка",
    #                 "price": 900.00,
    #                 "priceWithDiscount": 900.00,
    #                 "amount": 0.51
    #             }
    #         ]
    #     }
    #
    #     :return:
    #     Пример return
    #     {
    #         "response":
    #         {
    #             "guid": "123"    # id возврата
    #         }
    #     }
    #     """
    #     return self._return_cart(
    #         type="clientId",
    #         id=str(client_id),
    #         cart=cart
    #     )
    #
    # def _return_cart_by_card_barcode(self, card_barcode: str, cart: dict) -> dict:
    #     """
    #     Возврат товара по токену / баркоду карты
    #
    #     :param card_barcode: токен / баркод карты
    #     :param cart: параметры товара
    #     Пример cart:
    #     {
    #         "guid": "123",    # ID возврата
    #         "number": "213",    # Номер возврата
    #         "date": "2018-01-01 00:00:00",    # Дата возврата
    #         "sum": 1200.00,    # Сумма возврата без скидки
    #         "sumDiscount": 1100.00,    # Сумма возврата со скидкой
    #         "bonusAdd": 200.00,    # Начислено бонусов
    #         "bonusWriteOff": 200.00,    # Списано бонусов
    #         "depositAdd": 0.00,    # Пополнение депозита
    #         "depositWriteOff": 0.00,    # Списание с депозита
    #         "cart":
    #         [
    #             {
    #                 "nid": "123",    # ID номенклатуры
    #                 "groupId": "145",    # ID группы номенклатуры
    #                 "groupName": "Печенье",    # Наименование группы номенклатуры
    #                 "name": "Печенька",    # Наименование номенклатуры
    #                 "price": 100.00,    # Стоимость номенклатуры
    #                 "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
    #                 "amount": 1.0    # Количество
    #             },
    #             {
    #                 "nid": "124",
    #                 "groupId": "145",
    #                 "groupName": "Мороженное",
    #                 "name": "Мороженка",
    #                 "price": 900.00,
    #                 "priceWithDiscount": 900.00,
    #                 "amount": 0.51
    #             }
    #         ]
    #     }
    #
    #     :return:
    #     Пример return
    #     {
    #         "response":
    #         {
    #             "guid": "123"    # id возврата
    #         }
    #     }
    #     """
    #     return self._return_cart(
    #         type="cardBarcode",
    #         id=card_barcode,
    #         cart=cart
    #     )
    #
    # def _return_cart_by_card_number(self, card_number: str, cart: dict) -> dict:
    #     """
    #     Возврат товара по номеру карты
    #
    #     :param card_number: номер карты
    #     :param cart: параметры товара
    #     Пример cart:
    #     {
    #         "guid": "123",    # ID возврата
    #         "number": "213",    # Номер возврата
    #         "date": "2018-01-01 00:00:00",    # Дата возврата
    #         "sum": 1200.00,    # Сумма возврата без скидки
    #         "sumDiscount": 1100.00,    # Сумма возврата со скидкой
    #         "bonusAdd": 200.00,    # Начислено бонусов
    #         "bonusWriteOff": 200.00,    # Списано бонусов
    #         "depositAdd": 0.00,    # Пополнение депозита
    #         "depositWriteOff": 0.00,    # Списание с депозита
    #         "cart":
    #         [
    #             {
    #                 "nid": "123",    # ID номенклатуры
    #                 "groupId": "145",    # ID группы номенклатуры
    #                 "groupName": "Печенье",    # Наименование группы номенклатуры
    #                 "name": "Печенька",    # Наименование номенклатуры
    #                 "price": 100.00,    # Стоимость номенклатуры
    #                 "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
    #                 "amount": 1.0    # Количество
    #             },
    #             {
    #                 "nid": "124",
    #                 "groupId": "145",
    #                 "groupName": "Мороженное",
    #                 "name": "Мороженка",
    #                 "price": 900.00,
    #                 "priceWithDiscount": 900.00,
    #                 "amount": 0.51
    #             }
    #         ]
    #     }
    #
    #     :return:
    #     Пример return
    #     {
    #         "response":
    #         {
    #             "guid": "123"    # id возврата
    #         }
    #     }
    #     """
    #     return self._return_cart(
    #         type="cardNumber",
    #         id=card_number,
    #         cart=cart
    #     )
    #
    # def _return_cart_by_phone(self, phone: str, cart: dict) -> dict:
    #     """
    #     Возврат товара по телефону
    #
    #     :param phone: номер телефона
    #     :param cart: параметры товара
    #     Пример cart:
    #     {
    #         "guid": "123",    # ID возврата
    #         "number": "213",    # Номер возврата
    #         "date": "2018-01-01 00:00:00",    # Дата возврата
    #         "sum": 1200.00,    # Сумма возврата без скидки
    #         "sumDiscount": 1100.00,    # Сумма возврата со скидкой
    #         "bonusAdd": 200.00,    # Начислено бонусов
    #         "bonusWriteOff": 200.00,    # Списано бонусов
    #         "depositAdd": 0.00,    # Пополнение депозита
    #         "depositWriteOff": 0.00,    # Списание с депозита
    #         "cart":
    #         [
    #             {
    #                 "nid": "123",    # ID номенклатуры
    #                 "groupId": "145",    # ID группы номенклатуры
    #                 "groupName": "Печенье",    # Наименование группы номенклатуры
    #                 "name": "Печенька",    # Наименование номенклатуры
    #                 "price": 100.00,    # Стоимость номенклатуры
    #                 "priceWithDiscount": 90.00,    # Стоимость номенклатуры с учетом скидки
    #                 "amount": 1.0    # Количество
    #             },
    #             {
    #                 "nid": "124",
    #                 "groupId": "145",
    #                 "groupName": "Мороженное",
    #                 "name": "Мороженка",
    #                 "price": 900.00,
    #                 "priceWithDiscount": 900.00,
    #                 "amount": 0.51
    #             }
    #         ]
    #     }
    #
    #     :return:
    #     Пример return
    #     {
    #         "response":
    #         {
    #             "guid": "123"    # id возврата
    #         }
    #     }
    #     """
    #     return self._return_cart(
    #         type="phone",
    #         id=phone,
    #         cart=cart
    #     )
