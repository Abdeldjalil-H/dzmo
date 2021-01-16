from django.shortcuts import(
    render, 
    get_object_or_404, 
    HttpResponse,
    redirect,
)
from django.core.mail import send_mail
from django.urls import reverse_lazy,reverse
from django.views.generic import(
    ListView,
    CreateView,
)
from django.contrib.auth.mixins import UserPassesTestMixin
from problems.models import(
    ProblemSubmission,
    Comment,
    
)
from .models import MainPagePost
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
            return posts
        return posts.filter(public = True)
def verify_mail(request):
    res = send_mail(
        subject = 'Subject here',
        message = 'Here is the message.',
        from_email = 'algerianimoteam@gmail.com',
        recipient_list = ['djaloulehez3@gmail.com'],
        fail_silently=False,
    )    
    return HttpResponse(f"Email sent to {res} members")
