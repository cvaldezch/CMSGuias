# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cotizacion'
        db.create_table(u'logistica_cotizacion', (
            ('cotizacion_id', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True)),
            ('suministro', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['almacen.Suministro'], null=True, blank=True)),
            ('empdni', self.gf('django.db.models.fields.related.ForeignKey')(default='70492850', to=orm['home.Employee'])),
            ('almacen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Almacene'])),
            ('registrado', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('traslado', self.gf('django.db.models.fields.DateField')()),
            ('obser', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='PE', max_length=2)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'logistica', ['Cotizacion'])

        # Adding model 'Compra'
        db.create_table(u'logistica_compra', (
            ('compra_id', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True)),
            ('proveedor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Proveedor'])),
            ('empdni', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['home.Employee'])),
            ('cotizacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistica.Cotizacion'], null=True, blank=True)),
            ('projects', self.gf('django.db.models.fields.CharField')(default='', max_length=250, null=True, blank=True)),
            ('lugent', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('documento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Documentos'], null=True, blank=True)),
            ('pagos', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.FormaPago'], null=True, blank=True)),
            ('moneda', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Moneda'], null=True, blank=True)),
            ('registrado', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('traslado', self.gf('django.db.models.fields.DateField')()),
            ('contacto', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='PE', max_length=2)),
            ('deposito', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('discount', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'logistica', ['Compra'])

        # Adding model 'DetCompra'
        db.create_table(u'logistica_detcompra', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('compra', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistica.Compra'])),
            ('materiales', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Materiale'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(default='BR000', to=orm['home.Brand'], blank=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(default='MO000', to=orm['home.Model'], blank=True)),
            ('cantidad', self.gf('django.db.models.fields.FloatField')()),
            ('precio', self.gf('django.db.models.fields.FloatField')()),
            ('discount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('cantstatic', self.gf('django.db.models.fields.FloatField')()),
            ('flag', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
        ))
        db.send_create_signal(u'logistica', ['DetCompra'])

        # Adding model 'tmpcompra'
        db.create_table(u'logistica_tmpcompra', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('empdni', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('materiales', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Materiale'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(default='BR000', to=orm['home.Brand'], blank=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(default='MO000', to=orm['home.Model'], blank=True)),
            ('cantidad', self.gf('django.db.models.fields.FloatField')()),
            ('discount', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('precio', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal(u'logistica', ['tmpcompra'])

        # Adding model 'CotCliente'
        db.create_table(u'logistica_cotcliente', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cotizacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistica.Cotizacion'])),
            ('proveedor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Proveedor'], null=True, blank=True)),
            ('registrado', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('envio', self.gf('django.db.models.fields.DateField')()),
            ('contacto', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('validez', self.gf('django.db.models.fields.DateField')()),
            ('moneda', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Moneda'])),
            ('obser', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='PE', max_length=2)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'logistica', ['CotCliente'])

        # Adding model 'DetCotizacion'
        db.create_table(u'logistica_detcotizacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cotizacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistica.Cotizacion'])),
            ('proveedor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Proveedor'])),
            ('materiales', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Materiale'])),
            ('cantidad', self.gf('django.db.models.fields.FloatField')()),
            ('precio', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('discount', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, blank=True)),
            ('entrega', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('marca', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('modelo', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'logistica', ['DetCotizacion'])

        # Adding model 'CotKeys'
        db.create_table(u'logistica_cotkeys', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cotizacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistica.Cotizacion'])),
            ('proveedor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Proveedor'])),
            ('keygen', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('status', self.gf('django.db.models.fields.CharField')(default='PE', max_length=2)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'logistica', ['CotKeys'])

        # Adding model 'tmpcotizacion'
        db.create_table(u'logistica_tmpcotizacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('empdni', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('materiales', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Materiale'])),
            ('cantidad', self.gf('django.db.models.fields.FloatField')()),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(default='BR000', to=orm['home.Brand'], blank=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(default='MO000', to=orm['home.Model'], blank=True)),
        ))
        db.send_create_signal(u'logistica', ['tmpcotizacion'])

        # Adding model 'DevProveedor'
        db.create_table(u'logistica_devproveedor', (
            ('devolucionp_id', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True)),
            ('notaingreso', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('almacen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Almacene'])),
            ('compra', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistica.Compra'])),
            ('notacredido', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('montonc', self.gf('django.db.models.fields.FloatField')()),
            ('obser', self.gf('django.db.models.fields.TextField')()),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'logistica', ['DevProveedor'])

        # Adding model 'DetDevProveedor'
        db.create_table(u'logistica_detdevproveedor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('devolucionp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistica.DevProveedor'])),
            ('materiales', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Materiale'])),
            ('cantidad', self.gf('django.db.models.fields.FloatField')()),
            ('cantstatic', self.gf('django.db.models.fields.FloatField')()),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'logistica', ['DetDevProveedor'])

        # Adding model 'ServiceOrder'
        db.create_table(u'logistica_serviceorder', (
            ('serviceorder_id', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Proyecto'])),
            ('subprojecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ventas.Subproyecto'], null=True, blank=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Proveedor'])),
            ('register', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('quotation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistica.Cotizacion'], null=True, blank=True)),
            ('arrival', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Documentos'])),
            ('method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.FormaPago'])),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('term', self.gf('django.db.models.fields.DateField')()),
            ('dsct', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Moneda'])),
            ('deposit', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('elaborated', self.gf('django.db.models.fields.related.ForeignKey')(related_name='elaboratedAsEmployee', to=orm['home.Employee'])),
            ('authorized', self.gf('django.db.models.fields.related.ForeignKey')(related_name='authorizedAsEmployee', to=orm['home.Employee'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='PE', max_length=2)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'logistica', ['ServiceOrder'])

        # Adding model 'DetailsServiceOrder'
        db.create_table(u'logistica_detailsserviceorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('serviceorder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logistica.ServiceOrder'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Unidade'])),
            ('quantity', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal(u'logistica', ['DetailsServiceOrder'])


    def backwards(self, orm):
        # Deleting model 'Cotizacion'
        db.delete_table(u'logistica_cotizacion')

        # Deleting model 'Compra'
        db.delete_table(u'logistica_compra')

        # Deleting model 'DetCompra'
        db.delete_table(u'logistica_detcompra')

        # Deleting model 'tmpcompra'
        db.delete_table(u'logistica_tmpcompra')

        # Deleting model 'CotCliente'
        db.delete_table(u'logistica_cotcliente')

        # Deleting model 'DetCotizacion'
        db.delete_table(u'logistica_detcotizacion')

        # Deleting model 'CotKeys'
        db.delete_table(u'logistica_cotkeys')

        # Deleting model 'tmpcotizacion'
        db.delete_table(u'logistica_tmpcotizacion')

        # Deleting model 'DevProveedor'
        db.delete_table(u'logistica_devproveedor')

        # Deleting model 'DetDevProveedor'
        db.delete_table(u'logistica_detdevproveedor')

        # Deleting model 'ServiceOrder'
        db.delete_table(u'logistica_serviceorder')

        # Deleting model 'DetailsServiceOrder'
        db.delete_table(u'logistica_detailsserviceorder')


    models = {
        u'almacen.suministro': {
            'Meta': {'ordering': "['suministro_id']", 'object_name': 'Suministro'},
            'almacen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Almacene']"}),
            'asunto': ('django.db.models.fields.CharField', [], {'max_length': '180', 'null': 'True', 'blank': 'True'}),
            'empdni': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ingreso': ('django.db.models.fields.DateField', [], {}),
            'obser': ('django.db.models.fields.TextField', [], {}),
            'orders': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PE'", 'max_length': '2'}),
            'suministro_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'})
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
        u'home.unidade': {
            'Meta': {'object_name': 'Unidade'},
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'unidad_id': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'}),
            'uninom': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'logistica.compra': {
            'Meta': {'ordering': "['compra_id']", 'object_name': 'Compra'},
            'compra_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'contacto': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'cotizacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logistica.Cotizacion']", 'null': 'True', 'blank': 'True'}),
            'deposito': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'documento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Documentos']", 'null': 'True', 'blank': 'True'}),
            'empdni': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': u"orm['home.Employee']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lugent': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'moneda': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Moneda']", 'null': 'True', 'blank': 'True'}),
            'pagos': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.FormaPago']", 'null': 'True', 'blank': 'True'}),
            'projects': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'proveedor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Proveedor']"}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PE'", 'max_length': '2'}),
            'traslado': ('django.db.models.fields.DateField', [], {})
        },
        u'logistica.cotcliente': {
            'Meta': {'ordering': "['registrado']", 'object_name': 'CotCliente'},
            'contacto': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'cotizacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logistica.Cotizacion']"}),
            'envio': ('django.db.models.fields.DateField', [], {}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moneda': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Moneda']"}),
            'obser': ('django.db.models.fields.TextField', [], {}),
            'proveedor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Proveedor']", 'null': 'True', 'blank': 'True'}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PE'", 'max_length': '2'}),
            'validez': ('django.db.models.fields.DateField', [], {})
        },
        u'logistica.cotizacion': {
            'Meta': {'ordering': "['cotizacion_id']", 'object_name': 'Cotizacion'},
            'almacen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Almacene']"}),
            'cotizacion_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'empdni': ('django.db.models.fields.related.ForeignKey', [], {'default': "'70492850'", 'to': u"orm['home.Employee']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'obser': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'registrado': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PE'", 'max_length': '2'}),
            'suministro': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['almacen.Suministro']", 'null': 'True', 'blank': 'True'}),
            'traslado': ('django.db.models.fields.DateField', [], {})
        },
        u'logistica.cotkeys': {
            'Meta': {'object_name': 'CotKeys'},
            'cotizacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logistica.Cotizacion']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keygen': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'proveedor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Proveedor']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PE'", 'max_length': '2'})
        },
        u'logistica.detailsserviceorder': {
            'Meta': {'object_name': 'DetailsServiceOrder'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'serviceorder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logistica.ServiceOrder']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Unidade']"})
        },
        u'logistica.detcompra': {
            'Meta': {'ordering': "['materiales']", 'object_name': 'DetCompra'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'BR000'", 'to': u"orm['home.Brand']", 'blank': 'True'}),
            'cantidad': ('django.db.models.fields.FloatField', [], {}),
            'cantstatic': ('django.db.models.fields.FloatField', [], {}),
            'compra': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logistica.Compra']"}),
            'discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'flag': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materiales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "'MO000'", 'to': u"orm['home.Model']", 'blank': 'True'}),
            'precio': ('django.db.models.fields.FloatField', [], {})
        },
        u'logistica.detcotizacion': {
            'Meta': {'ordering': "['materiales']", 'object_name': 'DetCotizacion'},
            'cantidad': ('django.db.models.fields.FloatField', [], {}),
            'cotizacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logistica.Cotizacion']"}),
            'discount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'entrega': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marca': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'materiales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'modelo': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'precio': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'proveedor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Proveedor']"})
        },
        u'logistica.detdevproveedor': {
            'Meta': {'ordering': "['materiales']", 'object_name': 'DetDevProveedor'},
            'cantidad': ('django.db.models.fields.FloatField', [], {}),
            'cantstatic': ('django.db.models.fields.FloatField', [], {}),
            'devolucionp': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logistica.DevProveedor']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materiales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"})
        },
        u'logistica.devproveedor': {
            'Meta': {'ordering': "['devolucionp_id']", 'object_name': 'DevProveedor'},
            'almacen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Almacene']"}),
            'compra': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logistica.Compra']"}),
            'devolucionp_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'montonc': ('django.db.models.fields.FloatField', [], {}),
            'notacredido': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'notaingreso': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'obser': ('django.db.models.fields.TextField', [], {})
        },
        u'logistica.serviceorder': {
            'Meta': {'object_name': 'ServiceOrder'},
            'arrival': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'authorized': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'authorizedAsEmployee'", 'to': u"orm['home.Employee']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Moneda']"}),
            'deposit': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Documentos']"}),
            'dsct': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'elaborated': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'elaboratedAsEmployee'", 'to': u"orm['home.Employee']"}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'method': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.FormaPago']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Proyecto']"}),
            'quotation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logistica.Cotizacion']", 'null': 'True', 'blank': 'True'}),
            'register': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'serviceorder_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PE'", 'max_length': '2'}),
            'subprojecto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ventas.Subproyecto']", 'null': 'True', 'blank': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Proveedor']"}),
            'term': ('django.db.models.fields.DateField', [], {})
        },
        u'logistica.tmpcompra': {
            'Meta': {'ordering': "['materiales']", 'object_name': 'tmpcompra'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'BR000'", 'to': u"orm['home.Brand']", 'blank': 'True'}),
            'cantidad': ('django.db.models.fields.FloatField', [], {}),
            'discount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'empdni': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materiales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "'MO000'", 'to': u"orm['home.Model']", 'blank': 'True'}),
            'precio': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'logistica.tmpcotizacion': {
            'Meta': {'ordering': "['materiales']", 'object_name': 'tmpcotizacion'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'default': "'BR000'", 'to': u"orm['home.Brand']", 'blank': 'True'}),
            'cantidad': ('django.db.models.fields.FloatField', [], {}),
            'empdni': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materiales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Materiale']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'default': "'MO000'", 'to': u"orm['home.Model']", 'blank': 'True'})
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
        }
    }

    complete_apps = ['logistica']