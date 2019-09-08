from django.apps import AppConfig
from django.db.models.signals import pre_init
from .signals import event_handler


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        MyModel = self.get_model('DiscipleTeacher')
        pre_init.connect(event_handler, sender=MyModel, dispatch_uid='limit_on_number_recruit')