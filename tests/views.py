from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import(
    FormView, 
    ListView,
)
from django.urls import reverse_lazy
from .models import Test, TestAnswer
from .forms import UploadFileForm
class TestsList(ListView):
    template_name = 'tests/tests-list.html'
    queryset = Test.objects.all()
    context_object_name = 'tests_list'
class TestAnswerView(FormView):
    template_name   = 'tests/test.html'
    form_class      = UploadFileForm
    fields = ['files']
    context_object_name = 'forms'

    def setup(self, request, *args, **kwargs):
        self.test = get_object_or_404(Test, pk=kwargs.get('pk'))
        return super().setup(request, *args, **kwargs)
    def get_success_url(self, **kwargs):
        return reverse_lazy('tests:test', kwargs={'pk':self.kwargs['pk']})
    
    '''
    show test if the student is taking it, or time is over,
    show take test button if not taken before, and time,
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.test.started:
            context['forms'] = None
            return context
        if available := self.test.is_available_for(self.request.user):
            context['show_test'] = available
            context['test_problems'] = self.test.get_problems()
        else:
            context['show_btn'] = True
        return context
    
    def form_valid(self, form):
        if self.test.is_participant(self.request.user):
            return super().form_valid(form)  
        TestAnswer.create(student=self.request.user, test=self.test)
        return HttpResponseRedirect(self.get_success_url())
        
class TestResult(ListView):
    template_name = 'tests/test-results.html'
    
    context_object_name = 'answers_list'
    def get_queryset(self, **kwargs):
        pk = self.kwargs['pk']
        return TestAnswer.objects.filter(
                    test_id = pk, 
                    corrected = True).order_by('-mark') 