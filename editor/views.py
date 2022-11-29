from django.shortcuts import render
from schemes.models import Schemes,Tags, Category
from django.db.models import Q
from django.urls import reverse_lazy
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django import forms

class CustomLoginView(LoginView):
    template_name = 'editor/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('editor')


@login_required
def home(request):
    # context = {
    #     'posts': Schemes.objects.all()
    # }
    return render(request, 'editor/home.html')

class SchemeUpdateListView(LoginRequiredMixin,ListView):
    model = Schemes
    template_name = 'editor/update_scheme.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'schemes'
    ordering = ['uploadDate']
    paginate_by = 8
    queryset = model.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        search_input = self.request.GET.get('search-area') or ''
        context['title'] = 'Update Schemes'
        context['search_input']= search_input
        # print(context)
        return context
    def get_queryset(self):
        # user = get_object_or_404(User, username=self.kwargs.get('username'))
        search_input = self.request.GET.get('search-area') or ''
        return Schemes.objects.filter(Q(details__icontains=search_input)|Q(eligibility__icontains=search_input)|Q(nodalMinistry__icontains=search_input)).order_by('-uploadDate')

class DateInput(forms.DateInput):
    input_type = 'date'

class SchemeUpdate(LoginRequiredMixin,UpdateView):
    model = Schemes
    template_name = 'editor/schemes_form.html'
    fields = ['title','name','brief','eligibility','references','slug','tags','details','category','subcategory','openDate','closeDate','image']
    success_url = reverse_lazy('updatescheme')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit "+self.object.title
        return context
    def get_form(self,form_class=None):
        form = super(SchemeUpdate,self).get_form(form_class)
        # form.fields['category'].widget = forms.TextInput(attrs={"data-role":"tagsinput"})
        form.fields['openDate'].widget = DateInput()
        form.fields['closeDate'].widget = DateInput()
        return form
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SchemeUpdate,self).form_valid(form)

class SchemeAdd(LoginRequiredMixin,CreateView):
    model = Schemes
    template_name = 'editor/schemes_form.html'
    fields = ['title','name','brief','eligibility','references','slug','tags','details','category','subcategory','openDate','closeDate','image']
    # category = Tags.objects.all()
    # success_url = reverse_lazy('tasks')
    success_url = reverse_lazy('editor')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['title']='Add Scheme'
        # search_input = self.request.GET.get('search-area') or ''
        # context['title'] = 'Update Schemes'
        # context['search_input']= search_input
        # # print(context)
        return context
    def get_form(self,form_class=None):
        form = super(SchemeAdd,self).get_form(form_class)
        form.fields['category'].widget = forms.TextInput(attrs={"data-role":"tagsinput"})
        form.fields['openDate'].widget = DateInput()
        form.fields['closeDate'].widget = DateInput()
        return form
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SchemeAdd,self).form_valid(form)
