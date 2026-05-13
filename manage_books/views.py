from django.shortcuts import HttpResponse, render

def index(request):
    return render(request, 'manage_books/index.html.jinja')

def book(request, book_id):
    return render(request, 'manage_books/book.html.jinja', {'book_id': book_id})

def author(request, author_id):
    return render(request, 'manage_books/author.html.jinja', {'author_id': author_id})

def publisher(request, publisher_id):
    return render(request, 'manage_books/publisher.html.jinja', {'publisher_id': publisher_id})

def series(request, series_id):
    return render(request, 'manage_books/series.html.jinja', {'series_id': series_id})

def note(request, note_id):
    return render(request, 'manage_books/note.html.jinja', {'note_id': note_id})
