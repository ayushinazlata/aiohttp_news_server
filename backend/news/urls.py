from django.urls import path
from .views import NewsListCreateView

urlpatterns = [
    path('api/news/', NewsListCreateView.as_view(), name='news-list-create'),
]
