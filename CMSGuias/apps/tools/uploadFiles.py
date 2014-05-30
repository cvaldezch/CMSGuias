#-*- Encoding: utf-8 -*-
from django.conf import settings
import datetime
import os

def upload(absolutePath,archive,options={}):
	#defaults= {"date": False,"time": False}
	try:
		# path absolute
		path= "%s%s"%(settings.MEDIA_ROOT,absolutePath)
		# verify path exists if not exists path makers the folders
		if not os.path.exists(path):
			os.makedirs(path,774)
			os.chmod(path,0774)
		# verify aggregate options to name of file
		name= None
		if len(options) > 0:
			pass
		else:
			name= archive.name
		filename= "%s%s"%(path,name)
		# recover full address of filename
		dirfilename= open(filename, "wb+")
		# walk all file and save im new address
		for bit in archive.chunks():
			dirfilename.write(bit)
		# close file
		dirfilename.close()
		# changes file permissions
		os.chmod(filename, 0777)
	except Exception, e:
		raise e
	return filename

def removeTmp(absolutePath):
	try:
		os.remove(absolutePath)
	except Exception, e:
		raise e