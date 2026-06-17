from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Author, Book, Category, Genre, Note, Publisher, Series, Topic


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class BookForm(forms.ModelForm):
    new_publisher_name = forms.CharField(
        max_length=200, required=False,
        label='Nowy wydawca (jeśli nie ma na liście)',
    )
    new_author_names = forms.CharField(
        required=False,
        label='Nowi autorzy (imię i nazwisko, oddzielone przecinkami)',
        widget=forms.TextInput(attrs={'placeholder': 'np. Jan Kowalski, Anna Nowak'}),
    )

    class Meta:
        model = Book
        fields = [
            'title', 'isbn', 'publication_date', 'pages', 'cover', 'language',
            'publisher', 'series', 'category', 'authors', 'genres', 'topics',
        ]
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'authors': forms.CheckboxSelectMultiple,
            'genres': forms.CheckboxSelectMultiple,
            'topics': forms.CheckboxSelectMultiple,
        }

    def save(self, commit=True, owner=None):
        new_publisher_name = self.cleaned_data.pop('new_publisher_name', '').strip()
        new_author_names = self.cleaned_data.pop('new_author_names', '').strip()

        if new_publisher_name and not self.cleaned_data.get('publisher'):
            publisher = Publisher.objects.create(
                name=new_publisher_name, country='PL', founded_year=2000,
            )
            self.instance.publisher = publisher

        book = super().save(commit=False)
        if owner:
            book.owner = owner
        if commit:
            book.save()
            self.save_m2m()

        if new_author_names:
            for name in new_author_names.split(','):
                parts = name.strip().split()
                if len(parts) >= 2:
                    author, _ = Author.objects.get_or_create(
                        first_name=parts[0],
                        last_name=' '.join(parts[1:]),
                        defaults={'nationality': 'Nieznana'},
                    )
                    book.authors.add(author)

        return book


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Treść notatki...'}),
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'alias', 'nationality', 'title']


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'country', 'founded_year', 'website', 'email']


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ['name', 'description', 'authors']
        widgets = {'authors': forms.CheckboxSelectMultiple}


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
