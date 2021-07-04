from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('polls/', views.IndexView.as_view(), name='polls'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:poll_id>/vote/', views.vote, name='vote'),
    path('user/', views.UserView.as_view(), name='user')
]
