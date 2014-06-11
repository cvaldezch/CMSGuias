from CMSGuias.apps.almacen.models import Pedido, GuiaRemision, Suministro
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
        cod = Pedido.objects.all().aggregate(Max('pedido_id'))
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
#generate serie - number of guide for key guide remision
def GenerateSerieGuideRemision():
    id = None
    try:
        cod= GuiaRemision.objects.all().aggregate(Max('guia_id'))
        id= cod['guia_id__max']
        if id is not None:
            #print 'codigo not empty'
            sr= int(id[0:3])
            num= int(id[4:])
            #print "%i %i"%(sr,num)
            sr= sr+1 if num >= 99999999 else sr
            num= num+1 if num <= 99999999 else 1
            #print "%i %i"%(sr,num)
        else:
            sr= 1
            num= 1
        id= "%s-%s"%("{:0>3d}".format(sr),"{:0>8d}".format(num))
    except ObjectDoesNotExist, e:
        id= "000-00000000"
    return id

# Generate id for order supply
def GenerateKeySupply():
	  id = None
	  try:
	  	  cod = Suministro.objcets.aggregate(max=Max('suministro_id'))
	  	  id = cod['max']
	  	  cy = int(datetime.datetime.today().strftime(__year_str))
	  	  if id is not None:
	  	  	  yy = int(id[2:4])
	  	  	  counter = int(id[4:10])
	  	  	  if cy > yy:
	  	  	  	  counter = 1
	  	  	  else:
	  	  	  	  counter += 1
	  	  else:
	  	  	  counter = 1
	  	  id = "%s%s%s"%('SP', cy.__str__(), "{:0>6d}".format(counter))
	  except ObjectDoesNotExist:
	  	raise e
	  return id