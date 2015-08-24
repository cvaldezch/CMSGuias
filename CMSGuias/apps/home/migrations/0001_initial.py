# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pais'
        db.create_table(u'home_pais', (
            ('pais_id', self.gf('django.db.models.fields.CharField')(max_length=3, primary_key=True)),
            ('paisnom', self.gf('django.db.models.fields.CharField')(max_length=56)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Pais'])

        # Adding model 'Departamento'
        db.create_table(u'home_departamento', (
            ('departamento_id', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True)),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Pais'])),
            ('depnom', self.gf('django.db.models.fields.CharField')(max_length=56)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Departamento'])

        # Adding model 'Provincia'
        db.create_table(u'home_provincia', (
            ('provincia_id', self.gf('django.db.models.fields.CharField')(max_length=3, primary_key=True)),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Departamento'])),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Pais'])),
            ('pronom', self.gf('django.db.models.fields.CharField')(max_length=56)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Provincia'])

        # Adding model 'Distrito'
        db.create_table(u'home_distrito', (
            ('distrito_id', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True)),
            ('provincia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Provincia'])),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Departamento'])),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Pais'])),
            ('distnom', self.gf('django.db.models.fields.CharField')(max_length=56)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Distrito'])

        # Adding model 'Unidade'
        db.create_table(u'home_unidade', (
            ('unidad_id', self.gf('django.db.models.fields.CharField')(max_length=7, primary_key=True)),
            ('uninom', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Unidade'])

        # Adding model 'MaterialeAuditLogEntry'
        db.create_table(u'home_materialeauditlogentry', (
            ('materiales_id', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('matnom', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('matmed', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('unidad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Unidade'])),
            ('matacb', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('matare', self.gf('django.db.models.fields.FloatField')(null=True)),
            (u'action_user', self.gf('audit_log.models.fields.LastUserField')(related_name=u'_materiale_audit_log_entry', to=orm['auth.User'])),
            (u'action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'home', ['MaterialeAuditLogEntry'])

        # Adding model 'Materiale'
        db.create_table(u'home_materiale', (
            ('materiales_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15, primary_key=True)),
            ('matnom', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('matmed', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('unidad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Unidade'])),
            ('matacb', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('matare', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal(u'home', ['Materiale'])

        # Adding model 'TypeGroup'
        db.create_table(u'home_typegroup', (
            ('tgroup_id', self.gf('django.db.models.fields.CharField')(max_length=7, primary_key=True)),
            ('typeg', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['TypeGroup'])

        # Adding model 'GroupMaterials'
        db.create_table(u'home_groupmaterials', (
            ('mgroup_id', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True)),
            ('tgroup', self.gf('django.db.models.fields.related.ForeignKey')(default='TG00000', to=orm['home.TypeGroup'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('materials', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Materiale'])),
            ('observation', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['GroupMaterials'])

        # Adding model 'DetailsGroup'
        db.create_table(u'home_detailsgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mgroup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.GroupMaterials'])),
            ('materials', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Materiale'])),
            ('quantity', self.gf('django.db.models.fields.FloatField')()),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['DetailsGroup'])

        # Adding model 'Cargo'
        db.create_table(u'home_cargo', (
            ('cargo_id', self.gf('django.db.models.fields.CharField')(max_length=9, primary_key=True)),
            ('cargos', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('area', self.gf('django.db.models.fields.CharField')(default='Nothing', max_length=60)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(default='HH', to=orm['home.Unidade'], null=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Cargo'])

        # Adding model 'EmployeeAuditLogEntry'
        db.create_table(u'home_employeeauditlogentry', (
            ('empdni_id', self.gf('django.db.models.fields.CharField')(max_length=8, db_index=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('register', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('birth', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=180)),
            ('charge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Cargo'])),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'action_user', self.gf('audit_log.models.fields.LastUserField')(related_name=u'_employee_audit_log_entry', to=orm['auth.User'])),
            (u'action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'home', ['EmployeeAuditLogEntry'])

        # Adding model 'Employee'
        db.create_table(u'home_employee', (
            ('empdni_id', self.gf('django.db.models.fields.CharField')(max_length=8, primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('register', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('birth', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=180)),
            ('charge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Cargo'])),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Employee'])

        # Adding model 'userProfile'
        db.create_table(u'home_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('empdni', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Employee'])),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'home', ['userProfile'])

        # Adding model 'Almacene'
        db.create_table(u'home_almacene', (
            ('almacen_id', self.gf('django.db.models.fields.CharField')(max_length=4, primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Almacene'])

        # Adding model 'Transportista'
        db.create_table(u'home_transportista', (
            ('traruc_id', self.gf('django.db.models.fields.CharField')(max_length=11, primary_key=True)),
            ('tranom', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('tratel', self.gf('django.db.models.fields.CharField')(default='000-000-000', max_length=11, null=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Transportista'])

        # Adding model 'Conductore'
        db.create_table(u'home_conductore', (
            ('traruc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Transportista'])),
            ('condni_id', self.gf('django.db.models.fields.CharField')(max_length=8, primary_key=True)),
            ('connom', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('conlic', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('coninscription', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('contel', self.gf('django.db.models.fields.CharField')(default='', max_length=11, null=True, blank=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Conductore'])

        # Adding model 'Transporte'
        db.create_table(u'home_transporte', (
            ('traruc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Transportista'])),
            ('nropla_id', self.gf('django.db.models.fields.CharField')(max_length=8, primary_key=True)),
            ('marca', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Transporte'])

        # Adding model 'ClienteAuditLogEntry'
        db.create_table(u'home_clienteauditlogentry', (
            ('ruccliente_id', self.gf('django.db.models.fields.CharField')(max_length=11, db_index=True)),
            ('razonsocial', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Pais'])),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Departamento'])),
            ('provincia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Provincia'])),
            ('distrito', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Distrito'])),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('telefono', self.gf('django.db.models.fields.CharField')(default='000-000-000', max_length=30, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'action_user', self.gf('audit_log.models.fields.LastUserField')(related_name=u'_cliente_audit_log_entry', to=orm['auth.User'])),
            (u'action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'home', ['ClienteAuditLogEntry'])

        # Adding model 'Cliente'
        db.create_table(u'home_cliente', (
            ('ruccliente_id', self.gf('django.db.models.fields.CharField')(max_length=11, primary_key=True)),
            ('razonsocial', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Pais'])),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Departamento'])),
            ('provincia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Provincia'])),
            ('distrito', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Distrito'])),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('telefono', self.gf('django.db.models.fields.CharField')(default='000-000-000', max_length=30, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Cliente'])

        # Adding model 'Brand'
        db.create_table(u'home_brand', (
            ('brand_id', self.gf('django.db.models.fields.CharField')(max_length=5, primary_key=True)),
            ('brand', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Brand'])

        # Adding model 'Model'
        db.create_table(u'home_model', (
            ('model_id', self.gf('django.db.models.fields.CharField')(max_length=5, primary_key=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Brand'])),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Model'])

        # Adding model 'BrandMaterial'
        db.create_table(u'home_brandmaterial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('materiales', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Materiale'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Brand'])),
        ))
        db.send_create_signal(u'home', ['BrandMaterial'])

        # Adding model 'Herramientas'
        db.create_table(u'home_herramientas', (
            ('herramientas_id', self.gf('django.db.models.fields.CharField')(max_length=14, primary_key=True)),
            ('herramientas', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('medida', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('unidad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Unidade'])),
            ('tvida', self.gf('django.db.models.fields.IntegerField')()),
            ('acabado', self.gf('django.db.models.fields.CharField')(max_length=13)),
        ))
        db.send_create_signal(u'home', ['Herramientas'])

        # Adding model 'Documentos'
        db.create_table(u'home_documentos', (
            ('documento_id', self.gf('django.db.models.fields.CharField')(max_length=4, primary_key=True)),
            ('documento', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Documentos'])

        # Adding model 'FormaPago'
        db.create_table(u'home_formapago', (
            ('pagos_id', self.gf('django.db.models.fields.CharField')(max_length=4, primary_key=True)),
            ('pagos', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('valor', self.gf('django.db.models.fields.FloatField')()),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['FormaPago'])

        # Adding model 'Moneda'
        db.create_table(u'home_moneda', (
            ('moneda_id', self.gf('django.db.models.fields.CharField')(max_length=4, primary_key=True)),
            ('moneda', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('simbolo', self.gf('django.db.models.fields.CharField')(default='', max_length=5)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Moneda'])

        # Adding model 'TipoCambio'
        db.create_table(u'home_tipocambio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('moneda', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Moneda'])),
            ('fecha', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('registrado', self.gf('django.db.models.fields.TimeField')(auto_now=True, blank=True)),
            ('compra', self.gf('django.db.models.fields.FloatField')()),
            ('venta', self.gf('django.db.models.fields.FloatField')()),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['TipoCambio'])

        # Adding model 'Proveedor'
        db.create_table(u'home_proveedor', (
            ('proveedor_id', self.gf('django.db.models.fields.CharField')(max_length=11, primary_key=True)),
            ('razonsocial', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Pais'])),
            ('departamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Departamento'])),
            ('provincia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Provincia'])),
            ('distrito', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Distrito'])),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('origen', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(default='ejemplo@dominio.com', max_length=60)),
            ('contact', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Proveedor'])

        # Adding model 'LoginProveedor'
        db.create_table(u'home_loginproveedor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Proveedor'])),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'home', ['LoginProveedor'])

        # Adding model 'Configuracion'
        db.create_table(u'home_configuracion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('periodo', self.gf('django.db.models.fields.CharField')(default='', max_length=4)),
            ('registrado', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('moneda', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Moneda'])),
            ('igv', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal(u'home', ['Configuracion'])

        # Adding model 'Emails'
        db.create_table(u'home_emails', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('empdni', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Employee'])),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('fors', self.gf('django.db.models.fields.TextField')()),
            ('cc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cco', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('issue', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'home', ['Emails'])

        # Adding model 'Company'
        db.create_table(u'home_company', (
            ('ruc', self.gf('django.db.models.fields.CharField')(max_length=11, primary_key=True)),
            ('companyname', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('phone', self.gf('django.db.models.fields.CharField')(default='000-000', max_length=60, null=True, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
        ))
        db.send_create_signal(u'home', ['Company'])

        # Adding model 'KeyConfirmAuditLogEntry'
        db.create_table(u'home_keyconfirmauditlogentry', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('empdni', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Employee'])),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('desc', self.gf('django.db.models.fields.CharField')(default='', max_length=40, null=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'action_user', self.gf('audit_log.models.fields.LastUserField')(related_name=u'_keyconfirm_audit_log_entry', to=orm['auth.User'])),
            (u'action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'home', ['KeyConfirmAuditLogEntry'])

        # Adding model 'KeyConfirm'
        db.create_table(u'home_keyconfirm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('empdni', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Employee'])),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('desc', self.gf('django.db.models.fields.CharField')(default='', max_length=40, null=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'home', ['KeyConfirm'])

        # Adding model 'ToolsAuditLogEntry'
        db.create_table(u'home_toolsauditlogentry', (
            ('tools_id', self.gf('django.db.models.fields.CharField')(max_length=14, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('measure', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Unidade'])),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'action_user', self.gf('audit_log.models.fields.LastUserField')(related_name=u'_tools_audit_log_entry', to=orm['auth.User'])),
            (u'action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'home', ['ToolsAuditLogEntry'])

        # Adding model 'Tools'
        db.create_table(u'home_tools', (
            ('tools_id', self.gf('django.db.models.fields.CharField')(max_length=14, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('measure', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Unidade'])),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Tools'])


    def backwards(self, orm):
        # Deleting model 'Pais'
        db.delete_table(u'home_pais')

        # Deleting model 'Departamento'
        db.delete_table(u'home_departamento')

        # Deleting model 'Provincia'
        db.delete_table(u'home_provincia')

        # Deleting model 'Distrito'
        db.delete_table(u'home_distrito')

        # Deleting model 'Unidade'
        db.delete_table(u'home_unidade')

        # Deleting model 'MaterialeAuditLogEntry'
        db.delete_table(u'home_materialeauditlogentry')

        # Deleting model 'Materiale'
        db.delete_table(u'home_materiale')

        # Deleting model 'TypeGroup'
        db.delete_table(u'home_typegroup')

        # Deleting model 'GroupMaterials'
        db.delete_table(u'home_groupmaterials')

        # Deleting model 'DetailsGroup'
        db.delete_table(u'home_detailsgroup')

        # Deleting model 'Cargo'
        db.delete_table(u'home_cargo')

        # Deleting model 'EmployeeAuditLogEntry'
        db.delete_table(u'home_employeeauditlogentry')

        # Deleting model 'Employee'
        db.delete_table(u'home_employee')

        # Deleting model 'userProfile'
        db.delete_table(u'home_userprofile')

        # Deleting model 'Almacene'
        db.delete_table(u'home_almacene')

        # Deleting model 'Transportista'
        db.delete_table(u'home_transportista')

        # Deleting model 'Conductore'
        db.delete_table(u'home_conductore')

        # Deleting model 'Transporte'
        db.delete_table(u'home_transporte')

        # Deleting model 'ClienteAuditLogEntry'
        db.delete_table(u'home_clienteauditlogentry')

        # Deleting model 'Cliente'
        db.delete_table(u'home_cliente')

        # Deleting model 'Brand'
        db.delete_table(u'home_brand')

        # Deleting model 'Model'
        db.delete_table(u'home_model')

        # Deleting model 'BrandMaterial'
        db.delete_table(u'home_brandmaterial')

        # Deleting model 'Herramientas'
        db.delete_table(u'home_herramientas')

        # Deleting model 'Documentos'
        db.delete_table(u'home_documentos')

        # Deleting model 'FormaPago'
        db.delete_table(u'home_formapago')

        # Deleting model 'Moneda'
        db.delete_table(u'home_moneda')

        # Deleting model 'TipoCambio'
        db.delete_table(u'home_tipocambio')

        # Deleting model 'Proveedor'
        db.delete_table(u'home_proveedor')

        # Deleting model 'LoginProveedor'
        db.delete_table(u'home_loginproveedor')

        # Deleting model 'Configuracion'
        db.delete_table(u'home_configuracion')

        # Deleting model 'Emails'
        db.delete_table(u'home_emails')

        # Deleting model 'Company'
        db.delete_table(u'home_company')

        # Deleting model 'KeyConfirmAuditLogEntry'
        db.delete_table(u'home_keyconfirmauditlogentry')

        # Deleting model 'KeyConfirm'
        db.delete_table(u'home_keyconfirm')

        # Deleting model 'ToolsAuditLogEntry'
        db.delete_table(u'home_toolsauditlogentry')

        # Deleting model 'Tools'
        db.delete_table(u'home_tools')


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
        u'home.almacene': {
            'Meta': {'ordering': "['nombre']", 'object_name': 'Almacene'},
            'almacen_id': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'home.brand': {
            'Meta': {'object_name': 'Brand'},
            'brand': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'brand_id': ('django.db.models.fields.CharField', [], {'max_length': '5', 'primary_key': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'home.brandmaterial': {
            'Meta': {'object_name': 'BrandMaterial'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Brand']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materiales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"})
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
        u'home.clienteauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'ClienteAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_cliente_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Departamento']"}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'distrito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Distrito']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Pais']"}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Provincia']"}),
            'razonsocial': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ruccliente_id': ('django.db.models.fields.CharField', [], {'max_length': '11', 'db_index': 'True'}),
            'telefono': ('django.db.models.fields.CharField', [], {'default': "'000-000-000'", 'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        u'home.company': {
            'Meta': {'object_name': 'Company'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'companyname': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "'000-000'", 'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'ruc': ('django.db.models.fields.CharField', [], {'max_length': '11', 'primary_key': 'True'})
        },
        u'home.conductore': {
            'Meta': {'object_name': 'Conductore'},
            'condni_id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'primary_key': 'True'}),
            'coninscription': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'conlic': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'connom': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'contel': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'traruc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Transportista']"})
        },
        u'home.configuracion': {
            'Meta': {'object_name': 'Configuracion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'igv': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'moneda': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Moneda']"}),
            'periodo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4'}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'home.departamento': {
            'Meta': {'ordering': "['depnom']", 'object_name': 'Departamento'},
            'departamento_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'depnom': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Pais']"})
        },
        u'home.detailsgroup': {
            'Meta': {'object_name': 'DetailsGroup'},
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'mgroup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.GroupMaterials']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {})
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
        u'home.emails': {
            'Meta': {'object_name': 'Emails'},
            'account': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cco': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'empdni': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Employee']"}),
            'fors': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'home.employee': {
            'Meta': {'ordering': "['lastname']", 'object_name': 'Employee'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '180'}),
            'birth': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'charge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Cargo']"}),
            'empdni_id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'primary_key': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'home.employeeauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'EmployeeAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_employee_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '180'}),
            'birth': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'charge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Cargo']"}),
            'empdni_id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'home.formapago': {
            'Meta': {'object_name': 'FormaPago'},
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pagos': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'pagos_id': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'valor': ('django.db.models.fields.FloatField', [], {})
        },
        u'home.groupmaterials': {
            'Meta': {'object_name': 'GroupMaterials'},
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'mgroup_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'observation': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'tgroup': ('django.db.models.fields.related.ForeignKey', [], {'default': "'TG00000'", 'to': u"orm['home.TypeGroup']"})
        },
        u'home.herramientas': {
            'Meta': {'object_name': 'Herramientas'},
            'acabado': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'herramientas': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'herramientas_id': ('django.db.models.fields.CharField', [], {'max_length': '14', 'primary_key': 'True'}),
            'medida': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'tvida': ('django.db.models.fields.IntegerField', [], {}),
            'unidad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Unidade']"})
        },
        u'home.keyconfirm': {
            'Meta': {'object_name': 'KeyConfirm'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'empdni': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Employee']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        u'home.keyconfirmauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'KeyConfirmAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_keyconfirm_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'empdni': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Employee']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        u'home.loginproveedor': {
            'Meta': {'object_name': 'LoginProveedor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Proveedor']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '16'})
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
        u'home.materialeauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'MaterialeAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_materiale_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'matacb': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'matare': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'materiales_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
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
        u'home.proveedor': {
            'Meta': {'ordering': "['razonsocial']", 'object_name': 'Proveedor'},
            'contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Departamento']"}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'distrito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Distrito']"}),
            'email': ('django.db.models.fields.CharField', [], {'default': "'ejemplo@dominio.com'", 'max_length': '60'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'origen': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Pais']"}),
            'proveedor_id': ('django.db.models.fields.CharField', [], {'max_length': '11', 'primary_key': 'True'}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Provincia']"}),
            'razonsocial': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        u'home.provincia': {
            'Meta': {'ordering': "['pronom']", 'object_name': 'Provincia'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Departamento']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Pais']"}),
            'pronom': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'provincia_id': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'})
        },
        u'home.tipocambio': {
            'Meta': {'object_name': 'TipoCambio'},
            'compra': ('django.db.models.fields.FloatField', [], {}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moneda': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Moneda']"}),
            'registrado': ('django.db.models.fields.TimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'venta': ('django.db.models.fields.FloatField', [], {})
        },
        u'home.tools': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tools'},
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'measure': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tools_id': ('django.db.models.fields.CharField', [], {'max_length': '14', 'primary_key': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Unidade']"})
        },
        u'home.toolsauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'ToolsAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_tools_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'measure': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tools_id': ('django.db.models.fields.CharField', [], {'max_length': '14', 'db_index': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Unidade']"})
        },
        u'home.transporte': {
            'Meta': {'object_name': 'Transporte'},
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'marca': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'nropla_id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'primary_key': 'True'}),
            'traruc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Transportista']"})
        },
        u'home.transportista': {
            'Meta': {'object_name': 'Transportista'},
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tranom': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'traruc_id': ('django.db.models.fields.CharField', [], {'max_length': '11', 'primary_key': 'True'}),
            'tratel': ('django.db.models.fields.CharField', [], {'default': "'000-000-000'", 'max_length': '11', 'null': 'True'})
        },
        u'home.typegroup': {
            'Meta': {'object_name': 'TypeGroup'},
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tgroup_id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'}),
            'typeg': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'home.unidade': {
            'Meta': {'object_name': 'Unidade'},
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'unidad_id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'}),
            'uninom': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'home.userprofile': {
            'Meta': {'object_name': 'userProfile'},
            'empdni': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Employee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['home']