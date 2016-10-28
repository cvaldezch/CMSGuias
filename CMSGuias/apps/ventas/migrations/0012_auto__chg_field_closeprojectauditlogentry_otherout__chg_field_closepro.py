# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CloseProjectAuditLogEntry.otherout'
        db.alter_column(u'ventas_closeprojectauditlogentry', 'otherout', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'CloseProjectAuditLogEntry.retention'
        db.alter_column(u'ventas_closeprojectauditlogentry', 'retention', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'CloseProjectAuditLogEntry.otherin'
        db.alter_column(u'ventas_closeprojectauditlogentry', 'otherin', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'CloseProjectAuditLogEntry.tiva'
        db.alter_column(u'ventas_closeprojectauditlogentry', 'tiva', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'CloseProjectAuditLogEntry.tinvoice'
        db.alter_column(u'ventas_closeprojectauditlogentry', 'tinvoice', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'CloseProject.otherout'
        db.alter_column(u'ventas_closeproject', 'otherout', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'CloseProject.retention'
        db.alter_column(u'ventas_closeproject', 'retention', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'CloseProject.otherin'
        db.alter_column(u'ventas_closeproject', 'otherin', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'CloseProject.tiva'
        db.alter_column(u'ventas_closeproject', 'tiva', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'CloseProject.tinvoice'
        db.alter_column(u'ventas_closeproject', 'tinvoice', self.gf('django.db.models.fields.FloatField')(null=True))

    def backwards(self, orm):

        # Changing field 'CloseProjectAuditLogEntry.otherout'
        db.alter_column(u'ventas_closeprojectauditlogentry', 'otherout', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'CloseProjectAuditLogEntry.retention'
        db.alter_column(u'ventas_closeprojectauditlogentry', 'retention', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'CloseProjectAuditLogEntry.otherin'
        db.alter_column(u'ventas_closeprojectauditlogentry', 'otherin', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'CloseProjectAuditLogEntry.tiva'
        db.alter_column(u'ventas_closeprojectauditlogentry', 'tiva', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'CloseProjectAuditLogEntry.tinvoice'
        db.alter_column(u'ventas_closeprojectauditlogentry', 'tinvoice', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'CloseProject.otherout'
        db.alter_column(u'ventas_closeproject', 'otherout', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'CloseProject.retention'
        db.alter_column(u'ventas_closeproject', 'retention', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'CloseProject.otherin'
        db.alter_column(u'ventas_closeproject', 'otherin', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'CloseProject.tiva'
        db.alter_column(u'ventas_closeproject', 'tiva', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'CloseProject.tinvoice'
        db.alter_column(u'ventas_closeproject', 'tinvoice', self.gf('django.db.models.fields.FloatField')())

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
            'birth': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'charge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Cargo']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'empdni_id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'primary_key': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'fixed': ('django.db.models.fields.CharField', [], {'max_length': '26', 'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'observation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'phonejob': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
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
        u'operations.dsector': {
            'Meta': {'object_name': 'DSector'},
            'dateend': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'datestart': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dsector_id': ('django.db.models.fields.CharField', [], {'default': "'PRAA000VEN00SG0000DS000'", 'max_length': '23', 'primary_key': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'observation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'plane': ('django.db.models.fields.files.FileField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']", 'null': 'True', 'blank': 'True'}),
            'sgroup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operations.SGroup']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PE'", 'max_length': '2'})
        },
        u'operations.sgroup': {
            'Meta': {'object_name': 'SGroup'},
            'colour': ('django.db.models.fields.CharField', [], {'max_length': '21', 'null': 'True', 'blank': 'True'}),
            'dateend': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'datestart': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'observation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'sgroup_id': ('django.db.models.fields.CharField', [], {'default': "'PRAA000SG0000'", 'max_length': '18', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PE'", 'max_length': '2', 'blank': 'True'}),
            'subproject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'})
        },
        u'ventas.alertasproyecto': {
            'Meta': {'ordering': "[u'proyecto']", 'object_name': 'Alertasproyecto'},
            'charge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Cargo']"}),
            'empdni': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Employee']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'success'", 'max_length': '8'}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'})
        },
        u'ventas.closeproject': {
            'Meta': {'object_name': 'CloseProject'},
            'accounting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'closeconfirm': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '6', 'blank': 'True'}),
            'dateclose': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'dateletter': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'datereopen': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'datestorage': ('django.db.models.fields.DateTimeField', [], {}),
            'docregister': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'documents': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fileaccounting': ('django.db.models.fields.files.FileField', [], {'max_length': '250', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyreopens': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True'}),
            'letterdelivery': ('django.db.models.fields.files.FileField', [], {'max_length': '250', 'null': 'True'}),
            'otherin': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'otherout': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'performedaccounting': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'accounting'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'performedclose': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'closeasproject'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'performeddocument': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'documents'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'performedoperations': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'operations'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'performedre': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'reopen'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'performedstorage': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'storage'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'retention': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'PE'", 'max_length': '2'}),
            'storageclose': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tinvoice': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'tiva': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'ventas.closeprojectauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'CloseProjectAuditLogEntry'},
            'accounting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_closeproject_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'closeconfirm': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '6', 'blank': 'True'}),
            'dateclose': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'dateletter': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'datereopen': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'datestorage': ('django.db.models.fields.DateTimeField', [], {}),
            'docregister': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'documents': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fileaccounting': ('django.db.models.fields.files.FileField', [], {'max_length': '250', 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'keyreopens': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True'}),
            'letterdelivery': ('django.db.models.fields.files.FileField', [], {'max_length': '250', 'null': 'True'}),
            'otherin': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'otherout': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'performedaccounting': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'_auditlog_accounting'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'performedclose': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'_auditlog_closeasproject'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'performeddocument': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'_auditlog_documents'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'performedoperations': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'_auditlog_operations'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'performedre': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'_auditlog_reopen'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'performedstorage': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'_auditlog_storage'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'retention': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'PE'", 'max_length': '2'}),
            'storageclose': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tinvoice': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'tiva': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'ventas.detailspurchaseorder': {
            'Meta': {'ordering': "[u'nropurchase']", 'object_name': 'DetailsPurchaseOrder'},
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
            'Meta': {'ordering': "[u'proyecto']", 'object_name': 'HistoryMetProject'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "u'BR000'", 'to': u"orm['home.Brand']"}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'default': "u''", 'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "u'MO000'", 'to': u"orm['home.Model']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'default': "u''", 'to': u"orm['ventas.Proyecto']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'quantityorders': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'sales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'494J0T'", 'max_length': '6'})
        },
        u'ventas.metradoventa': {
            'Meta': {'ordering': "[u'proyecto']", 'object_name': 'Metradoventa'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "u'BR000'", 'to': u"orm['home.Brand']"}),
            'cantidad': ('django.db.models.fields.FloatField', [], {}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materiales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "u'MO000'", 'to': u"orm['home.Model']"}),
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
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "u'BR000'", 'to': u"orm['home.Brand']"}),
            'cantidad': ('django.db.models.fields.FloatField', [], {}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'materiales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "u'MO000'", 'to': u"orm['home.Model']"}),
            'precio': ('django.db.models.fields.FloatField', [], {}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'sales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'})
        },
        u'ventas.painting': {
            'Meta': {'ordering': "[u'-project']", 'object_name': 'Painting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nfilmb': ('django.db.models.fields.SmallIntegerField', [], {'default': '4'}),
            'nfilmc': ('django.db.models.fields.SmallIntegerField', [], {'default': '4'}),
            'nlayers': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'ventas.paintingauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'PaintingAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_painting_audit_log_entry'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'nfilmb': ('django.db.models.fields.SmallIntegerField', [], {'default': '4'}),
            'nfilmc': ('django.db.models.fields.SmallIntegerField', [], {'default': '4'}),
            'nlayers': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'ventas.proyecto': {
            'Meta': {'ordering': "[u'nompro']", 'object_name': 'Proyecto'},
            'approved': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'approvedAsEmployee'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'aservices': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'comienzo': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Moneda']", 'null': 'True', 'blank': 'True'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Departamento']"}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'distrito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Distrito']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'empdni': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'proyectoAsEmployee'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'exchange': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nompro': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'obser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Pais']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Provincia']"}),
            'proyecto_id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ruccliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Cliente']", 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'00'", 'max_length': '2'}),
            'typep': ('django.db.models.fields.CharField', [], {'default': "u'ACI'", 'max_length': '3'})
        },
        u'ventas.proyectoauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'ProyectoAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_proyecto_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'approved': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'_auditlog_approvedAsEmployee'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'aservices': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'comienzo': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Moneda']", 'null': 'True', 'blank': 'True'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Departamento']"}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'distrito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Distrito']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'empdni': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'_auditlog_proyectoAsEmployee'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'exchange': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nompro': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'obser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Pais']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Provincia']"}),
            'proyecto_id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'db_index': 'True'}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ruccliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Cliente']", 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'00'", 'max_length': '2'}),
            'typep': ('django.db.models.fields.CharField', [], {'default': "u'ACI'", 'max_length': '3'})
        },
        u'ventas.purchaseorder': {
            'Meta': {'ordering': "[u'project']", 'object_name': 'PurchaseOrder'},
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
            'Meta': {'ordering': "[u'proyecto']", 'object_name': 'RestoreStorage'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "u'BR000'", 'to': u"orm['home.Brand']"}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'default': "u''", 'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "u'MO000'", 'to': u"orm['home.Model']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'default': "u''", 'to': u"orm['ventas.Proyecto']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'sales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'PZ0DT7'", 'max_length': '6'})
        },
        u'ventas.sectore': {
            'Meta': {'ordering': "[u'sector_id']", 'object_name': 'Sectore'},
            'amount': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'amountsales': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'atype': ('django.db.models.fields.CharField', [], {'default': "u'NN'", 'max_length': '2', 'blank': 'True'}),
            'comienzo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'nomsec': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'obser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'planoid': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '16', 'null': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sector_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'AC'", 'max_length': '2'}),
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
            'atype': ('django.db.models.fields.CharField', [], {'default': "u'NN'", 'max_length': '2', 'blank': 'True'}),
            'comienzo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'nomsec': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'obser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'planoid': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '16', 'null': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sector_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'AC'", 'max_length': '2'}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'})
        },
        u'ventas.sectorfiles': {
            'Meta': {'object_name': 'SectorFiles'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'dsector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operations.DSector']", 'null': 'True', 'blank': 'True'}),
            'files': ('django.db.models.fields.files.FileField', [], {'max_length': '200'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'ventas.subproyecto': {
            'Meta': {'ordering': "[u'nomsub']", 'object_name': 'Subproyecto'},
            'additional': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comienzo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nomsub': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'obser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'AC'", 'max_length': '2'}),
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
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'AC'", 'max_length': '2'}),
            'subproyecto_id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'db_index': 'True'})
        },
        u'ventas.updatemetproject': {
            'Meta': {'ordering': "[u'proyecto']", 'object_name': 'UpdateMetProject'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "u'BR000'", 'to': u"orm['home.Brand']"}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'default': "u''", 'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "u'MO000'", 'to': u"orm['home.Model']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'default': "u''", 'to': u"orm['ventas.Proyecto']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'quantityorders': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'sales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'})
        },
        u'ventas.updatemetprojectauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'UpdateMetProjectAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_updatemetproject_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "u'BR000'", 'to': u"orm['home.Brand']"}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'default': "u''", 'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "u'MO000'", 'to': u"orm['home.Model']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'default': "u''", 'to': u"orm['ventas.Proyecto']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'quantityorders': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'sales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "u'0'", 'max_length': '1'})
        }
    }

    complete_apps = ['ventas']