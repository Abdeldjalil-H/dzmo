from django.urls import path

from .views import ChapterPreview, LessonDetail, LessonsList, exercice_view

app_name = "lessons"

urlpatterns = [
    path("<slug:topic>/", LessonsList.as_view(), name="list"),
    path("<topic>/<chapter>/", ChapterPreview.as_view(), name="chapter"),
    path("<topic>/<chapter>/<slug:slug>/", LessonDetail.as_view(), name="detail"),
    path("<topic>/<chapter_slug>/ex/<int:pk>/", exercice_view, name="exercice"),
]
