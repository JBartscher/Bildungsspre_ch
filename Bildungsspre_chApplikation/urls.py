from django.urls import path
from . import views

urlpatterns = [
    path('random/', views.RandomWordView.as_view()),
    path('word/', views.CreateWordCompleteView.as_view())
]
