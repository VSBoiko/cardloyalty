from datetime import datetime
import time

from CardLoyaltyBasket import Basket
from CardLoyaltyOrder import Order
from CardLoyaltyService import Service
from CardLoyaltyOrganization import Organization
from functions import dump

test = "Organization"

if test == "Basket":
    new_basket = Basket()

    # Добавить товар в корзину
    new_basket.add_item(
        product_id="84",
        name="Картошка",
        amount=5,
        price=30.00,
        discount_price=25.00,
        group_id="7",
        group_name="Овощи"
    )
    new_basket.add_item(
        product_id="97",
        name="Морковка",
        amount=2,
        price=50.00,
        discount_price=40.00,
        group_id="7",
        group_name="Овощи"
    )

    # Товары в корзине
    basket_products = new_basket.get_basket()
    basket_products_for_order = new_basket.get_basket_for_order()

    print("\nТовары в корзине")
    dump(basket_products)
    print("\n")
    dump(basket_products_for_order)


    # Стоимость корзины
    basket_price = new_basket.get_basket_price()                            # 250.0
    basket_discount_price = new_basket.get_basket_price_with_discount()     # 205.0

    print("\nСтоимость корзины")
    print("Без скидки", basket_price)
    print("Со скидкой", basket_discount_price)


    # Есть ли товар в корзине
    is_potatoes_in_basket = new_basket.is_item_in_basket("84")              # True
    is_pumpkin_in_basket = new_basket.is_item_in_basket("51")               # False

    print("\nЕсть ли товар в корзине")
    print("Картошка", is_potatoes_in_basket)
    print("Тыква", is_pumpkin_in_basket)


    # Получить товар корзины
    carrot = new_basket.get_item_from_basket("97")

    print("\nТовар корзины")
    dump(carrot)


    # Обновить количество и стоимость товара в коризне
    new_basket.update_item_amount("84", 6)
    new_basket.update_item_price("84", 35.00)
    new_basket.update_item_price_with_discount("84", 30.00)

    print("\nСтоимость корзины после обновления цены товара")
    print(new_basket.get_basket_price())                                    # 310.0
    print(new_basket.get_basket_price_with_discount())                      # 260.0
elif test == "Order":
    # Создание корзины заказа
    new_basket = Basket()
    new_basket.add_item(
        product_id="84",
        name="Картошка",
        amount=5,
        price=30.00,
        discount_price=25.00,
        group_id="7",
        group_name="Овощи"
    )
    new_basket.add_item(
        product_id="97",
        name="Морковка",
        amount=2,
        price=50.00,
        discount_price=40.00,
        group_id="7",
        group_name="Овощи"
    )

    new_order = Order(
        guid="order_26",
        number="26",
        date=datetime.now(),
        basket=new_basket
    )

    # Данные заказа
    order_info_for_order = new_order.get_to_create_order()

    print("\nДанные заказа")
    dump(order_info_for_order)

    # Стоимость корзины
    order_price = new_order.get_order_price()
    order_discount_price = new_order.get_order_price_with_discount()

    print("\nСтоимость заказа")
    print("Без скидки", order_price)                        # 250.0
    print("Со скидкой", order_discount_price)               # 205.0

    # Корзина заказа
    order_basket = new_order.get_order_basket()

    print("\nКорзина заказа")
    dump(order_basket.get_basket())
elif test == "Service":
    test_service = Service()

    # Получить все теги
    all_tags = test_service.get_all_tags()

    print("Получить все теги")
    dump(all_tags)


    # Получить название тега
    tag_id = 1458
    tag_name = test_service.get_tag_name(tag_id)

    print("Название тега с ID", tag_id)
    print(tag_name)


    # Получить все шаблоны
    all_templates = test_service.get_all_templates()

    print("Получить все шаблоны")
    dump(all_templates)


    # Добавить тег
    new_tag = test_service.add_tag("test tag")

    print("Добавить тег")
    dump(new_tag)
    dump(test_service.get_all_tags())

    # СМС
    res = test_service.send_sms(
        380278,
        "test",
        int(time.time())
    )
    print("\nСМС")
    dump(res)
elif test == "Organization":
    organizat = Organization()

    test_client = {
        "cardBarcode": "1040482",
        "cardNumber": "1040482",
        "clientId": "377308",
        "phone": "79165449909"
    }

    # Получить клиентов
    all_clients = organizat.get_all_clients(1, 10)
    new_clients = organizat.get_new_clients(1)
    print("\nКлиенты")
    print("\nВсе клиенты:")
    dump(all_clients)
    print("\nНовые клиенты:")
    dump(new_clients)
    print("\nКлиент по ID:")
    cl_id = int(test_client.get("clientId"))
    dump(organizat.get_client_by_id(cl_id))
    print("\nКлиент по баркоду:")
    cl_barcode = test_client.get("cardBarcode")
    dump(organizat.get_client_by_barcode(cl_barcode))
    print("\nКлиент по номеру карты:")
    cl_card = test_client.get("cardBarcode")
    dump(organizat.get_client_by_card(cl_card))
    print("\nКлиент по телефону:")
    cl_phone = test_client.get("phone")
    dump(organizat.get_client_by_phone(cl_phone))

    # # Регистрация
    # reg = organizat.registration(
    #     id="6v8-y4hsjg-n45try",
    #     name="Василек",
    #     plugin_version="8.0",
    #     soft_name="1C:Розница",
    #     soft_version="8.6.3"
    # )
    # print("\nРегистрация")
    # dump(reg)
    #
    # # Интеграция
    # integ = organizat.update_integration(
    #     soft_name="НазваниеПО",
    #     soft_version="1.1.1",
    #     unloading_new_clients="1.1.1",
    #     loading_types_cards="1.1.1",
    #     loading_new_clients="1.1.1",
    #     synchronization_order="1.1.1"
    # )
    # print("\nИнтеграция")
    # dump(integ)

    # Новый клиент
    # add_cl = organizat.add_client(
    #     first_name="Нестеренко",
    #     last_name="Николай",
    #     phone="79288828409",
    #     card_number="281340",
    #     card_barcode="281340",
    # )
    # print("\nНовый клиент")
    # dump(add_cl)

    # add_cl:
    # {
    #     "cardBarcode": "281340",
    #     "cardNumber": "281340",
    #     "clientId": 380278,
    #     "hash": "49ccc8ab45392bda8fa0cf809bb5e123",
    #     "phone": "7777777777"
    # }
