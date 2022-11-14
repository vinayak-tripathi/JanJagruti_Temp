from django.shortcuts import render
from schemes.models import Schemes,Tags, Category
from django.db.models import Q
from django.urls import reverse_lazy
# Create your views here.
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django import forms

def home(request):
    # context = {
    #     'posts': Schemes.objects.all()
    # }
    return render(request, 'editor/home.html')

class SchemeUpdateListView(ListView):
    model = Schemes
    template_name = 'editor/update_scheme.html'  # <app>/<model>_<viewtype>.html
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

class DateInput(forms.DateInput):
    input_type = 'date'

class SchemeUpdate(UpdateView):
    model = Schemes
    fields = ['title','name','brief','eligibility','references','slug','tags','details','category','subcategory','openDate','closeDate']

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