from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Problem, ProblemSubmission
from .forms import CommentForm, SubmitForm


# List of problems by section
class ProblemsList(ListView):
    template_name = "problems/problems-list.html"
    context_object_name = "problems_list"

    def get_queryset(self):
        problems = self.request.user.get_opened_problems_by_topic(
            self.kwargs.get("topic")
        )
        return [problems.filter(level=k) for k in range(1, 6)]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.kwargs.get("topic")
        context["topic"] = topic

        user = self.request.user
        context["solved_problems"] = user.get_correct_pks(topic)
        context["wrong_problems"] = user.get_wrong_pks(topic)
        context["pending_problems"] = user.get_pending_pks(topic)
        return context


class HaveAccessToProblem(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        problem = get_object_or_404(
            Problem, chapter__topic=self.kwargs["topic"], pk=self.kwargs["pb_pk"]
        )
        return problem.has_access(self.request.user)


class _ProblemView(DetailView):
    context_object_name = "this_sub"

    def setup(self, request, *args, **kwargs):
        self.problem = get_object_or_404(self.problem_model, pk=kwargs["pb_pk"])
        self.sub = int(request.GET.get("sub")) if request.GET.get("sub") else None
        self.user = request.user
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.GET.get("sub") == "0":
            return redirect("sub=0/")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            pass

    def get_object(self, **kwargs):
        if not self.sub:
            return None
        if self.problem.has_solved(self.request.user):
            return self.problem.get_sub(pk=self.sub, correct=True)

        obj = get_object_or_404(self.problem.get_user_subs(self.user), pk=self.sub)
        self.handle_non_correct_sub(obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["problem"] = self.problem
        context["show_btn"] = self.problem.can_submit(self.user)

        context["user_subs"] = self.problem.get_user_subs(self.user)
        if self.object:
            self.object.mark_as_seen(self.user)
            context["comments"] = self.object.get_comments()
        if self.problem.has_solved(self.user):
            context["all_sols"] = self.problem.get_correct_subs()
            context["show_btn"] = False
        elif self.problem.has_draft_sub(self.user):
            context["btn"] = "إكمال المحاولة السابقة"
        else:
            context["btn"] = "إجابة جديدة"
        return context

    def form_valid(self, form):
        sub = self.problem.get_unique_sub(self.user)
        form.instance.set_sub(sub)
        form.instance.set_user(self.user)
        form.save()
        sub.set_status("comment")
        sub.save()
        if self.request.is_ajax():
            return HttpResponse(
                render_to_string(
                    "problems/comments.html", {"comments": [form.instance]}
                )
            )
        return HttpResponseRedirect(self.get_success_url(sub.pk))

    def handle_non_correct_sub(self, sub):
        if sub.can_be_deleted(self.user):
            msg = """هذه الإجابة غير صحيحة. يمكنك الرد في التعليقات، أو  <a href="delete/" class="alert-link">حذف </a> الإجابة السابقة، وتقديم إجابة جديدة."""
            messages.info(self.request, msg)
        if sub.can_comment(self.user):
            self.extra_context = {"cmnt": self.form_class()}


class ProblemView(HaveAccessToProblem, _ProblemView):
    template_name = "problems/problem-view.html"
    form_class = CommentForm
    problem_model = Problem

    def get_success_url(self, sub_pk):
        return (
            reverse_lazy(
                ("problems:pb-view"),
                kwargs={"topic": self.kwargs["topic"], "pb_pk": self.kwargs["pb_pk"]},
            )
            + f"?sub={sub_pk}"
        )


class _ProblemSubmit(CreateView):
    def setup(self, request, *args, **kwargs):
        self.problem = get_object_or_404(self.problem_model, pk=kwargs["pb_pk"])
        self.draft_sub = self.problem_model.objects.get(
            pk=kwargs["pb_pk"]
        ).get_unique_sub(request.user)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not self.problem.can_submit(self.request.user):
            return HttpResponseRedirect(self.get_success_url(None))
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        if self.draft_sub:
            self.initial = {
                "solution": self.draft_sub.solution,
                "ltr_dir": self.draft_sub.ltr_dir,
            }
        return super().get_initial()

    def get_form(self):
        dir_attrs = self.draft_sub.get_dir_attrs() if self.draft_sub else {}
        return self.form_class(dir_attrs=dir_attrs, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context["form"].errors.values())
        context["problem"] = self.problem
        if self.draft_sub:
            context["solution"] = self.draft_sub.solution
            context["ltr_dir"] = self.draft_sub.ltr_dir
            context["show_del"] = True
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.draft_sub:
            self.draft_sub.update(
                obj.solution,
                obj.ltr_dir,
                self.request.POST["sub"],
                self.request.FILES.get("file"),
            )
            obj = self.draft_sub
        else:
            obj.set_student(self.request.user)
            obj.problem_id = self.kwargs["pb_pk"]
            obj.set_status(self.request.POST["sub"])
            obj.set_submited_now()
            obj.save()
        if obj.status == "submit":
            pk = obj.pk
        else:
            pk = None
        return HttpResponseRedirect(self.get_success_url(pk))


class ProblemSubmit(HaveAccessToProblem, _ProblemSubmit):
    model = ProblemSubmission
    form_class = SubmitForm
    template_name = "problems/problem-submit.html"
    problem_model = Problem

    def get_success_url(self, sub_pk):
        url = reverse_lazy(
            "problems:pb-view",
            kwargs={"topic": self.kwargs["topic"], "pb_pk": self.problem.pk},
        )
        if sub_pk:
            return url + f"?sub={sub_pk}"
        return url


class DeleteSubmission(DeleteView):
    template_name = "problems/delete-draft.html"
    problem_model = Problem

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self):
        return self.problem_model.objects.get(pk=self.kwargs["pb_pk"]).get_unique_sub(
            self.request.user
        )

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            "problems:pb-view",
            kwargs={"topic": self.kwargs["topic"], "pb_pk": self.kwargs["pb_pk"]},
        )


class LastCorrectedSubs(ListView):
    template_name = "problems/last-subs.html"
    context_object_name = "user_subs"

    def queryset(self, **kwargs):
        return self.request.user.progress.last_submissions.all()


class LastSolvedProblems(ListView):
    template_name = "problems/last-solved.html"
    context_object_name = "last_solved_problems"

    def get_queryset(self):
        return ProblemSubmission.correct_submissions.last_week().order_by(
            "-submited_on"
        )
