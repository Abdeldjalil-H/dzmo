from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

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
            context[
                "completed_chapters"
            ] = self.request.user.progress.completed_chapters.filter(topic=topic)
            context[
                "solved_exercices"
            ] = self.request.user.progress.solved_exercices.filter(chapter__topic=topic)
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

        context[
            "solved_exercices"
        ] = self.request.user.progress.solved_exercices.filter(chapter=chapter)
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


def get_ex(category, CHOICES=None):
    if category == "result":

        class ExerciceForm(forms.Form):
            question = forms.CharField(label="", required=False)

        return ExerciceForm
    elif category == "one":

        class ExerciceForm(forms.Form):
            question = forms.ChoiceField(
                choices=[(f"{k}", CHOICES[k]) for k in range(0, len(CHOICES))],
                widget=forms.RadioSelect,
                label="",
                required=False,
            )

        return ExerciceForm
    else:

        class ExerciceForm(forms.Form):
            question = forms.MultipleChoiceField(
                choices=[(f"{k}", CHOICES[k]) for k in range(0, len(CHOICES))],
                widget=forms.CheckboxSelectMultiple,
                label="",
                required=False,
            )

        return ExerciceForm


def exercice_view(request, pk, chapter_slug, **kwargs):
    exercice = Exercice.objects.get(id=pk)
    category = exercice.category
    choices = exercice.get_choices()
    chapter = Chapter.objects.get(slug=chapter_slug)
    if not request.user.is_authenticated or not chapter.has_access(request):
        return redirect(
            reverse(
                "lessons:chapter",
                kwargs={"topic": chapter.topic, "chapter": chapter_slug},
            )
        )
    form = get_ex(category=category, CHOICES=choices)(request.POST or None)
    template_name = "lessons/exercice.html"
    context = {
        "form": form,
        "exercice": exercice,
        "chapter": exercice.chapter,
        "solved_exercices": request.user.progress.solved_exercices.filter(
            chapter=chapter
        ),
        "wrong_exercices": [
            sol.exercice
            for sol in request.user.exercicesolution_set.filter(
                exercice__chapter=chapter
            )
        ],
    }
    if exercice in request.user.progress.solved_exercices.all():
        context["correct"] = True
        if exercice.category != "result":
            context["answer"] = [int(x) for x in exercice.solution.split(",")]
        return render(request, template_name, context)
    if request.method == "POST":
        if form.is_valid():
            sols = request.user.exercicesolution_set
            obj = sols.filter(exercice=exercice)
            if not obj:
                obj = ExerciceSolution(student=request.user, exercice_id=pk)
            else:
                obj = obj.first()
            ans = ""
            if exercice.category == "multiple":
                for char in form.cleaned_data["question"]:
                    ans += str(char) + ","
                ans = ans[:-1]
            else:
                ans = str(form.cleaned_data["question"]).replace(" ", "")

            obj.answer = ans
            obj.correct = obj.answer == exercice.solution
            # if all the exercices are soloved, the open new chapter
            if obj.correct:
                request.user.progress.solved_exercices.add(exercice)
                request.user.progress.add_points(exercice.points)
                ex_of_chapter = chapter.exercice_set.all()
                if all(
                    ex in request.user.progress.solved_exercices.all()
                    for ex in ex_of_chapter
                ):
                    print("hi")
                    request.user.progress.completed_chapters.add(chapter)
            obj.add_try()
            obj.save()
            return redirect(
                reverse(
                    "lessons:exercice",
                    kwargs={
                        "topic": chapter.topic,
                        "chapter_slug": chapter.slug,
                        "pk": exercice.pk,
                    },
                )
            )

    return render(request, template_name, context)
