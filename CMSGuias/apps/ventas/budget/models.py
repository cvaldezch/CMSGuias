from django.db import models

from audit_log.models.fields import LastUserField
from audit_log.models.managers import AuditLog

from CMSGuias.apps.home.models import Unidade


class Analysis(models.Model):
    analysis_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=255, null=False)
    unit = models.ForeignKey(Unidade, to_field='unidad_id')
    yield = models.FloatField()
    register = models.DateField(auto_now=True)
    flag = models.BooleanField(default=True)

    audit_log = AuditLog()

    class Meta:
        ordering = ['analysis']

    def __unicode__(self):
        return '%s %s %s'%(self.analysis_id, self.name, self.register)