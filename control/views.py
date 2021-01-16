from django.shortcuts import(
    render, 
    get_object_or_404, 
    HttpResponse,
    redirect,
)
from django.core.mail import send_mail
from django.urls import reverse_lazy,reverse
from django.conf import settings
from django.views.generic import(
    ListView,
    CreateView,
    FormView,
)
from django.contrib.auth.mixins import UserPassesTestMixin
from problems.models import(
    ProblemSubmission,
    Comment,
    Problem
    
)
from accounts.models import User
from .models import MainPagePost
from .forms import AddProblemsForm, SendMailForm
class StaffRequired(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_corrector
#class SubsList(UserPassesTestMixin, ListView):
class SubsList(StaffRequired, ListView):
    template_name       = 'control/submissions-list.html'
    context_object_name = 'subs_list'
    queryset            = ProblemSubmission.objects.filter(status__in = ['submit', 'comment'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.queryset
        subs_by_level =[]
        for k in range(1,6):
            subs_by_level.append(qs.filter(problem__level = k))
        context['subs_list'] = subs_by_level
        return context

class ProblemCorrection(StaffRequired, CreateView):
    template_name       = 'control/problem-correction.html'
    model               = Comment
    fields              = ['content']
    success_url         = reverse_lazy('control:subs-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        this_sub = get_object_or_404(ProblemSubmission,id = pk)
        context['problem']  = this_sub.problem
        context['comments'] = this_sub.comments.all()
        context['this_sub'] = this_sub

        if self.request.method == 'GET':
            decide = self.request.GET.get('decide')
            if decide == 'to_correct':
                if this_sub.correction_in_progress:
                    context['form'] = None
                    return context
                this_sub.correction_in_progress = True
                context['in_correction'] = True
                this_sub.save()
            elif decide == 'cancel_correction':
                this_sub.correction_in_progress = False
                this_sub.save()

        context['judge']    = not this_sub.correct
        context['correction_form'] = context['form']
        context['form'] = None
        return context

    def form_valid(self, form, **kwargs):
        pk = self.kwargs.get('pk')
        form.instance.user          = self.request.user
        form.instance.submission_id = pk
        this_sub = get_object_or_404(ProblemSubmission,id = pk)
        status = self.request.POST['status']
        #the other case is when we send only a comment
        if status:
            this_sub.status = status
            this_sub.save()
            #the 2nd condition: to run this only the first time
            if this_sub.status == 'correct' and not this_sub.correct:
                this_sub.correct = True
                this_sub.student.progress.solved_problems.add(this_sub.problem)
                this_sub.save()
                this_sub.student.progress.add_points(this_sub.problem.points)
            else:
                this_sub.correct = False
                this_sub.correction_in_progress = False
                this_sub.save()
        else:
            this_sub.status = 'correct'
            this_sub.save()
        this_sub.student.progress.last_submissions.add(this_sub)
        return super().form_valid(form, **kwargs)
        
class MainPage(ListView):
    template_name       = 'control/base.html'
    context_object_name = 'posts'
    def get_queryset(self):
        posts = MainPagePost.objects.filter(publish = True)
        if self.request.user.is_authenticated:
            return posts.order_by('-publish_date')
        return posts.filter(public = True)
def mail(request, subject,msg, receivers):
    res = send_mail(
        subject = subject,
        message = msg,
        from_email = settings.DEFAULT_FROM_EMAIL,
        recipient_list = receivers,
        fail_silently=False,
    ) 

class SendMail(FormView):
    template_name  = 'control/send-emails.html'
    form_class     = SendMailForm
    success_url    = reverse_lazy('control:send-mails')

    def form_valid(self, form, **kwargs):
        receivers = [usr.email for usr in form.cleaned_data['receivers']]
        if form.cleaned_data['to_all_students']:
            receivers += [stuent.email for student in User.objects.filter(grade__lt = 4)]
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

    def form_valid(self, form,**kwargs):
        add_problems(form.cleaned_data['statements'],
                    form.cleaned_data['chapter'].pk,
                    form.cleaned_data['level'],
                    )
        return super().form_valid(form, **kwargs)

def add_problems(statements_str, chapter_id, level):
    statements_list = statements_str.replace('\n',' ').split('\item')
    for pr in statements_list:
        if pr:
            Problem.objects.create(statement = pr, chapter_id = chapter_id, level= level)