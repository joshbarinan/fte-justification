from django.urls import path
from . import views

urlpatterns = [
    path('', views.fte_justification, name="fte_justification"),
    path('add-fte-justification/', views.add_fte_justification, name='add_fte_justification'),
]
