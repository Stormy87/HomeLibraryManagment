from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:book_id>/', views.book, name='book'),
    path('author/<int:author_id>/', views.author, name='author'),
    path('publisher/<int:publisher_id>/', views.publisher, name='publisher'),
    path('series/<int:series_id>/', views.series, name='series'),
    path('note/<int:note_id>/', views.note, name='note'),
    
]