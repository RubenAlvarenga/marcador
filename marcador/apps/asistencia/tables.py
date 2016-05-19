#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django_tables2 as tables
from .models import Asistencia
from django.utils.safestring import mark_safe
from django.conf import settings
from django_tables2  import  A
from django.utils.html import escape
from django.contrib.auth.models import User
ITEM_POR_PAGINA = 50


class EnlaceColumn(tables.Column):
    def render(self, value): return mark_safe('<a href="'+str(self.attrs["url"])+str(value)+'"><span class="glyphicon '+str(self.attrs["icono"])+'"></span></a>')
class buttonColumn(tables.Column):
    def render(self, value): return mark_safe('<a href="'+str(self.attrs["url"])+str(value)+'"><button type="button" class="btn btn-info btn-xs"><span class="glyphicon '+str(self.attrs["icono"])+'"></span> '+str(self.attrs["texto"])+'</button></a>')



class AsistenciaTable(tables.Table):
    get_horas_trabajadas = tables.Column(verbose_name='Horas', orderable=False )
    get_full_name = tables.Column(verbose_name='Nombres', order_by =("user.first_name"), accessor='user.get_full_name')
    class Meta:
        model = Asistencia
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("id",  'get_full_name', '...'   )



class UserTable(tables.Table):
    get_full_name = tables.Column(verbose_name='nombres', order_by =("first_name"))
    email=tables.Column(verbose_name='e-mail')
    last_login=tables.DateTimeColumn(verbose_name="ultimo ingreso")
    editar = buttonColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./updUsuario/", "icono":"glyphicon-pencil", "texto":"Editar" }, )
    groups  = tables.Column(verbose_name='Grupo', accessor="id")
    class Meta:
        model = User
        per_page=ITEM_POR_PAGINA
        exclude = ('password', 'last_name', 'first_name', 'date_joined', 'is_superuser', 'last_login', 'is_staff')
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("id",  'get_full_name', 'email', 'groups'   )


    def render_groups(self, record):
        return [ str(i.name) for i in record.groups.get_queryset() ]        