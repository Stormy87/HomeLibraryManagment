from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('book/add/', views.book_add, name='book_add'),
    path('book/<int:book_id>/', views.book_detail, name='book'),
    path('book/<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:book_id>/delete/', views.book_delete, name='book_delete'),
    path('book/<int:book_id>/toggle-read/', views.book_toggle_read, name='book_toggle_read'),
    path('book/<int:book_id>/toggle-favorite/', views.book_toggle_favorite, name='book_toggle_favorite'),
    path('book/<int:book_id>/note/add/', views.note_add, name='note_add'),

    path('author/<int:author_id>/', views.author_detail, name='author'),
    path('author/<int:author_id>/edit/', views.author_edit, name='author_edit'),

    path('publisher/<int:publisher_id>/', views.publisher_detail, name='publisher'),
    path('publisher/<int:publisher_id>/edit/', views.publisher_edit, name='publisher_edit'),

    path('series/<int:series_id>/', views.series_detail, name='series'),

    path('note/<int:note_id>/', views.note_detail, name='note'),

    path('dictionaries/', views.dictionaries_index, name='dictionaries'),
    path('dictionaries/<str:dict_type>/', views.dictionary_list, name='dictionary_list'),
    path('dictionaries/<str:dict_type>/add/', views.dictionary_add, name='dictionary_add'),
    path('dictionaries/<str:dict_type>/<int:item_id>/edit/', views.dictionary_edit, name='dictionary_edit'),
    path('dictionaries/<str:dict_type>/<int:item_id>/delete/', views.dictionary_delete, name='dictionary_delete'),
]
