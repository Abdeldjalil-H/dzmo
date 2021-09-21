from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.conf import settings
from datetime import timedelta
from django.views.generic import(
    ListView,
    CreateView,
    FormView,
)
from django.contrib.auth.mixins import UserPassesTestMixin
from requests.api import request
from problems.models import(
    ProblemSubmission,
    Comment,
    Problem    
)
from accounts.models import User
from .models import MainPagePost, Submissions
from .forms import AddProblemsForm, SendMailForm

class StaffRequired(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class CorrectorsOnly(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_corrector and self.request.user.corrector.problems

class SubsList(CorrectorsOnly, ListView):
    template_name       = 'control/submissions-list.html'
    context_object_name = 'subs_list'
    
    def get_queryset(self):
        order = self.request.GET.getlist('order') if self.request.GET.get('order') else []
        return Submissions.get_problems_subs_by_level(order=order, filters=self.request.user.corrector.get_filters())
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.request.GET.getlist('order') if self.request.GET.get('order') else ['submited_on']
        old_link = '?order=' + '&order='.join(order)
        context['link'] = old_link
        {'pb':'order=problem', 'student':'order=student', 'status':'order=status'}
        return context
        '''

class ProblemCorrection(CorrectorsOnly, CreateView):
    template_name       = 'control/problem-correction.html'
    model               = Comment
    need_form           = False
    fields              = ['ltr_dir','content']
    success_url         = reverse_lazy('control:subs-list')
    submission_model    = ProblemSubmission

    def setup(self, request, *args, **kwargs):
        self.submission = get_object_or_404(self.submission_model, pk=kwargs[self.pk_url_kwarg])
        self.decide = request.GET.get('decide')
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if not request.user.corrector.can_correct(self.submission.problem):
            return HttpResponseForbidden()
        if self.decide != 'to_correct' and self.decide:
            self.submission.set_correcting(False)
            self.submission.save()
            self.extra_context = {'can_correct':True}
        elif not self.decide:
            self.extra_context = {'can_correct':self.submission.can_be_corrected()}
        elif self.submission.can_be_corrected():
            self.need_form = True
            self.extra_context = {'can_correct':True}
            self.submission.set_correcting(True)
            self.submission.save()
        return super().get(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['ltr_dir'].widget.attrs = {'style':'position:relative;margin-left:5px;', 
        'onclick':"change_dir('id_content')",
        }
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['problem']  = self.submission.problem
        context['comments'] = self.submission.get_comments()
        context['this_sub'] = self.submission
        if not self.need_form:
            context['form'] = None      
        return context

    def handle_correct_sub(self):
        self.submission.correct = True
        self.submission.save()
        self.submission.student.add_solved_problem(self.submission.problem)
        self.submission.student.add_points(self.submission.problem.points)
        if self.submission.get_time_since_submit() < timedelta(days=7):
            Submissions.add_correct_sub(self.submission)

    def handle_wrong_sub(self):
        self.submission.correct = False
        self.submission.set_correcting(False)
        self.submission.save()

    def handle_comment_correct_sub(self):
        self.submission.set_status('correct')
        self.submission.save()

    def notify_student(self):
        self.submission.student.progress.last_submissions.add(self.submission)

    def remove_from_subs(self):
        Submissions.remove_sub(self.submission)
    def form_valid(self, form, **kwargs):
        pk = self.submission.pk
        form.instance.user = self.request.user
        form.instance.submission_id = pk
        status = self.request.POST.get('status')
        #the other case is when we send only a comment
        if status:
            self.submission.set_status(status)
            if status == 'correct':
                self.handle_correct_sub()
            else:
                self.handle_wrong_sub()
        else:
            self.handle_comment_correct_sub()
        
        self.remove_from_subs()
        self.notify_student()
        return super().form_valid(form, **kwargs)
        
class MainPage(ListView):
    template_name       = 'control/base.html'
    context_object_name = 'posts'
    def get_queryset(self):
        posts = MainPagePost.objects.filter(publish = True)
        if self.request.user.is_authenticated:
            return posts.order_by('-publish_date')
        return posts.filter(public = True)

def mail(subject,msg, receivers):
    res = send_mail(
        subject = subject,
        message = msg,
        from_email = settings.DEFAULT_FROM_EMAIL,
        recipient_list = receivers,
        fail_silently=False,
    ) 

class SendMail(StaffRequired, FormView):
    template_name  = 'control/send-emails.html'
    form_class     = SendMailForm
    success_url    = reverse_lazy('control:send-mails')

    def form_valid(self, form, **kwargs):
        receivers = [usr.email for usr in form.cleaned_data['receivers']]
        if form.cleaned_data['to_all_students']:
            receivers += [student.email for student in User.objects.filter(grade__lt = 4)]
        if form.cleaned_data['to_all_staff']:
            receivers += [staff.email for staff in User.objects.filter(is_staff = True)]
        send_mail(
            subject = form.cleaned_data['subject'],
            message = form.cleaned_data['msg'],
            from_email = settings.DEFAULT_FROM_EMAIL,
            recipient_list = receivers,
            fail_silently=False,
                ) 
        return super().form_valid(form, **kwargs)

class AddProblems(StaffRequired,FormView):
    template_name   = 'control/add_problems.html'
    form_class      = AddProblemsForm
    success_url     = reverse_lazy('control:add-problems')

    def add_problems(self, form):
        return add_problems(**form.cleaned_data)
    def form_valid(self, form,**kwargs):
        self.add_problems(form)
        '''
        add_problems(form.cleaned_data['statements'],
                    form.cleaned_data['chapter'].pk,
                    form.cleaned_data['level'],
                    )
        '''
        return super().form_valid(form, **kwargs)

def add_problems(**kwargs):
    chapter_id = kwargs['chapter'].pk
    statements_list = kwargs['statements'].replace('\n',' ').split('\item')
    level = kwargs['level']
    for pr in statements_list:
        if pr:
            Problem.objects.create(statement = pr, chapter_id = chapter_id, level= level)
