from django.urls import path
from .views import (
    home,
    SchemeListView,
    SchemeDetailView,
    
    # tagged
    CategoryView,
    TaggedView,
    userForm,
)
# from . import views
urlpatterns = [
    path('', home, name='home'),
    path('schemes/', SchemeListView.as_view(), name='schemes'),
    path('schemes/<slug:slug>/',SchemeDetailView.as_view(), name='schemedetail'),
    
    path('category/<slug:slug>',CategoryView.as_view(),name='category'),
    path('tagged/<slug:slug>',TaggedView.as_view(),name='tagged'),
    path('user/',userForm,name="userForm")
]