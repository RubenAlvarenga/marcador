from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect, urlresolvers, render, redirect
# Create your views here.
from django.contrib import messages
from django.template import RequestContext
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django_tables2 import SingleTableView, RequestConfig
from .models import Asistencia
from .tables import AsistenciaTable, UserTable
from .forms import UserForm,  updUserForm
from datetime import datetime
from django.contrib.auth.models import User
from django.template import Template, Context
from django.core.urlresolvers import reverse_lazy, reverse
def msg_render(msg):
    return Template(msg).render(Context())


def home(request):
    if request.user.is_authenticated():
        try:
            grupo = request.user.groups.values()[0]['name']
        except :
            return HttpResponseRedirect('/logout')
        else:
            if request.user.groups.values()[0]['name']=='empleado':
                return HttpResponseRedirect("/mismarcas")
            elif request.user.groups.values()[0]['name']=='empleador':
                return HttpResponseRedirect("/marcas")
            elif request.user.groups.values()[0]['name']=='administrador':
                return HttpResponseRedirect("/administrar")
    else:
        return HttpResponseRedirect("/")



class AsistenciaSingleTableView(SingleTableView):
    template_name='asistencia/marcar.html'
    model = Asistencia
    table_class = AsistenciaTable
    def get_queryset(self):
        table = super(AsistenciaSingleTableView, self).get_queryset().filter(user=self.request.user).order_by('-entrada')
        return table

    def get_context_data(self, **kwargs):
        context = super(AsistenciaSingleTableView, self).get_context_data(**kwargs)
        context['fecha']= datetime.now().date()
        return context

    def post(self, request, *args, **kwargs):
        accion=request.POST.get('accion')
        if accion=='ENT':
            entrada=Asistencia()
            entrada.user=request.user
            entrada.entrada =datetime.now()
            entrada.save()

        elif accion=='SAL':
            salida = Asistencia.objects.filter(user=request.user, salida=None).order_by('-entrada')
            if salida:
                salida=salida[0]
                salida.salida=datetime.now()
                salida.save()
            else:
                mensaje = "No ha marcado su Entrada"
                messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
                url = request.META['HTTP_REFERER']
                return HttpResponseRedirect(url)
        return HttpResponseRedirect('/logout')








class UserSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = User
    table_class = UserTable




    
    def get_queryset(self):
        table = super(UserSingleTableView, self).get_queryset()

        q=self.request.GET.get("q")
        if q: return table.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(username__icontains=q) )#.order_by(sort)
        else: return table


    # def post(self, request, *args, **kwargs):
    #     accion=request.POST.get('accion')
    #     if accion=='ENT':
    #         entrada=Asistencia()
    #         entrada.user=request.user
    #         entrada.entrada =datetime.now()
    #         entrada.save()

    #     elif accion=='SAL':
    #         salida = Asistencia.objects.filter(user=request.user, salida=None).order_by('-entrada')
    #         if salida:
    #             salida=salida[0]
    #             salida.salida=datetime.now()
    #             salida.save()
    #         else:
    #             mensaje = "No ha marcado su Entrada"
    #             messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
    #             url = request.META['HTTP_REFERER']
    #             return HttpResponseRedirect(url)
    #     return HttpResponseRedirect('/logout')






from django.contrib.auth.models import Group

def addUsuario(request):
    if request.method == 'POST':

        form = UserForm(request.POST or None, request.FILES)

        if form.is_valid():
            usuario=form.save()
            usuario.first_name=request.POST.get('nombre')
            usuario.last_name=request.POST.get('apellido')
            usuario.save()

            grupo = Group.objects.get(name=request.POST.get('grupo'))
            grupo.user_set.add(usuario)


            success_message = "El Usuario "+str(usuario.username)+" creado con exito"
            messages.add_message(request, messages.SUCCESS, success_message)
            url = urlresolvers.reverse('administrar')
            return HttpResponseRedirect(url)
        else:
           pass
    else:
        form = UserForm()

    template='asistencia/addUser.html'
    return render_to_response(template, {"form": form}, context_instance=RequestContext(request, locals()))



class UserUpdateView(SuccessMessageMixin, UpdateView):
    template_name='asistencia/updUser.html'
    model=User
    form_class = updUserForm
    success_message = msg_render("El Usuario %(username)s modificado con exito")
    
    def get_success_url(self):
        return reverse_lazy('administrar')
    
    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['user'] = self.request.user    
        return context

    # def get_form(self, form_class):
    #     form = super(UserUpdateView, self).get_form(form_class) #instantiate using parent
    #     try : impresora = Perfil.objects.get(user_id=self.object.id).impresora
    #     except : impresora = 'Ninguna'
    #     form.fields['impresora'].initial = impresora
    #     return form

    def form_valid(self, form):
        form.save()

        grupo = Group.objects.get(name=self.request.POST.get('grupo'))

        form.instance.groups.clear()
        
        grupo.user_set.add(form.instance)

        #grupo.user_set.add(form.instance)


        return super(UserUpdateView, self).form_valid(form)    




class AsistenciasSingleTableView(SingleTableView):
    template_name='asistencia/marcas.html'
    model = Asistencia
    table_class = AsistenciaTable
    def get_queryset(self):
        table = super(AsistenciasSingleTableView, self).get_queryset()

        q=self.request.GET.get("q")
        if q: return table.filter(Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q) | Q(user__username__icontains=q) )#.order_by(sort)
        else: return table


    def get_context_data(self, **kwargs):
        context = super(AsistenciasSingleTableView, self).get_context_data(**kwargs)
        context['notbutton'] = True
        return context