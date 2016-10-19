from CMSGuias.apps.ventas.models import Proyecto, Painting

class PaintingData(object):
    
    def push(self):
        try:
            pr = Proyecto.objects.filter(flag=True)
            for x in pr:
                try:
                    Painting.objects.get(project_id=x.proyecto_id)
                except Painting.DoesNotExist:
                    Painting.objects.create(project_id=x.proyecto_id,
                                            nlayers=1,
                                            nfilmb=4,
                                            nfilmc=4).save()
        except Exception as e:
            print e
