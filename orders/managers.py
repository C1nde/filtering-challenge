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
