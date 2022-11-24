from django.urls import path
from .views import (
    home,
    SchemeListView,
    SchemeDetailView,
    SchemeUpdate,
    about,
    # tagged
    CategoryView,
    TaggedView,
    userForm,
    contact,
    ministry,
)
# from . import views
urlpatterns = [
    path('', home, name='home'),
    path('schemes/', SchemeListView.as_view(), name='schemes'),
    path('about/',about, name='about'),
    path('contact/', contact, name='contact'),
    path('schemes/<slug:slug>/',SchemeDetailView.as_view(), name='schemedetail'),
    path('category/<slug:slug>',CategoryView.as_view(),name='category'),
    path('ministry/',ministry,name='ministry'),
    path('tagged/<slug:slug>',TaggedView.as_view(),name='tagged'),
    path('user/',userForm,name="userForm"),
    path('updatescheme/<slug:slug>',SchemeUpdate.as_view(),name="updatescheme"),
    # path('news/<slug:slug>/',News.as_view(),name='news')

]