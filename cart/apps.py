from django.apps import AppConfig


class CartAppConfig(AppConfig):
    name = 'cart'

    def ready(self):
        import cart.signals
