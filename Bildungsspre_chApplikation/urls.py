from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import views, api_views

urlpatterns = [
    path('', views.RandomWordView.as_view(), name="random_word_view"),
    # path('new/', views.NewWordFormView.as_view(), name="new_word_form"),
    path('new/', login_required(views.WordMultiFormView.as_view(), login_url='/api-auth/login/?next=/new/'), name="new_word_multipart_from"),

    path('random/', api_views.RandomWordAPIView.as_view()),
    path('api/word/', api_views.CreateWordCompleteView.as_view())
]
