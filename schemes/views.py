from django.shortcuts import render, get_object_or_404
from django.db.models import Q
# Create your views here.
from django.views.generic import (
    ListView,
    DetailView,
)

from .models import Schemes,Tags, Category
from django.urls import reverse_lazy
from django.forms.widgets import SelectDateWidget
from django import forms
# from taggit.models import Tags,Category,SubCategory

def home(request):
    context = {
        'categories': Category.objects.all()
    }
    return render(request, 'schemes/home.html',context)

class SchemeListView(ListView):
    model = Schemes
    template_name = 'schemes/schemes_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'schemes'
    ordering = ['uploadDate']
    paginate_by = 8
    queryset = model.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        search_input = self.request.GET.get('search-area') or ''
        context['title'] = 'Search Schemes'
        context['search_input']= search_input
        # print(context)
        return context
    def get_queryset(self):
        # user = get_object_or_404(User, username=self.kwargs.get('username'))
        search_input = self.request.GET.get('search-area') or ''
        return Schemes.objects.filter(Q(details__icontains=search_input)|Q(eligibility__icontains=search_input)|Q(nodalMinistry__icontains=search_input)).order_by('-uploadDate')

class SchemeDetailView(DetailView):
    model = Schemes
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context['object'],'Hello')
        # context["title"] = context['schemes'].objects
        fields = {
            'title' : 'Title',
            'details' : 'Details',
             'eligibility': 'Eligibility',
             'sources' : 'References',
             'validity' : 'Validty'

        }
        # ['title','name','brief','eligibility','references','slug','tags','details']
        context['fields']=fields
        return context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(context)
    #     context["title"] = context['schemes'].objects
    #     print(context['schemes'])
    #     return context




# class CategoryListView(ListView,slug):
#     tag = get_object_or_404(Tags,slug=slug)
def tagged(request, slug):
    tag = get_object_or_404(Category, slug=slug)
    # Filter posts by tag name  
    posts = Schemes.objects.filter(category=tag)
    context = {
        'tag':tag,
        'schemes':posts,
    }
    return render(request, 'schemes/schemes_list.html', context)

class CategoryView(ListView):
    model = Schemes
    template_name = 'schemes/schemes_list.html'
    context_object_name = 'schemes'
    paginate_by = 8
    queryset = model.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        context['title'] = "Categroy-"+str(self.cat)
        return context
    def get_queryset(self):
        # print(self.kwargs)
        self.cat = get_object_or_404(Category, slug=self.kwargs['slug'])
        posts = Schemes.objects.filter(category=self.cat)
        return posts

class TaggedView(ListView):
    model = Schemes
    template_name = 'schemes/schemes_list.html'
    context_object_name = 'schemes'
    paginate_by = 8
    queryset = model.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        context['title'] = "Tag-"+str(self.tag)
        return context
    def get_queryset(self):
        # print(self.kwargs)
        self.tag = get_object_or_404(Tags, slug=self.kwargs['slug'])
        # print(tag)
        posts = Schemes.objects.filter(tags=self.tag)
        print(posts)
        return posts

def about(request):
    return render(request,"schemes/about.html")

def userForm(request):
    return render(request, 'schemes/secondForm.html')