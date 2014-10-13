from django.test import TestCase

from orders.models import Order, OrderItem


class OrderOrderingTestCase(TestCase):
    fixtures = ['test_orders.json']

    def test_orders_are_split_by_shipping_method(self):
        fcm, pri = Order.objects.split_by_shipping_method()
        all_fcm = all([order.shipping_method == Order.FCM for order in fcm])
        all_pri = all([order.shipping_method == Order.PRI for order in pri])

        self.assertTrue(all_fcm)
        self.assertTrue(all_pri)

    def test_orders_are_split_by_single_and_multiple(self):
        singles, multiples = Order.objects.split_by_single_and_multiple()
        all_singles = all([order.items.count() == 1 for order in singles])
        all_multiples = all([order.items.count() >= 2 for order in multiples])

        self.assertTrue(all_singles)
        self.assertTrue(all_multiples)

    def test_single_orders_are_sorted(self):
        single_sorted_orders = Order.objects.single_orders_are_sorted()
        items_sizes = [order.items.first().product for order in single_sorted_orders]
        ordered_right = all([OrderItem.PRIORITY[items_sizes[number]] <= OrderItem.PRIORITY[size] for number, size in enumerate(items_sizes[1:])])

        self.assertTrue(ordered_right)

    def test_multiple_orders_are_split_by_xxl_and_not(self):
        xxl, not_xxl = Order.objects.orders_split_by_xxl_and_not()
        all_xxl = all(["XXL" in order.items.values_list('product', flat=True) for order in xxl])
        all_not_xxl = all(["XXL" not in order.items.values_list('product', flat=True) for order in not_xxl])

        self.assertTrue(all_xxl)
        self.assertTrue(all_not_xxl)
