from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_new, name='post_new'),
]
