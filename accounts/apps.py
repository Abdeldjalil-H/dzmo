from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "accounts"
    verbose_name = "الحسابات"

    def ready(self):
        import accounts.signals
