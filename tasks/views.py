from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_list_or_404, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView

from control.views import AddProblems, ProblemCorrection, SubsList
from problems.views import DeleteSubmission, _ProblemSubmit, _ProblemView

from .forms import AddProblemsForm, CommentForm, SubmitForm
from .models import Task, TaskComment, TaskProblem, TaskProblemSubmission


class CheckTeam(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        task = Task.objects.get(pk=self.kwargs["task_pk"])
        return task.has_access(self.request.user)


class TasksList(ListView):
    template_name = "tasks/tasks-list.html"
    context_object_name = "tasks_list"

    def get_queryset(self):
        user = self.request.user
        if user.is_team_member():
            return {"team": user.team.get_name(), "tasks": user.team.get_tasks()}


class TaskProblemsList(CheckTeam, ListView):
    template_name = "tasks/problems-list.html"
    context_object_name = "problems_list"

    def get_queryset(self, **kwargs):
        self.task = get_object_or_404(Task, pk=self.kwargs["task_pk"])
        return self.task.get_problems_by_level()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["solved_problems"] = self.task.get_correct_pks(user)
        context["wrong_problems"] = self.task.get_wrong_pks(user)
        context["pending_problems"] = self.task.get_pending_pks(user)
        return context


class TaskPbSubmit(CheckTeam, _ProblemSubmit):
    model = TaskProblemSubmission
    form_class = SubmitForm
    template_name = "tasks/task-problem-submit.html"
    problem_model = TaskProblem

    def get_success_url(self, sub_pk):
        url = reverse_lazy(
            "tasks:pb-view",
            kwargs={"task_pk": self.kwargs["task_pk"], "pb_pk": self.problem.pk},
        )
        if sub_pk:
            return f"{url}?sub={sub_pk}"
        return url


class TaskPbView(CheckTeam, _ProblemView):
    template_name = "tasks/task-problem-view.html"
    form_class = CommentForm
    problem_model = TaskProblem

    def get_success_url(self, sub_pk):
        return (
            reverse_lazy(
                ("tasks:pb-view"),
                kwargs={"task_pk": self.kwargs["task_pk"], "pb_pk": self.problem.pk},
            )
            + f"?sub={sub_pk}"
        )


class DeleteSubmission(DeleteSubmission):
    problem_model = TaskProblem

    def get_success_url(self):
        return reverse_lazy(
            ("tasks:pb-view"),
            kwargs={"task_pk": self.kwargs["task_pk"], "pb_pk": self.kwargs["pb_pk"]},
        )


class TaskSubsList(SubsList):
    def get_context_data(self, **kwargs):
        return {
            self.context_object_name: Task.objects.get(
                pk=self.kwargs["task_pk"]
            ).get_subs_by_level()
        }


class TaskPbsCorrection(ProblemCorrection):
    submission_model = TaskProblemSubmission
    model = TaskComment
    pk_url_kwarg = "sub_pk"
    template_name = "tasks/correction-subs-list.html"

    def get_success_url(self):
        return reverse_lazy(
            ("tasks:task-subs-list"), kwargs={"task_pk": self.kwargs["task_pk"]}
        )

    def remove_from_subs(self):
        pass

    def notify_student(self):
        self.submission.student.add_task_correction_notif(self.submission)


class LastCorrectedSubs(ListView):
    template_name = "tasks/last-corrected-subs.html"
    context_object_name = "user_subs"

    def get_queryset(self):
        return self.request.user.get_last_tasks_subs()


class CorrectSolsByTask(CheckTeam, ListView):
    template_name = "tasks/correct-sols-by-task.html"
    context_object_name = "sols"

    def get_queryset(self):
        return get_list_or_404(
            TaskProblemSubmission.correct,
            problem__task_id=self.kwargs["task_pk"],
        )


class AddProblems(AddProblems):
    form_class = AddProblemsForm
    success_url = reverse_lazy(("tasks:add-pbs"))

    def add_problems(self, form):
        return add_problems(**form.cleaned_data)


def add_problems(**kwargs):
    statements_list = kwargs["statements"].replace("\n", " ").split("\item")
    level = kwargs["level"]
    task = kwargs["task"]
    for pr in statements_list:
        if pr:
            task.problems.add(
                TaskProblem.objects.create(statement=pr, task=task.pk, level=level)
            )
