from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models






class Asistencia(models.Model):
    user = models.ForeignKey(User, verbose_name='Usuario', editable=False)
    entrada = models.DateTimeField( verbose_name='Entrada', editable=False)
    salida = models.DateTimeField( verbose_name='Salida', blank=True, null=True, editable=False)


    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ('-entrada', )
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
    def __unicode__(self):
        return u'%s' % (str(self.user))



    @property
    def get_horas_trabajadas(self):
        if self.entrada and self.salida:
            horas = self.salida - self.entrada
            return str(horas)[0:7]
        else: return None


