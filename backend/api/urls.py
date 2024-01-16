from django.urls import path
from .views import GenerateWordCloudView

urlpatterns = [
    path(
        "generate_wordcloud/",
        GenerateWordCloudView.as_view(),
        name="generate_wordcloud",
    ),
]
