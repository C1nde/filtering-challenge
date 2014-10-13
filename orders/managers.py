from django.db import models


class OrderManager(models.Manager):
    """
    Custom manager for Order model
    """
    def split_by_shipping_method(self):
        fcm = []
        pri = []
        for model in self.get_queryset().all():
            if model.shipping_method == self.model.FCM:
                fcm.append(model)
            elif model.shipping_method == self.model.PRI:
                pri.append(model)
        return fcm, pri

    def split_by_single_and_multiple(self):
        singles = []
        multiples = []
        all_orders = self.get_queryset().annotate(models.Count('items')).all()
        for order in all_orders:
            if order.items__count == 1:
                singles.append(order)
            elif order.items__count > 0:
                multiples.append(order)
        return singles, multiples

    def single_orders_are_sorted(self):
        orders = self.get_queryset().annotate(models.Count('items')).filter(items__count=1).select_related('items')
        return sorted(orders, key=lambda order: order.items.first().PRIORITY[order.items.first().product])
