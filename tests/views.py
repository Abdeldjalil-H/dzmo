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

    def get_success_url(self, **kwargs):
        return reverse_lazy('tests:test', kwargs={'pk':self.kwargs['pk']})

class TestResult(ListView):
    template_name = 'tests/test-results.html'
    
    context_object_name = 'answers_list'
    def get_queryset(self, **kwargs):
        pk = self.kwargs['pk']
        return TestAnswer.objects.filter(
                    test_id = pk, 
                    corrected = True).order_by('-mark') 