from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import Chapter, Lesson, ExerciceSolution, Exercice
from django import forms


class LessonsList(ListView):
    template_name = "lessons/lessons-list.html"
    context_object_name = "chapters"

    def get_queryset(self, **kwargs):
        return Chapter.objects.filter(topic=self.kwargs.get("topic"), publish=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.kwargs.get("topic")
        if self.request.user.is_authenticated:
            context["completed_chapters"] = self.request.user.completed_chapters.filter(
                topic=topic
            )

            exercises = Exercice.objects.with_status(student=self.request.user).filter(
                chapter__topic=topic
            )

            exercises_by_chapter = defaultdict(list)
            for ex in exercises:
                exercises_by_chapter[ex.chapter_id].append(ex)

            for chapter in context["chapters"]:
                chapter.exercices_with_status = exercises_by_chapter.get(chapter.id, [])

        return context


class LessonDetail(DetailView):
    template_name = "lessons/lesson-detail.html"
    context_object_name = "lesson"
    model = Lesson

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapter = get_object_or_404(Chapter, slug=self.kwargs.get("chapter"))
        context["chapter"] = chapter

        if not self.request.user.is_authenticated:
            if chapter.prereq_chapters:
                context["lesson"] = None
            return context

        access = chapter.has_access(self.request)
        if not access:
            context["lesson"] = None
            return context

        context["exercices"] = Exercice.objects.with_status(
            student=self.request.user
        ).filter(chapter=chapter)
        return context


class ChapterPreview(DetailView):
    template_name = "lessons/chapter.html"
    context_object_name = "chapter"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['access'] = context['chapter'].has_access()
    def get_object(self, **kwargs):
        return get_object_or_404(Chapter, slug=self.kwargs["chapter"])


def get_exercise_form(category, CHOICES=None):
    if category == "result":

        class ExerciceForm(forms.Form):
            question = forms.CharField(label="", required=False)

    elif category == "one":

        class ExerciceForm(forms.Form):
            question = forms.ChoiceField(
                choices=[(f"{k}", CHOICES[k]) for k in range(0, len(CHOICES))],
                widget=forms.RadioSelect,
                label="",
                required=False,
            )

    else:

        class ExerciceForm(forms.Form):
            question = forms.MultipleChoiceField(
                choices=[(f"{k}", CHOICES[k]) for k in range(0, len(CHOICES))],
                widget=forms.CheckboxSelectMultiple,
                label="",
                required=False,
            )

    return ExerciceForm


class ExerciceView(LoginRequiredMixin, View):
    template_name = "lessons/exercice.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pk = kwargs.get("pk")
        self.chapter_slug = kwargs.get("chapter_slug")
        exercice = Exercice.objects.select_related("chapter").get(id=self.pk)
        self.category = exercice.category
        self.choices = exercice.get_choices()
        self.chapter = exercice.chapter
        from django.db.models import Exists, OuterRef

        chapter_exercises = Exercice.objects.with_status(student=request.user).filter(
            chapter=exercice.chapter, submissions__student_id=request.user.id
        )
        self.chapter_exercises = chapter_exercises
        self.exercice = next(ex for ex in chapter_exercises if ex.pk == self.pk)

    def dispatch(self, request, *args, **kwargs):
        if not self.chapter.has_access(request) or (
            request.method == "POST" and self.exercice.solved
        ):
            return redirect(
                reverse(
                    "lessons:chapter",
                    kwargs={"topic": self.chapter.topic, "chapter": self.chapter_slug},
                )
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self):
        context = {
            "form": get_exercise_form(category=self.category, CHOICES=self.choices)(),
            "exercice": self.exercice,
            "chapter": self.exercice.chapter,
            "exercices": self.chapter_exercises,
        }
        if self.exercice.solved:
            context["correct"] = True
            if self.exercice.category != "result":
                context["answer"] = [int(x) for x in self.exercice.solution.split(",")]
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = get_exercise_form(category=self.category, CHOICES=self.choices)(
            request.POST
        )
        if form.is_valid():
            submission = ExerciceSolution.objects.filter(
                student=request.user, exercice=self.exercice
            ).first()
            if not submission:
                submission = ExerciceSolution(student=request.user, exercice_id=self.pk)

            ans = ""
            if self.exercice.category == "multiple":
                ans = ",".join(str(char) for char in form.cleaned_data["question"])
            else:
                ans = str(form.cleaned_data["question"]).replace(" ", "")

            submission.answer = ans
            submission.correct = submission.answer == self.exercice.solution

            if submission.correct:
                request.user.add_points(self.exercice.points)
                if all(ex.solved for ex in self.chapter_exercises if ex.pk != self.pk):
                    request.user.completed_chapters.add(self.chapter)

            submission.add_try()
            submission.save()

            return redirect(
                reverse(
                    "lessons:exercice",
                    kwargs={
                        "topic": self.chapter.topic,
                        "chapter_slug": self.chapter.slug,
                        "pk": self.exercice.pk,
                    },
                )
            )

        context = self.get_context_data()
        context["form"] = form
        return render(request, self.template_name, context)
