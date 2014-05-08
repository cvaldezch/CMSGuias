from django_evolution.mutations import AddField
from django.db import models


MUTATIONS = [
    AddField('Niple', 'cantidad', models.IntegerField, null=True),
    AddField('tmpniple', 'cantidad', models.IntegerField, null=True)
]
