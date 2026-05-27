from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:book_id>/', views.book, name='book'),
    path('author/<int:author_id>/', views.author, name='author'),
    path('authors/', views.authors_list, name='authors_list'),
    path('publisher/<int:publisher_id>/', views.publisher, name='publisher'),
    path('publishers/', views.publishers_list, name='publishers_list'),
    path('series/', views.series_list, name='series_list'),
    path('series/<int:series_id>/', views.series, name='series'),
    path('note/<int:note_id>/', views.note, name='note'),
    path('notes/', views.notes_list, name='notes_list')
]