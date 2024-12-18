from flask import request, abort, redirect, url_for, session
from functools import wraps
from flask_login import current_user, logout_user


def is_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.role == 'admin':
            return func(*args, **kwargs)
        return abort(401)
    return decorated_function


def same_user(func):
    @wraps(func)
    def decorated_function(*args, email, **kwargs):
        if current_user.email != email:
            return abort(403)
        return func(*args, email=email, **kwargs)
    return decorated_function


def has_pharmacy(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.pharmacy:
            return redirect(url_for('index'))
        return func(*args, *kwargs)
    return decorated_function


def is_active(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.active == 'no':
            session.clear()
            logout_user()
            response = redirect(url_for('login'))
            response.cache_control.no_cache = True
            return response
        return func(*args, **kwargs)
    return decorated_function


def calc_discount(results, suppliers: list, info: dict):
    prices_discount = []

    for product in results:
        for price in product.prices:
            if price.supplier_info.id in suppliers:
                prices_discount.append(
                    {
                        "product_id": price.product_info.id,
                        "product_price_id": price.id,
                        "product_name": product.name,
                        "supplier_id": price.supplier_info.id,
                        "supplier": price.supplier_info.name,
                        "price": round(price.price * (1 - info[price.supplier_info.id]['discount']), 2),
                        "due_date": price.due_date,
                        "stock": price.stock,
                    }

                )

            else:
                prices_discount.append(
                    {
                        "product_id": product.id,
                        "product_price_id": price.id,
                        "product_name": product.name,
                        "supplier_id": price.supplier_info.id,
                        "supplier": price.supplier_info.name,
                        "price": price.price,
                        "due_date": price.due_date,
                        "stock": price.stock,
                    }

                )

    prices_discount.sort(key=lambda item: item['price'])

    return prices_discount


def discount_cart(shopping_cart, user_discount):
    suppliers = [item for item in user_discount]

    for item in shopping_cart:
        if shopping_cart[item]['supplier_id'] in suppliers:
            # apply discount
            for product in shopping_cart[item]['products']:
                shopping_cart[item]['products'][product]['price'] = \
                    round(shopping_cart[item]['products'][product]['price'] * \
                          (1 - user_discount[shopping_cart[item]['supplier_id']]['discount']), 2)

            shopping_cart[item]['total'] = round(shopping_cart[item]['total'] *
                                                 (1 - user_discount[shopping_cart[item]['supplier_id']]['discount']), 2)

    return shopping_cart
