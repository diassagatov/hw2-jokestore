from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/story/random/', views.RandomStoryAPIView.as_view(), name='api-random-story'),
    path('api/story/create/', views.CreateStoryAPIView.as_view(), name='api-create-story'),
    path('api/story/<int:pk>/rank/', views.RankStoryAPIView.as_view(),name='api-rank',),
]
