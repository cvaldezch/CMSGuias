from django_evolution.mutations import DeleteField


MUTATIONS = [
    DeleteField('Proyecto', 'telefono')
]
