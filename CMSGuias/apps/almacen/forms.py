# -*- coding: utf-8 -*-

from django import forms
from CMSGuias.apps.almacen import models
from CMSGuias.apps.home.models import (
  Cliente, Almacene, Transportista, Transporte, Conductore)
from CMSGuias.apps.ventas.models import Proyecto, Sectore, Subproyecto


# Customers
class addCustomersForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = {'flag'}
        widgets = {
            'ruccliente_id': forms.TextInput(attrs={'class': 'form-control'}),
            'razonsocial': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.Select(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-control'}),
            'distrito': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'maxlength': '200',
                'rows': '4'}),
            'telefono': forms.TextInput(attrs={
                'type': 'tel',
                'placeholder': '000-000-000',
                'class': 'form-control'})}


# Projects
class addProjectForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        exclude = {'flag', 'proyecto_id'}
        STATUS_PROJECT = (
          ('PE', 'PEDIENTE'),
          ('AC', 'ACTIVO'),
          ('CO', 'COMPLETO'))
        widgets = {
            'ruccliente': forms.Select(attrs={'class': 'form-control'}),
            'nompro': forms.TextInput(attrs={'class': 'form-control'}),
            'comienzo': forms.TextInput(attrs={
                'class': 'form-control in-date',
                'maxlength': '10',
                'placeholder': 'aaaa-mm-dd'}),
            'fin': forms.TextInput(attrs={
                'class': 'form-control in-date',
                'maxlength': '10',
                'placeholder': 'aaaa-mm-dd'}),
            'pais': forms.Select(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-control'}),
            'distrito': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'obser': forms.Textarea(attrs={
                'class': 'form-control',
                'maxlength': '200',
                'rows': '4'}),
            'status': forms.Select(attrs={
                'class': 'form-control'}, choices=STATUS_PROJECT)}


# sectores
class addSectoresForm(forms.ModelForm):
    class Meta:
        model = Sectore
        exclude = {'registrado', 'flag', 'proyecto', 'subproyecto'}
        STATUS = (('PE', 'PENDIENTE'))
        widgets = {
            'sector_id': forms.TextInput(attrs={'class': 'form-control'}),
            # 'proyecto': forms.Select(attrs     ={'class': 'form-control'}),
            # 'subproyecto': forms.Select(attrs  ={'class': 'form-control'}),
            'planoid': forms.TextInput(attrs={'class': 'form-control'}),
            'nomsec': forms.TextInput(attrs={'class': 'form-control'}),
            'comienzo': forms.TextInput(attrs={
                'class': 'form-control in-date',
                'maxlength': '10',
                'placeholder': 'aaaa-mm-dd'}),
            'fin': forms.TextInput(attrs={
                'class': 'form-control in-date',
                'maxlength': '10',
                'placeholder': 'aaaa-mm-dd'}),
            'obser': forms.Textarea(attrs={
                'class': 'form-control',
                'maxlength': '200',
                'rows': '3'}),
            'status': forms.Select(attrs={
                'class': 'form-control'}, choices=STATUS)}


# SubProyectos'
class addSubprojectForm(forms.ModelForm):
    class Meta:
        model = Subproyecto
        exclude = {'proyecto', 'registrado', 'flag'}
        STATUS = (('PE', 'PENDIENTE'))
        widgets = {
            'subproyecto_id': forms.TextInput(attrs={'class': 'form-control'}),
            'nomsub': forms.TextInput(attrs={'class': 'form-control'}),
            'comienzo': forms.TextInput(attrs={
                'class': 'form-control in-date',
                'maxlength': '10',
                'placeholder': 'aaaa-mm-dd'}),
            'fin': forms.TextInput(attrs={
                'class': 'form-control in-date',
                'maxlength': '10',
                'placeholder': 'aaaa-mm-dd'}),
            'obser': forms.Textarea(attrs={
                'class': 'form-control',
                'maxlength': '200',
                'rows': '3'}),
            'status': forms.Select(attrs={
                'class': 'form-control'}, choices=STATUS)}


# Almacenes
class addAlmacenesForm(forms.ModelForm):
    class Meta:
        model = Almacene
        exclude = {'almacen_id', 'flag'}
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '50'})}


# Carrier
class addCarrierForm(forms.ModelForm):
    class Meta:
        model = Transportista
        exclude = {'flag'}
        widgets = {
            'traruc_id': forms.TextInput(attrs={
                'class': 'form-control', 'maxlength': '11'}),
            'tranom': forms.TextInput(attrs={'class': 'form-control'}),
            'tratel': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '000-000-000'})}


# Transport
class addTransportForm(forms.ModelForm):
    class Meta:
        model = Transporte
        exclude = {'traruc', 'flag'}
        widgets = {
            'nropla_id': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'})}


# Conductores
class addConductorForm(forms.ModelForm):
    class Meta:
        model = Conductore
        exclude = {'traruc', 'flag'}
        widgets = {
            'condni_id': forms.TextInput(attrs={'class': 'form-control'}),
            'connom': forms.TextInput(attrs={'class': 'form-control'}),
            'conlic': forms.TextInput(attrs={'class': 'form-control'}),
            'contel': forms.TextInput(attrs={'class': 'form-control'})}


# Orders
class addOrdersForm(forms.ModelForm):
    class Meta:
        model = models.Pedido
        exclude = {
          'pedido_id',
          'registrado',
          'status',
          'flag'}


# Guide referral
class addGuideReferral(forms.ModelForm):
    class Meta:
        model = models.GuiaRemision
        exclude = {
            'guia_id',
            'registrado',
            'status',
            'flag',
            'comment',
            'observation',
            'nota'}


class addTempGuide(forms.ModelForm):
    class Meta:
        model = models.TmpDetGuia
        exclude = {'flag'}


# Note Ingress
class addNoteIngress(forms.ModelForm):
    class Meta:
        model = models.NoteIngress
        exclude = {
            'ingress_id',
            'status',
            'flag'}
