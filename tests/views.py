from django.shortcuts import get_object_or_404
from django.views.generic import(
    FormView, 
    ListView,
)
from django.urls import reverse_lazy
from .models import Test, TestAnswer
from .forms import UploadFileForm
class TestsList(ListView):
    template_name = 'tests-list.html'
    model = Test
    context_object_name = 'tests_list'
class TestAnswerView(FormView):
    template_name   = 'tests/test.html'
    form_class      = UploadFileForm
    fields = ['answer_file']

    def get_success_url(self, **kwargs):
        return reverse_lazy('tests:test', kwargs={'pk':self.kwargs['pk']})

    def get_user_ans(self, pk):
        return self.request.user.testanswer_set.get(
                test_id = pk)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        test = get_object_or_404(Test, pk = pk)
        context['test'] = test
        print(self.request.POST)
        if self.request.POST.get('take-test'):
            self.request.user.test_set.add(test)
            TestAnswer.objects.get_or_create(
                test_id = self.kwargs.get('pk'),
                student = self.request.user,
                )
        context['take_test']= test in self.request.user.test_set.all()
        if context['take_test']:
            context['can_answer'] = self.get_user_ans(pk).can_answer
        return context

    def form_valid(self, form, **kwargs):
        user_ans = self.get_user_ans(self.kwargs['pk'])
        if user_ans.can_answer:
            user_ans.add_ans_file(form.cleaned_data['file'])
        user_ans.submited_now()
        return super().form_valid(form,**kwargs)
