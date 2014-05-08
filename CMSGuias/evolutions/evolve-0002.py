from django_evolution.mutations import AddField, ChangeField
from django.db import models


MUTATIONS = [
    AddField('Proyecto', 'status', models.CharField, initial=u'00', max_length=2),
    ChangeField('Materiale', 'matpre', initial=None, null=True),
    AddField('Detpedido', 'cantshop', models.FloatField, initial=0)
]
