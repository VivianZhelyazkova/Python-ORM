import os
import django
from django.db.models import Q, Count, F, Case, Value, When, BooleanField

from main_app.models import Profile, Order, Product

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ""

    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string)
        |
        Q(email__icontains=search_string)
        |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if not profiles.exists():
        return ""

    return "\n".join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders.count()}"
        for p in profiles
    )


def get_loyal_profiles() -> str:
    profiles = Profile.objects.get_regular_customers()

    if not profiles.exists():
        return ""

    return "\n".join(
        f"Profile: {p.full_name}, orders: {p.orders.count()}"
        for p in profiles
    )


def get_last_sold_products() -> str:
    last_order = Order.objects.prefetch_related('products').last()

    if last_order is None or not last_order.products.exists():
        return ""

    products = ', '.join(last_order.products.order_by('name').values_list('name', flat=True))

    return f"Last sold products: {products}"


def get_top_products():
    products = Product.objects.annotate(
        orders_count=Count("order")
    ).filter(orders_count__gt=0).order_by("-orders_count", "name")[:5]
    if not products.exists():
        return ""

    result = "\n".join(f"{p.name}, sold {p.orders_count} times" for p in products)
    return f"Top products:\n" + result


def apply_discounts():
    orders = Order.objects.annotate(
        products_count=Count("products")).filter(products_count__gt=2, is_completed=False).update(
        total_price=F("total_price") * 0.9)
    return f"Discount applied to {orders} orders."


def complete_order():
    last_order = Order.objects.filter(is_completed=False).order_by("creation_date").first()
    if not last_order:
        return ""
    last_order.products.update(
        in_stock=F("in_stock") - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F("is_available"),
            output=BooleanField()
        ))
    last_order.is_completed = True
    last_order.save()

    return "Order has been completed!"
