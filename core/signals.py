from django.db import Error


class LimitNumberRecordsError(Error):
    pass



def event_handler(sender, **kwargs):
    if sender.objects.filter(teacher=kwargs['kwargs']['teacher']).count() < 3:
        pass
    else:
        raise LimitNumberRecordsError