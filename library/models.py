from django.core.validators import MinLengthValidator
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager


class Author(models.Model):
    name = models.CharField(max_length=200)
    birth = models.DateTimeField()
    death = models.DateTimeField(null=True, blank=True)

    # books = models.ManyToManyField('Books', through='Authored')

    def __str__(self):
        return self.name


class Authored(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language


class Place(models.Model):
    section = models.CharField(max_length=100)
    shelf = models.CharField(max_length=50)

    def __str__(self):
        return self.section


class Book(models.Model):
    name = models.CharField(max_length=200,
                            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")])
    publish_day = models.DateTimeField(auto_now_add=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    # author = models.ManyToManyField('Author', through='Authored')
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    description = models.TextField()
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    place = models.ForeignKey('Place', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    picture = models.BinaryField(null=True, editable=True)
    # picture = models.BinaryField(null=True, blank=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='book_owner')
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       through='Fav', related_name='favorite_books')
    tags = TaggableManager()
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      through='Comment', related_name='book_comments')


    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15: return self.text
        return self.text[:11] + ' ...'


# for choosing favorite book
class Fav(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='favs_users')

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return '%s likes %s' % (self.user.username, self.book.name[:10])


# chat in library
class Message(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
