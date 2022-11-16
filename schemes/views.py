from django.shortcuts import render, get_object_or_404
from django.db.models import Q
# Create your views here.
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Schemes,Tags, Category
from django.urls import reverse_lazy
from django.forms.widgets import SelectDateWidget
from django import forms
# from taggit.models import Tags,Category,SubCategory

def home(request):
    # context = {
    #     'posts': Schemes.objects.all()
    # }
    category =[
   {
      "title": "Agriculture,Rural & Environment",
      "tagUrl": "agriculture",
      "url" : "https://www.myscheme.gov.in/_next/image?url=https%3A%2F%2Fcdn.myscheme.in%2Fimages%2Fcategories%2FAgriculture%2CRural%20%26%20Environment.png&w=48&q=75"
   },
   {
      "title": "Banking,Financial Services and Insurance",
      "tagUrl": "banking",
      "url" : "https://cdn.myscheme.in/images/categories/Public%20Safety,Law%20&%20Justice.png"
   },
   {
      "title":"Business & Entrepreneurship",
      "tagUrl": "business",
      "url": "https://cdn.myscheme.in/images/categories/Business%20&%20Entrepreneurship.png"
   },
     {
      "title":"Education & Learning",
      "tagUrl": "education",
      "url": "https://cdn.myscheme.in/images/categories/Education%20&%20Learning.png"
   },
     {
      "title":"Health & Wellness",
      "tagUrl": "health",
      "url": "https://cdn.myscheme.in/images/categories/Health%20&%20Wellness.png"
   },
     {
      "title":"Public Safety,Law & Justice",
      "tagUrl": "justice",
      "url": "https://cdn.myscheme.in/images/categories/Public%20Safety,Law%20&%20Justice.png"
   },
   {
      "title":"Science, IT & Communications",
      "tagUrl": "technical-course",
      "url": "https://cdn.myscheme.in/images/categories/Science,%20IT%20&%20Communications.png"
   },
   {
      "title":"Skills & Employment",
      "tagUrl": "employment",
      "url": "https://cdn.myscheme.in/images/categories/Skills%20&%20Employment.png"
   },
   {
      "title":"Housing & Shelter",
      "tagUrl": "shelter",
      "url": "https://cdn.myscheme.in/images/categories/Housing%20&%20Shelter.png"
   }
   
]

    context = {
        'categories' : category,
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
        return Schemes.objects.filter(details__icontains=search_input).order_by('-uploadDate')

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
    # model = Schemes
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(context)
    #     context["title"] = context['schemes'].objects
    #     print(context['schemes'])
    #     return context
class DateInput(forms.DateInput):
    input_type = 'date'

class SchemeAdd(CreateView):
    model = Schemes
    fields = ['title','name','brief','eligibility','references','slug','tags','details','category','subcategory','openDate','closeDate']
    # success_url = reverse_lazy('tasks')
    success_url = reverse_lazy('schemes')
    def get_form(self,form_class=None):
        form = super(SchemeAdd,self).get_form(form_class)
        form.fields['openDate'].widget = DateInput()
        form.fields['closeDate'].widget = DateInput()
        return form
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SchemeAdd,self).form_valid(form)

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

class SchemeUpdate(UpdateView):
    model = Schemes
    fields = ['title','name','brief','eligibility','references','slug','tags','details','category','subcategory','openDate','closeDate']

class AboutView(DetailView):
    template_name = 'schemes/about.html'

