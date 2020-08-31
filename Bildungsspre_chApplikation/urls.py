from django.urls import path
from . import views

urlpatterns = [
    path('', views.RandomWordView.as_view()),
    path('random/', views.RandomWordAPIView.as_view()),
    path('word/', views.CreateWordCompleteView.as_view())
]
