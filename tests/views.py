from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
#from django.core.files.storage import get_storage_class
#from .models import answer_file_path
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
        context = {'duration': self.test.duration, 'starts_at': self.test.starts_at, 'ends_at': self.test.ends_at}
        if not self.test.started:
            return context
        if not self.test.is_available_for(self.request.user):
            context['show_btn'] = True
            return context
        
        context |={'show_test': True, 
                'ltr': self.test.ltr,
                'test_problems': self.test.get_problems()
        }
        
        if not self.test.is_over:
            context['form'] = self.get_form()
            #media_storage = get_storage_class()()
            #sub = 
            #url = media_storage.url(name=answer_file_path(sub,pb_pk=2))
            context['show_link'] = self.test.get_submission(self.request.user).get_files_status()
            #context['link'] = url
        return context
    
    def get_form(self):
        if self.request.method == 'GET':
            return self.form_class(**self.get_form_kwargs())
        return self.form_class(instance=self.test.get_submission(self.request.user), **self.get_form_kwargs())
    
    def post(self, request, *args, **kwargs):
        if self.test.is_over:
            return HttpResponseRedirect(self.get_success_url())
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        if self.test.is_participant(self.request.user):
            pb_number = int(self.request.POST.get('pb'))
            if pb_number <= self.test.number_of_pbs:
                form.save(pb_num=pb_number)
        else: 
            TestAnswer.create(student=self.request.user, test=self.test).save()
        return HttpResponseRedirect(self.get_success_url())
        
class TestResult(ListView):
    template_name = 'tests/test-results.html'
    
    context_object_name = 'answers_list'
    def get_queryset(self, **kwargs):
        pk = self.kwargs['pk']
        return TestAnswer.objects.filter(
                    test_id = pk, 
                    corrected = True).order_by('-mark') 