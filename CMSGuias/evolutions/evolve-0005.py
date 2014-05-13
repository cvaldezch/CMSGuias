from django_evolution.mutations import AddField
from django.db import models


MUTATIONS = [
    AddField('Pedido', 'sector', models.ForeignKey, initial=<<USER VALUE REQUIRED>>, related_model=u'almacen.Sectore'),
    AddField('Pedido', 'subproyecto', models.ForeignKey, initial=<<USER VALUE REQUIRED>>, related_model=u'almacen.Subproyecto')
]
