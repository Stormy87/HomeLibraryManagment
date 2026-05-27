from django.shortcuts import HttpResponse, render
from manage_books.models import Genre, Author, Publisher, Series, Note, Book, Topic

def index(request):
  genres = Genre.objects.all()
  authors = Author.objects.all()
  publishers = Publisher.objects.all()
  series = Series.objects.all()
  notes = Note.objects.all()
  books = Book.objects.all()
  topics = Topic.objects.all()

  # Filter by genre
  genre_id = request.GET.get('genre')
  genre_name = None
  if genre_id:
    books = books.filter(genres__id=genre_id)
    try:
      genre_name = Genre.objects.get(id=genre_id).name
    except Genre.DoesNotExist:
      pass

  # Filter by topic
  topic_id = request.GET.get('topic')
  topic_name = None
  if topic_id:
    books = books.filter(topic__id=topic_id)
    try:
      topic_name = Topic.objects.get(id=topic_id).name
    except Topic.DoesNotExist:
      pass

  # Filter by author
  author_id = request.GET.get('author')
  author_name = None
  if author_id:
    books = books.filter(authors__id=author_id)
    try:
      author_obj = Author.objects.get(id=author_id)
      author_name = f"{author_obj.name} {author_obj.last_name}"
    except Author.DoesNotExist:
      pass

  # Filter by publisher
  publisher_id = request.GET.get('publisher')
  publisher_name = None
  if publisher_id:
    books = books.filter(publisher__id=publisher_id)
    try:
      publisher_name = Publisher.objects.get(id=publisher_id).name
    except Publisher.DoesNotExist:
      pass

  # Filter by series
  series_id = request.GET.get('series')
  series_name = None
  if series_id:
    books = books.filter(series__id=series_id)
    try:
      series_name = Series.objects.get(id=series_id).name
    except Series.DoesNotExist:
      pass

  # Filter by read status
  is_read = request.GET.get('is_read')
  if is_read == 'true':
    books = books.filter(is_read=True)
  elif is_read == 'false':
    books = books.filter(is_read=False)

  # Filter by favorite status
  is_favorite = request.GET.get('is_favorite')
  if is_favorite == 'true':
    books = books.filter(is_favorite=True)

  return render(request, 'manage_books/index.html.jinja', {
    'genres': genres,
    'authors': authors,
    'publishers': publishers,
    'series': series,
    'notes': notes,
    'books': books,
    'topics': topics,
    'favorite_books': books.filter(is_favorite=True),
    'read_books': books.filter(is_read=True),
    'genre_id': genre_id,
    'genre_name': genre_name,
    'topic_id': topic_id,
    'topic_name': topic_name,
    'author_id': author_id,
    'author_name': author_name,
    'publisher_id': publisher_id,
    'publisher_name': publisher_name,
    'series_id': series_id,
    'series_name': series_name,
    'is_read': is_read,
    'is_favorite': is_favorite,
  })

def book(request, book_id):
  book = Book.objects.get(id=book_id)
  notes = Note.objects.filter(book=book)
  return render(request, 'manage_books/book.html.jinja', {'book': book, 'notes': notes})

def author(request, author_id):
  author = Author.objects.get(id=author_id)
  books = author.books.all()
  return render(request, 'manage_books/author.html.jinja', {'author': author, 'books': books})

def publisher(request, publisher_id):
  publisher = Publisher.objects.get(id=publisher_id)
  books = Book.objects.filter(publisher=publisher)
  return render(request, 'manage_books/publisher.html.jinja', {'publisher': publisher, 'books': books})

def series(request, series_id):
  series_obj = Series.objects.get(id=series_id)
  books = Book.objects.filter(series=series_obj)
  return render(request, 'manage_books/series.html.jinja', {'series': series_obj, 'books': books})

def note(request, note_id):
  note = Note.objects.get(id=note_id)
  return render(request, 'manage_books/note.html.jinja', {'note': note})

def authors_list(request):
  authors = Author.objects.all().order_by('name', 'last_name')
  return render(request, 'manage_books/authors_list.html.jinja', {'authors': authors})

def publishers_list(request):
  publishers = Publisher.objects.all().order_by('name')
  return render(request, 'manage_books/publishers_list.html.jinja', {'publishers': publishers})

def series_list(request):
  series_objs = Series.objects.all().order_by('name')
  return render(request, 'manage_books/series_list.html.jinja', {'series': series_objs})

def notes_list(request):
  notes = Note.objects.all().order_by('-created_at')
  return render(request, 'manage_books/notes_list.html.jinja', {'notes': notes})