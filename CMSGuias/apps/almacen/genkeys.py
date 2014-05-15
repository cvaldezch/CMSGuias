from CMSGuias.apps.almacen import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
import datetime

### format date str
__date_str = "%Y-%m-%d"
__year_str = "%y" # 'AA'
### 


def __init__():
	return "MSG => select key generator"

def GenerateIdOrders():
	id = None
	try:
		cod = models.Pedido.objects.all().aggregate(Max('pedido_id'))
		id = cod['pedido_id__max']
		an= int(datetime.datetime.today().strftime(__year_str))
		if id is not None:
			aa= int(id[2:4])
			count = int(id[4:10])
			if an > aa:
				count = 1
			else:
				count+= 1
		else:
			count = 1
		id= "%s%s%s"%('PE',str(an),"{:0>6d}".format(count))
	except ObjectDoesNotExist, e:
		msg = "Error generator"
	return u"%s"%id