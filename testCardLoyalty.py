from datetime import datetime

from CardLoyaltyBasket import Basket
from CardLoyaltyOrder import Order
from functions import dump

test = "Order"

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
