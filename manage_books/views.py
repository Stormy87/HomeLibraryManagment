from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (
    AuthorForm, BookForm, CategoryForm, GenreForm, NoteForm,
    PublisherForm, RegisterForm, SeriesForm, TopicForm,
)
from .models import Author, Book, Category, Genre, Note, Publisher, Series, Topic


def _user_books(request):
    if request.user.is_authenticated:
        return Book.objects.filter(Q(owner=request.user) | Q(owner__isnull=True))
    return Book.objects.all()


def _user_owns_book(user, book):
    return book.owner is None or book.owner == user


def _claim_book(book, user):
    if book.owner is None:
        book.owner = user
        book.save(update_fields=['owner'])


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Konto zostało utworzone. Witaj w bibliotece!')
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'manage_books/register.html.jinja', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    from django.contrib.auth.forms import AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Zalogowano pomyślnie.')
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'manage_books/login.html.jinja', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Wylogowano.')
    return redirect('index')


def index(request):
    all_books = _user_books(request)
    books = all_books
    genres = Genre.objects.all()
    topics = Topic.objects.all()

    genre_id = request.GET.get('genre')
    genre_name = None
    if genre_id:
        books = books.filter(genres__id=genre_id)
        genre_obj = Genre.objects.filter(id=genre_id).first()
        if genre_obj:
            genre_name = genre_obj.name

    topic_id = request.GET.get('topic')
    topic_name = None
    if topic_id:
        books = books.filter(topics__id=topic_id)
        topic_obj = Topic.objects.filter(id=topic_id).first()
        if topic_obj:
            topic_name = topic_obj.name

    return render(request, 'manage_books/index.html.jinja', {
        'genres': genres,
        'topics': topics,
        'books': books.distinct(),
        'favorite_books': all_books.filter(is_favorite=True),
        'read_books': all_books.filter(is_read=True),
        'genre_id': genre_id,
        'genre_name': genre_name,
        'topic_id': topic_id,
        'topic_name': topic_name,
    })


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    notes = book.notes.all().order_by('-created_at')
    return render(request, 'manage_books/book.html.jinja', {'book': book, 'notes': notes})


@login_required
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(owner=request.user)
            messages.success(request, f'Książka „{book.title}” została dodana.')
            return redirect('book', book_id=book.id)
    else:
        form = BookForm()
    return render(request, 'manage_books/book_form.html.jinja', {
        'form': form, 'title': 'Dodaj nową książkę',
    })


@login_required
def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if not _user_owns_book(request.user, book):
        messages.error(request, 'Nie masz uprawnień do edycji tej książki.')
        return redirect('book', book_id=book.id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(owner=request.user)
            _claim_book(book, request.user)
            messages.success(request, 'Dane książki zostały zaktualizowane.')
            return redirect('book', book_id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, 'manage_books/book_form.html.jinja', {
        'form': form, 'title': 'Edytuj książkę', 'book': book,
    })


@login_required
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if not _user_owns_book(request.user, book):
        messages.error(request, 'Nie masz uprawnień do usunięcia tej książki.')
        return redirect('book', book_id=book.id)
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Książka „{title}” została usunięta.')
        return redirect('index')
    return render(request, 'manage_books/confirm_delete.html.jinja', {
        'object': book, 'object_name': 'książkę', 'cancel_url': 'book',
        'cancel_id': book.id,
    })


@login_required
@require_POST
def book_toggle_read(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if not _user_owns_book(request.user, book):
        return redirect('book', book_id=book.id)
    _claim_book(book, request.user)
    book.is_read = not book.is_read
    book.save()
    return redirect('book', book_id=book.id)


@login_required
@require_POST
def book_toggle_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if not _user_owns_book(request.user, book):
        return redirect('book', book_id=book.id)
    _claim_book(book, request.user)
    book.is_favorite = not book.is_favorite
    book.save()
    return redirect('book', book_id=book.id)


@login_required
def note_add(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if not _user_owns_book(request.user, book):
        messages.error(request, 'Nie masz uprawnień do dodawania notatek do tej książki.')
        return redirect('book', book_id=book.id)
    _claim_book(book, request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.book = book
            note.save()
            messages.success(request, 'Notatka została dodana.')
            return redirect('book', book_id=book.id)
    else:
        form = NoteForm()
    return render(request, 'manage_books/note_form.html.jinja', {
        'form': form, 'book': book,
    })


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = _user_books(request).filter(authors=author)
    return render(request, 'manage_books/author.html.jinja', {
        'author': author, 'books': books,
    })


@login_required
def author_edit(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dane autora zostały zaktualizowane.')
            return redirect('author', author_id=author.id)
    else:
        form = AuthorForm(instance=author)
    return render(request, 'manage_books/dictionary_form.html.jinja', {
        'form': form, 'title': 'Edytuj autora', 'back_url': 'author',
        'back_id': author.id,
    })


@login_required
def publisher_detail(request, publisher_id):
    publisher = get_object_or_404(Publisher, id=publisher_id)
    books = _user_books(request).filter(publisher=publisher)
    return render(request, 'manage_books/publisher.html.jinja', {
        'publisher': publisher, 'books': books,
    })


@login_required
def publisher_edit(request, publisher_id):
    publisher = get_object_or_404(Publisher, id=publisher_id)
    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dane wydawcy zostały zaktualizowane.')
            return redirect('publisher', publisher_id=publisher.id)
    else:
        form = PublisherForm(instance=publisher)
    return render(request, 'manage_books/dictionary_form.html.jinja', {
        'form': form, 'title': 'Edytuj wydawcę', 'back_url': 'publisher',
        'back_id': publisher.id,
    })


@login_required
def series_detail(request, series_id):
    series_obj = get_object_or_404(Series, id=series_id)
    books = _user_books(request).filter(series=series_obj).order_by('publication_date')
    books_count = books.count()
    return render(request, 'manage_books/series.html.jinja', {
        'series': series_obj, 'books': books, 'books_count': books_count,
    })


def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'manage_books/note.html.jinja', {'note': note})


# --- Dictionary CRUD ---

DICTIONARY_CONFIG = {
    'authors': (Author, AuthorForm, 'Autorzy', 'autora'),
    'publishers': (Publisher, PublisherForm, 'Wydawcy', 'wydawcę'),
    'series': (Series, SeriesForm, 'Serie', 'serię'),
    'genres': (Genre, GenreForm, 'Gatunki', 'gatunek'),
    'topics': (Topic, TopicForm, 'Tematy', 'temat'),
    'categories': (Category, CategoryForm, 'Działy', 'dział'),
}


@login_required
def dictionaries_index(request):
    return render(request, 'manage_books/dictionaries.html.jinja', {
        'dictionaries': [
            ('authors', 'Autorzy'),
            ('publishers', 'Wydawcy'),
            ('series', 'Serie'),
            ('genres', 'Gatunki'),
            ('topics', 'Tematy'),
            ('categories', 'Działy'),
        ],
    })


@login_required
def dictionary_list(request, dict_type):
    model, _, label, _ = DICTIONARY_CONFIG[dict_type]
    if dict_type == 'authors':
        items = model.objects.all().order_by('last_name', 'first_name')
    else:
        items = model.objects.all().order_by('name')
    return render(request, 'manage_books/dictionary_list.html.jinja', {
        'items': items, 'dict_type': dict_type, 'label': label,
    })


@login_required
def dictionary_add(request, dict_type):
    model, form_class, label, _ = DICTIONARY_CONFIG[dict_type]
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Pozycja została dodana.')
            return redirect('dictionary_list', dict_type=dict_type)
    else:
        form = form_class()
    return render(request, 'manage_books/dictionary_form.html.jinja', {
        'form': form, 'title': f'Dodaj — {label}', 'back_url': 'dictionary_list',
        'dict_type': dict_type,
    })


@login_required
def dictionary_edit(request, dict_type, item_id):
    model, form_class, label, _ = DICTIONARY_CONFIG[dict_type]
    item = get_object_or_404(model, id=item_id)
    if request.method == 'POST':
        form = form_class(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pozycja została zaktualizowana.')
            return redirect('dictionary_list', dict_type=dict_type)
    else:
        form = form_class(instance=item)
    return render(request, 'manage_books/dictionary_form.html.jinja', {
        'form': form, 'title': f'Edytuj — {label}', 'back_url': 'dictionary_list',
        'dict_type': dict_type,
    })


@login_required
def dictionary_delete(request, dict_type, item_id):
    model, _, label, object_name = DICTIONARY_CONFIG[dict_type]
    item = get_object_or_404(model, id=item_id)
    if request.method == 'POST':
        item.delete()
        messages.success(request, f'Pozycja została usunięta.')
        return redirect('dictionary_list', dict_type=dict_type)
    return render(request, 'manage_books/confirm_delete.html.jinja', {
        'object': item, 'object_name': object_name,
        'cancel_url': 'dictionary_list', 'dict_type': dict_type,
    })
