# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProyectoAuditLogEntry'
        db.create_table(u'ventas_proyectoauditlogentry', (
            ('proyecto_id', self.gf('django.db.models.fields.CharField')(max_length=7, db_index=True)),
            ('ruccliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Cliente'], null=True)),
            ('nompro', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('registrado', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('comienzo', self.gf('django.db.models.fields.DateField')(null=True)),
            ('fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Pais'])),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Departamento'])),
            ('provincia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Provincia'])),
            ('distrito', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Distrito'])),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('obser', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='00', max_length=2)),
            ('empdni', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'_auditlog_proyectoAsEmployee', null=True, to=orm['home.Employee'])),
            ('approved', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'_auditlog_approvedAsEmployee', null=True, to=orm['home.Employee'])),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Moneda'], null=True, blank=True)),
            ('exchange', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('typep', self.gf('django.db.models.fields.CharField')(default='ACI', max_length=3)),
            ('contact', self.gf('django.db.models.fields.CharField')(default='', max_length=254, null=True, blank=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'action_user', self.gf('audit_log.models.fields.LastUserField')(related_name=u'_proyecto_audit_log_entry', to=orm['auth.User'])),
            (u'action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'ventas', ['ProyectoAuditLogEntry'])

        # Adding model 'Proyecto'
        db.create_table(u'ventas_proyecto', (
            ('proyecto_id', self.gf('django.db.models.fields.CharField')(max_length=7, primary_key=True)),
            ('ruccliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Cliente'], null=True)),
            ('nompro', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('registrado', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('comienzo', self.gf('django.db.models.fields.DateField')(null=True)),
            ('fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Pais'])),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Departamento'])),
            ('provincia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Provincia'])),
            ('distrito', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Distrito'])),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('obser', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='00', max_length=2)),
            ('empdni', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='proyectoAsEmployee', null=True, to=orm['home.Employee'])),
            ('approved', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='approvedAsEmployee', null=True, to=orm['home.Employee'])),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Moneda'], null=True, blank=True)),
            ('exchange', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('typep', self.gf('django.db.models.fields.CharField')(default='ACI', max_length=3)),
            ('contact', self.gf('django.db.models.fields.CharField')(default='', max_length=254, null=True, blank=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'ventas', ['Proyecto'])

        # Adding model 'CloseProject'
        db.create_table(u'ventas_closeproject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Proyecto'])),
            ('storageclose', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('datestorage', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('letterdelivery', self.gf('django.db.models.fields.files.FileField')(max_length=250, null=True)),
            ('dateletter', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('documents', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accounting', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tinvoice', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('tiva', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('otherin', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('otherout', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('retention', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('fileaccounting', self.gf('django.db.models.fields.files.FileField')(max_length=250, null=True)),
            ('closeconfirm', self.gf('django.db.models.fields.CharField')(default='', max_length=6, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='PE', max_length=2, blank=True)),
            ('performedstorage', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='storage', null=True, to=orm['home.Employee'])),
            ('performedoperations', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='operations', null=True, to=orm['home.Employee'])),
            ('performeddocument', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='documents', null=True, to=orm['home.Employee'])),
            ('performedaccounting', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='accounting', null=True, to=orm['home.Employee'])),
            ('performedclose', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='closeasproject', null=True, to=orm['home.Employee'])),
        ))
        db.send_create_signal(u'ventas', ['CloseProject'])

        # Adding model 'SubproyectoAuditLogEntry'
        db.create_table(u'ventas_subproyectoauditlogentry', (
            ('subproyecto_id', self.gf('django.db.models.fields.CharField')(max_length=7, db_index=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Proyecto'])),
            ('nomsub', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('registrado', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('comienzo', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('obser', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='AC', max_length=2)),
            ('additional', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'action_user', self.gf('audit_log.models.fields.LastUserField')(related_name=u'_subproyecto_audit_log_entry', to=orm['auth.User'])),
            (u'action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'ventas', ['SubproyectoAuditLogEntry'])

        # Adding model 'Subproyecto'
        db.create_table(u'ventas_subproyecto', (
            ('subproyecto_id', self.gf('django.db.models.fields.CharField')(max_length=7, primary_key=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Proyecto'])),
            ('nomsub', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('registrado', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('comienzo', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('obser', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='AC', max_length=2)),
            ('additional', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'ventas', ['Subproyecto'])

        # Adding model 'SectoreAuditLogEntry'
        db.create_table(u'ventas_sectoreauditlogentry', (
            ('sector_id', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Proyecto'])),
            ('subproyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Subproyecto'], null=True, blank=True)),
            ('planoid', self.gf('django.db.models.fields.CharField')(default='', max_length=16, null=True)),
            ('nomsec', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('registrado', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('comienzo', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('obser', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('amountsales', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('atype', self.gf('django.db.models.fields.CharField')(default='NN', max_length=2, blank=True)),
            ('link', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='AC', max_length=2)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'action_user', self.gf('audit_log.models.fields.LastUserField')(related_name=u'_sectore_audit_log_entry', to=orm['auth.User'])),
            (u'action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'ventas', ['SectoreAuditLogEntry'])

        # Adding model 'Sectore'
        db.create_table(u'ventas_sectore', (
            ('sector_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20, primary_key=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Proyecto'])),
            ('subproyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Subproyecto'], null=True, blank=True)),
            ('planoid', self.gf('django.db.models.fields.CharField')(default='', max_length=16, null=True)),
            ('nomsec', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('registrado', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('comienzo', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('obser', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('amountsales', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('atype', self.gf('django.db.models.fields.CharField')(default='NN', max_length=2, blank=True)),
            ('link', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='AC', max_length=2)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'ventas', ['Sectore'])

        # Adding model 'SectorFiles'
        db.create_table(u'ventas_sectorfiles', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Sectore'])),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Proyecto'])),
            ('subproyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Subproyecto'], null=True, blank=True)),
            ('files', self.gf('django.db.models.fields.files.FileField')(max_length=200)),
            ('note', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2015, 8, 3, 0, 0), auto_now=True, blank=True)),
            ('time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(10, 25, 28, 301235), auto_now=True, blank=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'ventas', ['SectorFiles'])

        # Adding model 'MetradoventaAuditLogEntry'
        db.create_table(u'ventas_metradoventaauditlogentry', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Proyecto'])),
            ('subproyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Subproyecto'], null=True, blank=True)),
            ('sector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Sectore'])),
            ('materiales', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Materiale'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(default='BR000', to=orm['home.Brand'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(default='MO000', to=orm['home.Model'])),
            ('cantidad', self.gf('django.db.models.fields.FloatField')()),
            ('precio', self.gf('django.db.models.fields.FloatField')()),
            ('sales', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'action_user', self.gf('audit_log.models.fields.LastUserField')(related_name=u'_metradoventa_audit_log_entry', to=orm['auth.User'])),
            (u'action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'ventas', ['MetradoventaAuditLogEntry'])

        # Adding model 'Metradoventa'
        db.create_table(u'ventas_metradoventa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Proyecto'])),
            ('subproyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Subproyecto'], null=True, blank=True)),
            ('sector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Sectore'])),
            ('materiales', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Materiale'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(default='BR000', to=orm['home.Brand'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(default='MO000', to=orm['home.Model'])),
            ('cantidad', self.gf('django.db.models.fields.FloatField')()),
            ('precio', self.gf('django.db.models.fields.FloatField')()),
            ('sales', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'ventas', ['Metradoventa'])

        # Adding model 'Alertasproyecto'
        db.create_table(u'ventas_alertasproyecto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Proyecto'])),
            ('subproyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Subproyecto'], null=True, blank=True)),
            ('sector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Sectore'], null=True, blank=True)),
            ('registrado', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('empdni', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Employee'])),
            ('charge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Cargo'])),
            ('message', self.gf('django.db.models.fields.TextField')(default='')),
            ('status', self.gf('django.db.models.fields.CharField')(default='success', max_length=8)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'ventas', ['Alertasproyecto'])

        # Adding model 'HistoryMetProject'
        db.create_table(u'ventas_historymetproject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('token', self.gf('django.db.models.fields.CharField')(default='8KT3Y4', max_length=6)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['ventas.Proyecto'])),
            ('subproyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Subproyecto'], null=True, blank=True)),
            ('sector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Sectore'])),
            ('materials', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['home.Materiale'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(default='BR000', to=orm['home.Brand'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(default='MO000', to=orm['home.Model'])),
            ('quantity', self.gf('django.db.models.fields.FloatField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('sales', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('comment', self.gf('django.db.models.fields.CharField')(default='', max_length=250, null=True, blank=True)),
            ('quantityorders', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('tag', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'ventas', ['HistoryMetProject'])

        # Adding model 'RestoreStorage'
        db.create_table(u'ventas_restorestorage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('token', self.gf('django.db.models.fields.CharField')(default='L1F7KZ', max_length=6)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['ventas.Proyecto'])),
            ('subproyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Subproyecto'], null=True, blank=True)),
            ('sector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Sectore'])),
            ('materials', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['home.Materiale'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(default='BR000', to=orm['home.Brand'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(default='MO000', to=orm['home.Model'])),
            ('quantity', self.gf('django.db.models.fields.FloatField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('sales', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=9, decimal_places=3, blank=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'ventas', ['RestoreStorage'])

        # Adding model 'UpdateMetProjectAuditLogEntry'
        db.create_table(u'ventas_updatemetprojectauditlogentry', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['ventas.Proyecto'])),
            ('subproyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Subproyecto'], null=True, blank=True)),
            ('sector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Sectore'])),
            ('materials', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['home.Materiale'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(default='BR000', to=orm['home.Brand'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(default='MO000', to=orm['home.Model'])),
            ('quantity', self.gf('django.db.models.fields.FloatField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('sales', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(default='', max_length=250, null=True, blank=True)),
            ('quantityorders', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'action_user', self.gf('audit_log.models.fields.LastUserField')(related_name=u'_updatemetproject_audit_log_entry', to=orm['auth.User'])),
            (u'action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'ventas', ['UpdateMetProjectAuditLogEntry'])

        # Adding model 'UpdateMetProject'
        db.create_table(u'ventas_updatemetproject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['ventas.Proyecto'])),
            ('subproyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Subproyecto'], null=True, blank=True)),
            ('sector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Sectore'])),
            ('materials', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['home.Materiale'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(default='BR000', to=orm['home.Brand'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(default='MO000', to=orm['home.Model'])),
            ('quantity', self.gf('django.db.models.fields.FloatField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('sales', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(default='', max_length=250, null=True, blank=True)),
            ('quantityorders', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'ventas', ['UpdateMetProject'])

        # Adding model 'PurchaseOrderAuditLogEntry'
        db.create_table(u'ventas_purchaseorderauditlogentry', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Proyecto'])),
            ('register', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('nropurchase', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('issued', self.gf('django.db.models.fields.DateField')()),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Moneda'])),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Documentos'])),
            ('method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.FormaPago'])),
            ('observation', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dsct', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('igv', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('order', self.gf('django.db.models.fields.files.FileField')(max_length=200, null=True, blank=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'action_user', self.gf('audit_log.models.fields.LastUserField')(related_name=u'_purchaseorder_audit_log_entry', to=orm['auth.User'])),
            (u'action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'ventas', ['PurchaseOrderAuditLogEntry'])

        # Adding model 'PurchaseOrder'
        db.create_table(u'ventas_purchaseorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Proyecto'])),
            ('register', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('nropurchase', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('issued', self.gf('django.db.models.fields.DateField')()),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Moneda'])),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Documentos'])),
            ('method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.FormaPago'])),
            ('observation', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dsct', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('igv', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('order', self.gf('django.db.models.fields.files.FileField')(max_length=200, null=True, blank=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'ventas', ['PurchaseOrder'])

        # Adding model 'DetailsPurchaseOrderAuditLogEntry'
        db.create_table(u'ventas_detailspurchaseorderauditlogentry', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('purchase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.PurchaseOrder'])),
            ('nropurchase', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Unidade'])),
            ('delivery', self.gf('django.db.models.fields.DateField')()),
            ('quantity', self.gf('django.db.models.fields.FloatField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            (u'action_user', self.gf('audit_log.models.fields.LastUserField')(related_name=u'_detailspurchaseorder_audit_log_entry', to=orm['auth.User'])),
            (u'action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'ventas', ['DetailsPurchaseOrderAuditLogEntry'])

        # Adding model 'DetailsPurchaseOrder'
        db.create_table(u'ventas_detailspurchaseorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('purchase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.PurchaseOrder'])),
            ('nropurchase', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Unidade'])),
            ('delivery', self.gf('django.db.models.fields.DateField')()),
            ('quantity', self.gf('django.db.models.fields.FloatField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'ventas', ['DetailsPurchaseOrder'])


    def backwards(self, orm):
        # Deleting model 'ProyectoAuditLogEntry'
        db.delete_table(u'ventas_proyectoauditlogentry')

        # Deleting model 'Proyecto'
        db.delete_table(u'ventas_proyecto')

        # Deleting model 'CloseProject'
        db.delete_table(u'ventas_closeproject')

        # Deleting model 'SubproyectoAuditLogEntry'
        db.delete_table(u'ventas_subproyectoauditlogentry')

        # Deleting model 'Subproyecto'
        db.delete_table(u'ventas_subproyecto')

        # Deleting model 'SectoreAuditLogEntry'
        db.delete_table(u'ventas_sectoreauditlogentry')

        # Deleting model 'Sectore'
        db.delete_table(u'ventas_sectore')

        # Deleting model 'SectorFiles'
        db.delete_table(u'ventas_sectorfiles')

        # Deleting model 'MetradoventaAuditLogEntry'
        db.delete_table(u'ventas_metradoventaauditlogentry')

        # Deleting model 'Metradoventa'
        db.delete_table(u'ventas_metradoventa')

        # Deleting model 'Alertasproyecto'
        db.delete_table(u'ventas_alertasproyecto')

        # Deleting model 'HistoryMetProject'
        db.delete_table(u'ventas_historymetproject')

        # Deleting model 'RestoreStorage'
        db.delete_table(u'ventas_restorestorage')

        # Deleting model 'UpdateMetProjectAuditLogEntry'
        db.delete_table(u'ventas_updatemetprojectauditlogentry')

        # Deleting model 'UpdateMetProject'
        db.delete_table(u'ventas_updatemetproject')

        # Deleting model 'PurchaseOrderAuditLogEntry'
        db.delete_table(u'ventas_purchaseorderauditlogentry')

        # Deleting model 'PurchaseOrder'
        db.delete_table(u'ventas_purchaseorder')

        # Deleting model 'DetailsPurchaseOrderAuditLogEntry'
        db.delete_table(u'ventas_detailspurchaseorderauditlogentry')

        # Deleting model 'DetailsPurchaseOrder'
        db.delete_table(u'ventas_detailspurchaseorder')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'home.brand': {
            'Meta': {'object_name': 'Brand'},
            'brand': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'brand_id': ('django.db.models.fields.CharField', [], {'max_length': '5', 'primary_key': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'home.cargo': {
            'Meta': {'ordering': "['cargos']", 'object_name': 'Cargo'},
            'area': ('django.db.models.fields.CharField', [], {'default': "'Nothing'", 'max_length': '60'}),
            'cargo_id': ('django.db.models.fields.CharField', [], {'max_length': '9', 'primary_key': 'True'}),
            'cargos': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'default': "'HH'", 'to': u"orm['home.Unidade']", 'null': 'True'})
        },
        u'home.cliente': {
            'Meta': {'ordering': "['razonsocial']", 'object_name': 'Cliente'},
            'contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Departamento']"}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'distrito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Distrito']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Pais']"}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Provincia']"}),
            'razonsocial': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ruccliente_id': ('django.db.models.fields.CharField', [], {'max_length': '11', 'primary_key': 'True'}),
            'telefono': ('django.db.models.fields.CharField', [], {'default': "'000-000-000'", 'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        u'home.departamento': {
            'Meta': {'ordering': "['depnom']", 'object_name': 'Departamento'},
            'departamento_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'depnom': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Pais']"})
        },
        u'home.distrito': {
            'Meta': {'ordering': "['distnom']", 'object_name': 'Distrito'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Departamento']"}),
            'distnom': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'distrito_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Pais']"}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Provincia']"})
        },
        u'home.documentos': {
            'Meta': {'object_name': 'Documentos'},
            'documento': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'documento_id': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'home.employee': {
            'Meta': {'ordering': "['lastname']", 'object_name': 'Employee'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '180'}),
            'birth': ('django.db.models.fields.DateField', [], {}),
            'charge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Cargo']"}),
            'empdni_id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'primary_key': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'home.formapago': {
            'Meta': {'object_name': 'FormaPago'},
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pagos': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'pagos_id': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'valor': ('django.db.models.fields.FloatField', [], {})
        },
        u'home.materiale': {
            'Meta': {'ordering': "['matnom']", 'object_name': 'Materiale'},
            'matacb': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'matare': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'materiales_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15', 'primary_key': 'True'}),
            'matmed': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'matnom': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'unidad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Unidade']"})
        },
        u'home.model': {
            'Meta': {'object_name': 'Model'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Brand']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'model_id': ('django.db.models.fields.CharField', [], {'max_length': '5', 'primary_key': 'True'})
        },
        u'home.moneda': {
            'Meta': {'object_name': 'Moneda'},
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'moneda': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'moneda_id': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'simbolo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5'})
        },
        u'home.pais': {
            'Meta': {'ordering': "['paisnom']", 'object_name': 'Pais'},
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pais_id': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'paisnom': ('django.db.models.fields.CharField', [], {'max_length': '56'})
        },
        u'home.provincia': {
            'Meta': {'ordering': "['pronom']", 'object_name': 'Provincia'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Departamento']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Pais']"}),
            'pronom': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'provincia_id': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'})
        },
        u'home.unidade': {
            'Meta': {'object_name': 'Unidade'},
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'unidad_id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'}),
            'uninom': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'ventas.alertasproyecto': {
            'Meta': {'ordering': "['proyecto']", 'object_name': 'Alertasproyecto'},
            'charge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Cargo']"}),
            'empdni': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Employee']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'success'", 'max_length': '8'}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'})
        },
        u'ventas.closeproject': {
            'Meta': {'object_name': 'CloseProject'},
            'accounting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'closeconfirm': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '6', 'blank': 'True'}),
            'dateletter': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'datestorage': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'documents': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fileaccounting': ('django.db.models.fields.files.FileField', [], {'max_length': '250', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letterdelivery': ('django.db.models.fields.files.FileField', [], {'max_length': '250', 'null': 'True'}),
            'otherin': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'otherout': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'performedaccounting': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'accounting'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'performedclose': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'closeasproject'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'performeddocument': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'documents'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'performedoperations': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'operations'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'performedstorage': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'storage'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'retention': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PE'", 'max_length': '2', 'blank': 'True'}),
            'storageclose': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tinvoice': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'tiva': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'})
        },
        u'ventas.detailspurchaseorder': {
            'Meta': {'ordering': "['nropurchase']", 'object_name': 'DetailsPurchaseOrder'},
            'delivery': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nropurchase': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'purchase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.PurchaseOrder']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Unidade']"})
        },
        u'ventas.detailspurchaseorderauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'DetailsPurchaseOrderAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_detailspurchaseorder_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'delivery': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'nropurchase': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'purchase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.PurchaseOrder']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Unidade']"})
        },
        u'ventas.historymetproject': {
            'Meta': {'ordering': "['proyecto']", 'object_name': 'HistoryMetProject'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'BR000'", 'to': u"orm['home.Brand']"}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "'MO000'", 'to': u"orm['home.Model']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['ventas.Proyecto']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'quantityorders': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'sales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'8KT3Y4'", 'max_length': '6'})
        },
        u'ventas.metradoventa': {
            'Meta': {'ordering': "['proyecto']", 'object_name': 'Metradoventa'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'BR000'", 'to': u"orm['home.Brand']"}),
            'cantidad': ('django.db.models.fields.FloatField', [], {}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materiales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "'MO000'", 'to': u"orm['home.Model']"}),
            'precio': ('django.db.models.fields.FloatField', [], {}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'sales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'})
        },
        u'ventas.metradoventaauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'MetradoventaAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_metradoventa_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'BR000'", 'to': u"orm['home.Brand']"}),
            'cantidad': ('django.db.models.fields.FloatField', [], {}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'materiales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "'MO000'", 'to': u"orm['home.Model']"}),
            'precio': ('django.db.models.fields.FloatField', [], {}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'sales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'})
        },
        u'ventas.proyecto': {
            'Meta': {'ordering': "['nompro']", 'object_name': 'Proyecto'},
            'approved': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'approvedAsEmployee'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'comienzo': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Moneda']", 'null': 'True', 'blank': 'True'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Departamento']"}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'distrito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Distrito']"}),
            'empdni': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'proyectoAsEmployee'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'exchange': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nompro': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'obser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Pais']"}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Provincia']"}),
            'proyecto_id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'ruccliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Cliente']", 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'00'", 'max_length': '2'}),
            'typep': ('django.db.models.fields.CharField', [], {'default': "'ACI'", 'max_length': '3'})
        },
        u'ventas.proyectoauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'ProyectoAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_proyecto_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'approved': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'_auditlog_approvedAsEmployee'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'comienzo': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Moneda']", 'null': 'True', 'blank': 'True'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Departamento']"}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'distrito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Distrito']"}),
            'empdni': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'_auditlog_proyectoAsEmployee'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'exchange': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nompro': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'obser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Pais']"}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Provincia']"}),
            'proyecto_id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'db_index': 'True'}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'ruccliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Cliente']", 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'00'", 'max_length': '2'}),
            'typep': ('django.db.models.fields.CharField', [], {'default': "'ACI'", 'max_length': '3'})
        },
        u'ventas.purchaseorder': {
            'Meta': {'ordering': "['project']", 'object_name': 'PurchaseOrder'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Moneda']"}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Documentos']"}),
            'dsct': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'igv': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'issued': ('django.db.models.fields.DateField', [], {}),
            'method': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.FormaPago']"}),
            'nropurchase': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'observation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.files.FileField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'ventas.purchaseorderauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'PurchaseOrderAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_purchaseorder_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Moneda']"}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Documentos']"}),
            'dsct': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'igv': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'issued': ('django.db.models.fields.DateField', [], {}),
            'method': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.FormaPago']"}),
            'nropurchase': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'observation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.files.FileField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'ventas.restorestorage': {
            'Meta': {'ordering': "['proyecto']", 'object_name': 'RestoreStorage'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'BR000'", 'to': u"orm['home.Brand']"}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "'MO000'", 'to': u"orm['home.Model']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['ventas.Proyecto']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'sales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'L1F7KZ'", 'max_length': '6'})
        },
        u'ventas.sectore': {
            'Meta': {'ordering': "['sector_id']", 'object_name': 'Sectore'},
            'amount': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'amountsales': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'atype': ('django.db.models.fields.CharField', [], {'default': "'NN'", 'max_length': '2', 'blank': 'True'}),
            'comienzo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'nomsec': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'obser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'planoid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16', 'null': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sector_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'AC'", 'max_length': '2'}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'})
        },
        u'ventas.sectoreauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'SectoreAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_sectore_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'amount': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'amountsales': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'atype': ('django.db.models.fields.CharField', [], {'default': "'NN'", 'max_length': '2', 'blank': 'True'}),
            'comienzo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'nomsec': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'obser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'planoid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16', 'null': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sector_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'AC'", 'max_length': '2'}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'})
        },
        u'ventas.sectorfiles': {
            'Meta': {'object_name': 'SectorFiles'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 8, 3, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'files': ('django.db.models.fields.files.FileField', [], {'max_length': '200'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(10, 25, 28, 301235)', 'auto_now': 'True', 'blank': 'True'})
        },
        u'ventas.subproyecto': {
            'Meta': {'ordering': "['nomsub']", 'object_name': 'Subproyecto'},
            'additional': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comienzo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nomsub': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'obser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'AC'", 'max_length': '2'}),
            'subproyecto_id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'})
        },
        u'ventas.subproyectoauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'SubproyectoAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_subproyecto_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'additional': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comienzo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nomsub': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'obser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'AC'", 'max_length': '2'}),
            'subproyecto_id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'db_index': 'True'})
        },
        u'ventas.updatemetproject': {
            'Meta': {'ordering': "['proyecto']", 'object_name': 'UpdateMetProject'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'BR000'", 'to': u"orm['home.Brand']"}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "'MO000'", 'to': u"orm['home.Model']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['ventas.Proyecto']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'quantityorders': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'sales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'ventas.updatemetprojectauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'UpdateMetProjectAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_updatemetproject_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'BR000'", 'to': u"orm['home.Brand']"}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "'MO000'", 'to': u"orm['home.Model']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['ventas.Proyecto']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'quantityorders': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'sales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        }
    }

    complete_apps = ['ventas']