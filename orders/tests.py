from django.test import TestCase

from orders.models import Order, OrderItem

import results


class OrderOrderingTestCase(TestCase):
    fixtures = ['test_orders.json']

    def test_orders_are_split_by_shipping_method(self):
        fcm, pri = Order.objects.split_by_shipping_method()
        fcm = [model.pk for model in fcm]
        pri = [model.pk for model in pri]
        self.assertEqual(results.fcm, fcm)
        self.assertEqual(results.pri, pri)

    def test_orders_are_split_by_single_and_multiple(self):
        singles, multiples = Order.objects.split_by_single_and_multiple()
        singles = [model.pk for model in singles]
        multiples = [model.pk for model in multiples]
        self.assertEqual(results.singles, singles)
        self.assertEqual(results.multiples, multiples)

    def test_single_orders_are_sorted(self):
        single_sorted_orders = Order.objects.single_orders_are_sorted()
        items_sizes = [order.items.first().product for order in single_sorted_orders]
        ordered_right = all([OrderItem.PRIORITY[items_sizes[number]] <= OrderItem.PRIORITY[size] for number, size in enumerate(items_sizes[1:])])
        self.assertTrue(ordered_right)

    def test_multiple_orders_are_split_by_xxl_and_not(self):
        xxl, not_xxl = Order.objects.orders_split_by_xxl_and_not()
        xxl = [model.pk for model in xxl]
        not_xxl = [model.pk for model in not_xxl]
        self.assertEqual(results.xxl, xxl)
        self.assertEqual(results.not_xxl, not_xxl)
