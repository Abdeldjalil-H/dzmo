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
            context["solved_exercices"] = self.request.user.solved_exercices.filter(
                chapter__topic=topic
            )
            context["wrong_exercices"] = [
                sol.exercice
                for sol in self.request.user.exercicesolution_set.filter(correct=False)
            ]
        return context


class LessonDetail(DetailView):
    template_name = "lessons/lesson-detail.html"
    context_object_name = "lesson"
    # the lesson will be token in automatic way
    # bcz we have <slug:slug> in the url works with pk also
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

        context["solved_exercices"] = self.request.user.solved_exercices.filter(
            chapter=chapter
        )
        context["wrong_exercices"] = [
            sol.exercice
            for sol in self.request.user.exercicesolution_set.filter(
                exercice__chapter=chapter
            )
        ]
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
        self.exercice = Exercice.objects.get(id=self.pk)
        self.category = self.exercice.category
        self.choices = self.exercice.get_choices()
        self.chapter = Chapter.objects.get(slug=self.chapter_slug)

    def dispatch(self, request, *args, **kwargs):
        if not self.chapter.has_access(request):
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
            "solved_exercices": self.request.user.solved_exercices.filter(
                chapter=self.chapter
            ),
            "wrong_exercices": [
                sol.exercice
                for sol in self.request.user.exercicesolution_set.filter(
                    exercice__chapter=self.chapter
                )
            ],
        }
        if self.exercice in self.request.user.solved_exercices.all():
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
            sols = request.user.exercicesolution_set
            obj = sols.filter(exercice=self.exercice).first()
            if not obj:
                obj = ExerciceSolution(student=request.user, exercice_id=self.pk)

            ans = ""
            if self.exercice.category == "multiple":
                ans = ",".join(str(char) for char in form.cleaned_data["question"])
            else:
                ans = str(form.cleaned_data["question"]).replace(" ", "")

            obj.answer = ans
            obj.correct = obj.answer == self.exercice.solution

            if obj.correct:
                request.user.solved_exercices.add(self.exercice)
                request.user.add_points(self.exercice.points)
                ex_of_chapter = self.chapter.exercice_set.all()
                if all(
                    ex in request.user.solved_exercices.all() for ex in ex_of_chapter
                ):
                    request.user.completed_chapters.add(self.chapter)

            obj.add_try()
            obj.save()

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
