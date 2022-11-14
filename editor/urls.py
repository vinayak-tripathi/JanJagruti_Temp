from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import (
    SchemeAdd,
    home,
    SchemeUpdate,
    SchemeUpdateListView)
urlpatterns = [
    path('editor/',home,name="editor"),
    path('editor/login/', auth_views.LoginView.as_view(template_name='editor/login.html'), name='login'),
    path('editor/logout/', auth_views.LogoutView.as_view(template_name='editor/logout.html'), name='logout'),
    path('editor/logout/', auth_views.LogoutView.as_view(template_name='editor/logout.html'), name='logout'),
    path('editor/updatescheme/',SchemeUpdateListView.as_view(),name="updatescheme"),
    path('editor/addscheme/',SchemeAdd.as_view(),name = 'addscheme'),
    path('editor/updatescheme/<slug:slug>',SchemeUpdate.as_view(),name="updatescheme"),
    ]