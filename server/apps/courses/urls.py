from django.urls import path
from . import views


urlpatterns = [
	path('contents/', views.contents),
	path('page/', views.page),
	path('course/', views.Course.as_view()),
]
