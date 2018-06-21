"""MindNavigator_Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url

from MindNavigator_Server import views
from MindNavigator_Server.models import Intervention, InterventionManager

urlpatterns = [
    url('admin/', admin.site.urls),
    url('user_reg$', views.handle_register),
    url('user_lgn$', views.handle_login),
    url('event_crt$', views.handle_event_create),
    url('event_edt$', views.handle_event_edit),
    url('event_del$', views.handle_event_delete),
    url('event_del$', views.handle_event_delete),
    url('events_fetch$', views.handle_events_fetch),
    url('interv_crt$', views.handle_intervention_create),
    url('interv_syst$', views.handle_system_intervention_get),
    url('interv_peer$', views.handle_peer_intervention_get),
    url('eval_subm$', views.handle_evaluation_submit),
    url('eval_fetch$', views.handle_evaluation_fetch),
]

if Intervention.objects.all().count() == 0:
    Intervention.objects.create_intervention(name='Eat delicious food', intervention_type=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name='Ride a bicycle', intervention_type=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name='Go for a walk', intervention_type=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name='Meet with friends', intervention_type=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name='Play computer games', intervention_type=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name='Watch a movie', intervention_type=InterventionManager.SYSTEM)
