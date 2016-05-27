# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SGroup.sgroup_id'
        db.alter_column(u'operations_sgroup', 'sgroup_id', self.gf('django.db.models.fields.CharField')(max_length=18, primary_key=True))

        # Changing field 'SGroupAuditLogEntry.sgroup_id'
        db.alter_column(u'operations_sgroupauditlogentry', 'sgroup_id', self.gf('django.db.models.fields.CharField')(max_length=18))

    def backwards(self, orm):

        # Changing field 'SGroup.sgroup_id'
        db.alter_column(u'operations_sgroup', 'sgroup_id', self.gf('django.db.models.fields.CharField')(max_length=13, primary_key=True))

        # Changing field 'SGroupAuditLogEntry.sgroup_id'
        db.alter_column(u'operations_sgroupauditlogentry', 'sgroup_id', self.gf('django.db.models.fields.CharField')(max_length=13))

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
        u'operations.deductive': {
            'Meta': {'ordering': "['deductive_id']", 'object_name': 'Deductive'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deductive_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'relations': ('django.db.models.fields.TextField', [], {}),
            'rtype': ('django.db.models.fields.CharField', [], {'default': "'NN'", 'max_length': '3'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']", 'null': 'True', 'blank': 'True'}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'})
        },
        u'operations.deductiveinputs': {
            'Meta': {'ordering': "['deductive', 'materials']", 'object_name': 'DeductiveInputs'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'BR000'", 'to': u"orm['home.Brand']"}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deductive': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operations.Deductive']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "'MO000'", 'to': u"orm['home.Model']"}),
            'price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'related': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'operations.deductiveoutputs': {
            'Meta': {'ordering': "['deductive', 'materials']", 'object_name': 'DeductiveOutputs'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'deductive': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operations.Deductive']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'operations.detailspreorders': {
            'Meta': {'object_name': 'DetailsPreOrders'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Brand']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Model']"}),
            'orders': ('django.db.models.fields.FloatField', [], {}),
            'preorder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operations.PreOrders']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {})
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
        u'operations.dsectorauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'DSectorAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_dsector_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'dateend': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'datestart': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dsector_id': ('django.db.models.fields.CharField', [], {'default': "'PRAA000VEN00SG0000DS000'", 'max_length': '23', 'db_index': 'True'}),
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
        u'operations.dsmetrado': {
            'Meta': {'object_name': 'DSMetrado'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Brand']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dsector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operations.DSector']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Model']"}),
            'nipple': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ppurchase': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'psales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'qguide': ('django.db.models.fields.FloatField', [], {}),
            'qorder': ('django.db.models.fields.FloatField', [], {}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']", 'null': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'operations.dsmetradoauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'DSMetradoAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_dsmetrado_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Brand']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dsector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operations.DSector']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Model']"}),
            'nipple': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ppurchase': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'psales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'qguide': ('django.db.models.fields.FloatField', [], {}),
            'qorder': ('django.db.models.fields.FloatField', [], {}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']", 'null': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'operations.historydsmetrado': {
            'Meta': {'object_name': 'HistoryDSMetrado'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Brand']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dsector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operations.DSector']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Model']"}),
            'nipple': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ppurchase': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'psales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'qcode': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'qguide': ('django.db.models.fields.FloatField', [], {}),
            'qorder': ('django.db.models.fields.FloatField', [], {}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'operations.letter': {
            'Meta': {'ordering': "['letter_id']", 'object_name': 'Letter'},
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fors': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'froms': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'letter': ('django.db.models.fields.files.FileField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'letter_id': ('django.db.models.fields.CharField', [], {'max_length': '19', 'primary_key': 'True'}),
            'observation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'performed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Employee']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PE'", 'max_length': '2'})
        },
        u'operations.letteranexo': {
            'Meta': {'ordering': "['letter']", 'object_name': 'LetterAnexo'},
            'anexo': ('django.db.models.fields.files.FileField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operations.Letter']"})
        },
        u'operations.letteranexoauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'LetterAnexoAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_letteranexo_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'anexo': ('django.db.models.fields.files.FileField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'letter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operations.Letter']"})
        },
        u'operations.letterauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'LetterAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_letter_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fors': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'froms': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'letter': ('django.db.models.fields.files.FileField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'letter_id': ('django.db.models.fields.CharField', [], {'max_length': '19', 'db_index': 'True'}),
            'observation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'performed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Employee']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PE'", 'max_length': '2'})
        },
        u'operations.metproject': {
            'Meta': {'ordering': "['proyecto']", 'object_name': 'MetProject'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'BR000'", 'to': u"orm['home.Brand']"}),
            'cantidad': ('django.db.models.fields.FloatField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materiales': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "'MO000'", 'to': u"orm['home.Model']"}),
            'precio': ('django.db.models.fields.FloatField', [], {}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['ventas.Proyecto']"}),
            'quantityorder': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'sales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'operations.mmetrado': {
            'Meta': {'object_name': 'MMetrado'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Brand']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dsector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operations.DSector']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Model']"}),
            'nipple': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ppurchase': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'psales': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'qguide': ('django.db.models.fields.FloatField', [], {}),
            'qorder': ('django.db.models.fields.FloatField', [], {}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']", 'null': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'operations.nipple': {
            'Meta': {'ordering': "['proyecto']", 'object_name': 'Nipple'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['operations.DSector']", 'null': 'True', 'blank': 'True'}),
            'cantidad': ('django.db.models.fields.FloatField', [], {'default': '1', 'null': 'True'}),
            'cantshop': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materiales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'metrado': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']", 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']", 'null': 'True', 'blank': 'True'}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'operations.preorders': {
            'Meta': {'ordering': "['preorder_id']", 'object_name': 'PreOrders'},
            'annular': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'issue': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nipples': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'observation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'performed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Employee']"}),
            'preorder_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PE'", 'max_length': '2'}),
            'subproject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'}),
            'transfer': ('django.db.models.fields.DateField', [], {})
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
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'sgroup_id': ('django.db.models.fields.CharField', [], {'default': "'PRAA000SG0000'", 'max_length': '18', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PE'", 'max_length': '2', 'blank': 'True'}),
            'subproject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'})
        },
        u'operations.sgroupauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'SGroupAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_sgroup_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'colour': ('django.db.models.fields.CharField', [], {'max_length': '21', 'null': 'True', 'blank': 'True'}),
            'dateend': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'datestart': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'observation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Sectore']"}),
            'sgroup_id': ('django.db.models.fields.CharField', [], {'default': "'PRAA000SG0000'", 'max_length': '18', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PE'", 'max_length': '2', 'blank': 'True'}),
            'subproject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'})
        },
        u'ventas.proyecto': {
            'Meta': {'ordering': "['nompro']", 'object_name': 'Proyecto'},
            'approved': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'approvedAsEmployee'", 'null': 'True', 'to': u"orm['home.Employee']"}),
            'aservices': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'comienzo': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Moneda']", 'null': 'True', 'blank': 'True'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Departamento']"}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'distrito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Distrito']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'empdni': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'proyectoAsEmployee'", 'null': 'True', 'to': u"orm['home.Employee']"}),
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
            'status': ('django.db.models.fields.CharField', [], {'default': "'00'", 'max_length': '2'}),
            'typep': ('django.db.models.fields.CharField', [], {'default': "'ACI'", 'max_length': '3'})
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
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sector_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'AC'", 'max_length': '2'}),
            'subproyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'})
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
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'AC'", 'max_length': '2'}),
            'subproyecto_id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'})
        }
    }

    complete_apps = ['operations']