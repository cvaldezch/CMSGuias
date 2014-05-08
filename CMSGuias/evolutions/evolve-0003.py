from django_evolution.mutations import AddField
from django.db import models


MUTATIONS = [
    AddField('Proyecto', 'ruccliente', models.ForeignKey, null=True, related_model='almacen.Cliente')
]
