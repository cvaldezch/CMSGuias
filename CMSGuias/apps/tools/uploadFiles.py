#-*- Encoding: utf-8 -*-
from django.conf import settings
import datetime
import os
import urllib


def upload(absolutePath,archive,options={}):
    #defaults= {"date": False,"time": False}
    try:
        # path absolute
        path = '%s%s'%(settings.MEDIA_ROOT, absolutePath)
        # verify path exists if not exists path makers the folders
        if not os.path.exists(path):
            os.makedirs(path, 0774)
            os.chmod(path, 0774)
        # verify aggregate options to name of file
        name = None
        if len(options) > 0:
            ext = archive.name.split('.')
            ext = ext[ext.__len__() - 1]
            ext = ext.lower()
            name = '%s.%s'%(options['name'], ext)
        else:
          name = archive.name
        filename = '%s%s'%(path, name)
        # recover full address of filename
        dirfilename = open(filename, "wb+")
        # walk all file and save im new address
        for bit in archive.chunks():
            dirfilename.write(bit)
        # close file
        dirfilename.close()
        # changes file permissions
        os.chmod(filename, 0777)
        return filename
    except Exception, e:
        print e

def removeTmp(absolutePath):
    try:
        os.remove(absolutePath)
    except Exception, e:
        raise e

def deleteFile(uriPath, partial=False):
    try:
        path = None
        # path absolute
        if partial:
            path = '%s%s'%(settings.MEDIA_ROOT, uriPath)
        else:
            path = uriPath
        if path is not None:
            print os.remove(path)
        else:
            return False
    except Exception, e:
        print e
        return False

def fileExists(paths, partial=False):
    try:
        if partial:
            # path absolute
            path = '%s%s'%(settings.MEDIA_ROOT, paths)
        else:
            path = paths
        return os.path.lexists(path)
    except Exception, e:
        print e
        return False

def descompressRAR(filename, path_to_extract):
    try:
        if filename == '':
            return 'File name is nothing.'
        if path_to_extract == '':
            return 'Path to extract nothing.'
        if filename != '' and path_to_extract != '':
            path_to_extract = '%s%s'%(settings.MEDIA_ROOT, path_to_extract)
            cmd = 'unrar x -y %s %s'%(filename, path_to_extract)
            os.system(cmd)
            return 'success'
    except Exception, e:
        return e.__str__()

def listDir(path):
    r = ['<ul class="jqueryFileTree" style="display: none;">']
    try:
        r = ['<ul class="jqueryFileTree" style="display: none;">']
        #d = urllib.unquote(path) #request.POST.get('dir','c:\\temp'
        dirstart = str(settings.MEDIA_ROOT).split('/')[1]
        if not path.startswith('/%s/'%dirstart):
            path = '%s%s'%(settings.MEDIA_ROOT, path)
        path = urllib.unquote(path)
        for f in os.listdir(path):
            ff = os.path.join(path,f)
            if os.path.isdir(ff):
                r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
            else:
                e = os.path.splitext(f)[1][1:] # get .ext and remove dot
                media = ff.split('/media/')
                print media
                r.append('<li class="file ext_%s"><a href="#" rel="/media/%s">%s</a></li>' % (e,media[1],f))
        r.append('</ul>')
    except Exception, e:
        r.append('Could not load directory.')

    r.append('</ul>')
    return r