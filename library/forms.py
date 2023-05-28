from library.models import Language, Place, Category, Author, Book
from djangouniversity import settings
from django import forms
from library.humanize import naturalsize
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
from django.core import validators
from django import forms


# Create the form class.
class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = '__all__'


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class AuthorForm(forms.ModelForm):
    birth = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    death = forms.DateField(required=False)

    class Meta:
        model = Author
        fields = '__all__'


class BookForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    picture = forms.FileField(required=False, label='File to Upload <= ' + max_upload_limit_text)
    upload_field_name = 'picture'

    # Hint: this will need to be changed for use in the library application :)
    class Meta:
        model = Book
        # fields = ['name', 'author', 'description', 'language', 'place', 'category', 'picture']
        fields = ['name', 'author', 'description', 'language', 'place', 'category', 'picture',
                  'tags']  # Picture is manual

    # Validate the size of the picture
    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('picture')
        if book is None:
            return
        if len(book) > self.max_upload_limit:
            self.add_error('picture', "File must be < " + self.max_upload_limit_text + " bytes")

        # Convert uploaded File object to a picture

    def save(self, commit=True):
        instance = super(BookForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.picture  # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()
            self.save_m2m()
        return instance
    # Convert uploaded File object to a picture


class CreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    picture = forms.FileField(required=False, label='File to Upload <= ' + max_upload_limit_text)
    upload_field_name = 'picture'

    # Hint: this will need to be changed for use in the ads application :)
    class Meta:
        model = Book

        fields = ['name', 'author', 'description', 'language', 'place', 'category', 'picture',
                  'tags']  # Picture is manual

    # Validate the size of the picture

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('picture')
        if book is None:
            return
        if len(book) > self.max_upload_limit:
            self.add_error('picture', "File must be < " + self.max_upload_limit_text + " bytes")

    # Convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(CreateForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.picture  # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()
            self.save_m2m()
        return instance


class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)


class BasicForm(forms.Form):
    name = forms.CharField(validators=[
        validators.MinLengthValidator(2, "Please enter 2 or more characters")])
    birth = forms.DateField()
    death = forms.DateField()

