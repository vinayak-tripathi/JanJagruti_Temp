from django.urls import path
from .views import (
    home,
    SchemeListView,
    SchemeDetailView,
    SchemeAdd,
    # tagged
    CategoryView,
    TaggedView,
    SchemeUpdate,
    AboutView
    
)
from whatsapp import views    # ← new import

# from . import views
urlpatterns = [
    path('', home, name='home'),
    path('schemes/', SchemeListView.as_view(), name='schemes'),
    path('message', views.message),    # ← new item
    path('about',AboutView.as_view(),name = 'about'), # for about page
    path('schemes/<slug:slug>/',SchemeDetailView.as_view(), name='schemedetail'),
    path('addscheme/',SchemeAdd.as_view(),name = 'addscheme'),
    path('category/<slug:slug>',CategoryView.as_view(),name='category'),
    path('tagged/<slug:slug>',TaggedView.as_view(),name='tagged'),
    path('updatescheme/<slug:slug>',SchemeUpdate.as_view(),name="updatescheme")
]