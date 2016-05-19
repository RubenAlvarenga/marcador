"""marcador URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
from django.conf import settings
from apps.asistencia import views
from apps.asistencia.views import AsistenciaSingleTableView, UserSingleTableView, UserUpdateView, AsistenciasSingleTableView
from apps.decorators import custom_permission_required

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page': '/'}),
    
    #NO MOVER DE LUGAR!!!!!!!!!!!!
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name':'index.html'}, name='login'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),

    url(r'^home$', views.home, name='home'),


	url(r'^mismarcas/$', custom_permission_required('asistencia.add_asistencia')(AsistenciaSingleTableView.as_view()), name='mismarcas'),

    url(r'^marcas/$', custom_permission_required('asistencia.list_asistencia')(AsistenciasSingleTableView.as_view()), name='marcas'),

    url(r'^administrar/$', custom_permission_required('auth.add_user')(UserSingleTableView.as_view()), name='administrar'),


    url(r'^administrar/addUsuario$', custom_permission_required('auth.add_user')(views.addUsuario), name='add_user'),
    url(r'^administrar/updUsuario/(?P<pk>[\d]+)$', custom_permission_required('auth.change_user')(UserUpdateView.as_view()), name='upd_user'),


]
