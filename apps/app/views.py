# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import RBT, Altafonte, FinalProduct, Document, Kisom, RingtoneCode
from django.db.models import Sum

# @login_required(login_url="/artist/login/")
# def index(request):
#     context = {'segment': 'index'}

#     html_template = loader.get_template('index.html')
#     return HttpResponse(html_template.render(context, request))

class ClubChartView(LoginRequiredMixin, TemplateView):
    template_name='index.html'
    login_url = 'login'
    # print(request)
    # @method_decorator(login_required)
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # if(user.is_authenticated):
                
        # print(user)
        # try:
        context['record_new_6'] = FinalProduct.objects.filter(artist = user.first_name)[::-1][:6][::-1]
        
        context['record_all'] = FinalProduct.objects.filter(artist = user.first_name)
        
        context['total_rbt'] = FinalProduct.objects.filter(artist = user.first_name).aggregate(Sum('rbt_val'))
        
        context['total_kisom'] = FinalProduct.objects.filter(artist = user.first_name).aggregate(Sum('kisom_val'))
        
        context['total_altafonte_aoa'] = FinalProduct.objects.filter(artist = user.first_name).aggregate(Sum('altafonte_aoa'))
        
        context['total_artista'] = FinalProduct.objects.filter(artist = user.first_name).aggregate(Sum('total_artista'))
        
        context['document'] = Document.objects.filter(artist_name = self.request.session['id'], admin_approval_status = True)
        
        context['user_altafonte'] = Altafonte.objects.filter(artist_display = user.first_name, admin_approval_status = True).count()
        
        context['user_kisom'] = Kisom.objects.filter(artist_name = user.first_name, admin_approval_status = True).count()
        
        context['user_rbt'] = RBT.objects.filter(artist_name = user.first_name, admin_approval_status = True).count()
        
        context['total_songs'] = context['user_altafonte'] + context['user_kisom'] + context['user_rbt']
        
        context['demo'] = Altafonte.objects.filter(artist_display = user.first_name).values('service_id') .annotate(dcount=Sum('altafonte_aoa')).order_by('dcount')
        
        context['ringtone_codes'] = RingtoneCode.objects.filter(artist_name = self.request.session['id'], admin_approval_status = True)
        
        # print(context['demo'])
        # print('Count 1111', Altafonte.objects.filter(artist_display = user.first_name).values('service_id') .annotate(dcount=Sum('altafonte_aoa')).order_by().count())
        # for i in context['demo']:
        #     print(i['service_id'])
        #     print(i['dcount'])
        
        # print('my list      111111111111')
        context['top_10_service'] = context['demo'][::-1][:10]
        # for i in list_1:
        #     print(i['service_id'])
        #     print(i['dcount'])
            
        # print('count 2222   ')
            # print(i['artist_display'])
        # # print(user_altafonte)
        
        # print(context['document'])
        return context
#login url route
@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        #load and split template
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
