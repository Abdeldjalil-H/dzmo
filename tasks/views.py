from django.contrib.messages.api import success
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from django.views.generic.edit import CreateView, DeleteView
from .models import (
    Task,
    TaskComment, 
    TaskProblem,
    TaskProblemSubmission,
)
from control.views import (
    ProblemCorrection, 
    SubsList,
    AddProblems,
)
from .forms import SubmitForm, CommentForm, AddProblemsForm
class TasksList(ListView):
    template_name       = 'tasks/tasks-list.html'
    context_object_name = 'tasks_list'

    def get_queryset(self):
        return self.request.user.team.get_tasks()
    
class TaskProblemsList(ListView):
    template_name       = 'tasks/problems-list.html'
    context_object_name = 'problems_list'
    
    def get_queryset(self, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        return task.get_problems_by_level()
        
class TaskPbSubmit(CreateView):
    model = TaskProblemSubmission
    form_class = SubmitForm
    template_name = 'tasks/task-problem.html'
    
    def setup(self, request, *args, **kwargs):
        self.problem = get_object_or_404(TaskProblem, pk=kwargs['pb_pk'])
        self.draft_sub = TaskProblem.objects.get(pk = kwargs['pb_pk']).get_draft_sub(request.user)
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if not self.problem.can_submit(self.request.user):
            return HttpResponseRedirect(reverse_lazy('tasks:pb-view', kwargs={'task_pk':self.kwargs['task_pk'], 'pb_pk':self.problem.pk}))
        return super().get(request, *args, **kwargs)
    
    def get_initial(self):
        if self.draft_sub:
            self.initial = {'solution':self.draft_sub.solution,
                            'ltr_dir':self.draft_sub.ltr_dir,
            } 
        return super().get_initial()
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('tasks:pb-view', kwargs={'task_pk':self.kwargs['task_pk'], 'pb_pk':self.problem.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problem'] = self.problem
        context['show_del'] = True if self.draft_sub else False
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.draft_sub:
            self.draft_sub.update(obj.solution, obj.ltr_dir, self.request.POST['sub'])
        else:                 
            obj.set_student(self.request.user)
            obj.problem_id = self.kwargs['pb_pk']
            obj.set_status(self.request.POST['sub'])
            obj.save()
        return HttpResponseRedirect(self.get_success_url())

class TaskPbView(DetailView):
    template_name = 'tasks/task-problem.html'
    context_object_name = 'this_sub'
    form_class = CommentForm
    def get_success_url(self, sub_pk):
        return reverse_lazy(('tasks:pb-view'), kwargs={'task_pk':self.kwargs['task_pk'], 'pb_pk':self.problem.pk}) + f'?sub={sub_pk}'
    def setup(self, request, *args, **kwargs):
        self.problem = get_object_or_404(TaskProblem, pk=kwargs['pb_pk'])
        self.sub = int(request.GET.get('sub')) if request.GET.get('sub') else None
        self.user = request.user
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if request.GET.get('sub') == '0':
            return redirect('sub=0/')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        sub = self.problem.get_sub(student=self.user)
        form.instance.set_sub(sub)
        form.instance.set_user(self.user)
        form.save()
        sub.set_status('comment')
        sub.save()
        return HttpResponseRedirect(self.get_success_url(sub.pk))
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)   
        else:
            pass
    def handle_non_correct_sub(self, sub):
        if sub.can_be_deleted(self.user):
            msg = '''هذه الإجابة غير صحيحة. يمكنك الرد في التعليقات، أو  <a href="sub=0/delete/" class="alert-link">حذف </a> الإجابة السابقة، وتقديم إجابة جديدة.'''
            messages.info(self.request, msg)
        if sub.can_comment(self.user):
            self.extra_context = {'cmnt':self.form_class()}
    def get_object(self, **kwargs):
        if not self.sub:
            return None
        if self.problem.has_solved(self.request.user):
            return self.problem.get_sub(pk=self.sub)

        obj = get_object_or_404(self.problem.get_user_subs(self.user), pk=self.sub)
        self.handle_non_correct_sub(obj)
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problem'] = self.problem
        context['show_btn'] = self.problem.can_submit(self.user)
        #check if this_sub can be deleted
        
        #btn text and submit value
        context['user_subs'] = self.problem.get_user_subs(self.user)
        if self.object:
            context['comments'] = self.object.get_comments()
        if self.problem.has_solved(self.user):
            context['all_sols'] = self.problem.get_all_subs()
            context['show_btn'] = False
        elif self.problem.has_draft_sub(self.user):
            context['btn'] = 'إكمال المحاولة السابقة'
        else:
            context['btn'] = 'إجابة جديدة'
        return context

class DeleteDraft(DeleteView):
    template_name = 'problems/delete-draft.html'
    problem_model = TaskProblem
    #pk_url_kwarg = 'sub_pk'
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.soft_delete()
        return HttpResponseRedirect(self.get_success_url())
    def get_object(self):
        return self.problem_model.objects.get(pk=self.kwargs['pb_pk']).get_draft_sub(self.request.user)

    def get_success_url(self):
        return reverse_lazy(('tasks:pb-view'), kwargs={'task_pk':self.kwargs['task_pk'], 'pb_pk':self.kwargs['pb_pk']})
class TaskSubsList(SubsList):
 
    def get_context_data(self, **kwargs):
        return {self.context_object_name:Task.objects.get(pk = self.kwargs['task_pk']).get_subs_by_level()}

class TaskPbsCorrection(ProblemCorrection):
    submission_model    = TaskProblemSubmission
    model               = TaskComment
    pk_url_kwarg = 'sub_pk'

    def get_success_url(self):
        return reverse_lazy(('tasks:task-subs-list'), kwargs={'task_pk':self.kwargs['task_pk']})
    def handle_correct_sub(self):
        self.submission.correct = True
        self.submission.save()

    def notify_student(self):
        pass

class AddProblems(AddProblems):
    form_class = AddProblemsForm

    def add_problems(self, form):
        return add_problems(**form.cleaned_data)

def add_problems(**kwargs):
    statements_list = kwargs['statements'].replace('\n',' ').split('\item')
    level = kwargs['level']
    task = kwargs['task']
    for pr in statements_list:
        if pr:
            task.problems.add(TaskProblem.objects.create(statement = pr, task = task.pk, level= level))