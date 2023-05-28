from typing import Dict

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
import html
from .models import Book, Author, Category, Place, Language, Comment, Fav, Message
from .forms import BookForm, CommentForm, BasicForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q, QuerySet
from .forms import CreateForm
from django.views import generic
# csrf exemption in class based views

# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from .models import Message
from datetime import datetime, timedelta
import time
from rest_framework import viewsets
from .serializers import BookSerializer, AuthorSerializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class MainView(View):
    template_name = 'library/book_list.html'

    def get(self, request):

        strval = request.GET.get("search", False)
        if strval:
            query = Q(name__icontains=strval)
            query.add(Q(description__icontains=strval), Q.OR)
            book_list = Book.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else:
            book_list = Book.objects.all().order_by('-updated_at')[:10]

        # Augment the post_list
        for obj in book_list:
            obj.natural_updated = naturaltime(obj.updated_at)
        # print(connection.queries)
        lb = Book.objects.all()
        la = Author.objects.count()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_books.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [row['id'] for row in rows]
        ctx = {'book_list': book_list, 'search': strval, 'author_count': la, 'favorites': favorites}
        return render(request, self.template_name, ctx)
        # print(connection.queries)


class BookListView(View):
    def get(self, request):
        stuff = Book.objects.all()
        cntx = {'book_list': stuff}
        return render(request, 'library/books_list.html', cntx)


class BookCreateView(OwnerCreateView):
    model = Book

    fields = ['name', 'author', 'description', 'language', 'place', 'category', 'category', 'tags']
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('library:all')

    def get(self, request, pk=None):
        form = BookForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = BookForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

            # Add owner to the model before saving
        book = form.save(commit=False)
        book.owner = self.request.user
        book.save()
        # form.save_m2m()    # Add this
        return redirect(self.success_url)


class BookUpdateView(OwnerUpdateView):
    template_name = 'library/book_form.html'
    model = Book
    # fields = '__all__'
    success_url = reverse_lazy('library:all')

    def get(self, request, pk):
        book = get_object_or_404(Book, id=pk)
        form = BookForm(instance=book)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        book = get_object_or_404(Book, id=pk)
        # , owner=self.request.user)
        form = BookForm(request.POST, request.FILES or None, instance=book)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        book = form.save(commit=False)
        book.save()
        # form.save_m2m()    # Add this

        return redirect(self.success_url)


class BookDeleteView(DeleteView):
    model = Book
    fields = fields = '__all__'
    success_url = reverse_lazy('library:all')


class BookDetailView(OwnerDetailView):
    model = Book
    template_name = "library/book_detail.html"

    def get(self, request, pk):
        x = Book.objects.get(id=pk)
        comments = Comment.objects.filter(book=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = {'book': x, 'comments': comments, 'comment_form': comment_form}

        return render(request, self.template_name, context)


class LanguageView(View):
    def get(self, request):
        ml = Language.objects.all()
        ctx = {'language_list': ml}
        return render(request, 'library/language_list.html', ctx)


class LanguageCreateView(CreateView):
    model = Language
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class LanguageUpdateView(UpdateView):
    model = Language
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class LanguageDeleteView(DeleteView):
    model = Language
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class PlaceView(View):
    def get(self, request):
        pl = Place.objects.all()
        ctx = {'place_list': pl}
        return render(request, 'library/place_list.html', ctx)


class PlaceCreateView(CreateView):
    model = Place
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class PlaceUpdateView(UpdateView):
    model = Place
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class PlaceDeleteView(DeleteView):
    model = Place
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class CategoryView(View):
    def get(self, request):
        cl = Category.objects.all()
        ctx = {'category_list': cl}
        return render(request, 'library/category_list.html', ctx)


class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class CategoryUpdateView(UpdateView):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class CategoryDeleteView(DeleteView):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class AuthorView(View):
    def get(self, request):
        al = Author.objects.all()
        ctx = {'author_list': al}
        return render(request, 'library/author_list.html', ctx)


class AuthorlistView(View):
    model = Author

    def get(self, request):
        modelname = self.model._meta.verbose_name.title().lower()
        stuff = self.model.objects.all()
        cntx = {modelname + '_list': stuff}
        # return render(request, 'library/' + modelname + '_list.html', cntx)
        return render(request, 'library/authors_list.html', cntx)


class AuthorCreateView(CreateView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('library:all')


# Call as dumpdata('GET', request.GET)
def dumpdata(place, data):
    retval = ""
    if len(data) > 0:
        retval += '<p>Incoming ' + place + ' data:<br/>\n'
        for key, value in data.items():
            retval += html.escape(key) + '=' + html.escape(value) + '</br>\n'
        retval += '</p>\n'
    return retval


class DumpPostView(View):  # Reusable bit...
    def post(self, request):
        dump = dumpdata('POST', request.POST)
        ctx = {'title': 'request.POST', 'dump': dump}
        return render(request, 'library/dump.html', ctx)


class AuthorUpdateView(DumpPostView):
    #def get(self, request):
        #old_data = {
           # 'name': 'SakaiCar',
          #  'birth': '2000-08-14',
         #   'death': '2023-01-01'
        #}
        #form = BasicForm(old_data)
      #  ctx = {'form': form}
       # return render(request, 'library/author_form.html', ctx)
     model = Author
     fields = '__all__'
     success_url = reverse_lazy('library:all')


class AuthorDeleteView(DeleteView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('library:all')


class BookDetailView(DetailView):
    model = Book
    template_name = "library/book_detail.html"


def stream_file(request, pk):
    book = get_object_or_404(Book, id=pk)
    response = HttpResponse()
    response['Content-Type'] = book.content_type
    response['Content-Length'] = len(book.picture)
    response.write(book.picture)
    return response


@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print("Add PK", pk)
        t = get_object_or_404(Book, id=pk)
        fav = Fav(user=request.user, book=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print("Delete PK", pk)
        t = get_object_or_404(Book, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, book=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()


# chat time
def jsonfun(request):
    time.sleep(2)
    stuff = {
        'first': 'first thing',
        'second': 'second thing'
    }
    return JsonResponse(stuff)


class TalkMain(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'library/talk.html')

    def post(self, request):
        message = Message(text=request.POST['message'], owner=request.user)
        message.save()
        return redirect(reverse('library:talk'))


class TalkMessages(LoginRequiredMixin, View):
    def get(self, request):
        messages = Message.objects.all().order_by('-created_at')[:10]
        results = []
        for message in messages:
            result = [message.text, naturaltime(message.created_at)]
            results.append(result)
        return JsonResponse(results, safe=False)


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        f = get_object_or_404(Book, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, book=f)
        comment.save()
        return redirect(reverse('library:book_detail', args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "library/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        book = self.object.book
        return reverse('library:book_detail', args=[book.id])


# Lets explore how (badly) we can override some of what goes on...
class WackyEquinesView(generic.ListView):
    model = Book
    template_name = 'library/wacky.html'  # Convention: library/book_list.html

    def get_queryset(self, **kwargs):
        crazy = Author.objects.all()  # Convention: Author
        print('CRAZY')
        return crazy

    # Add something to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crazy_thing'] = 'CRAZY THING'
        return context


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows breeds to be viewed or edited.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthoriewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cats to be viewed or edited.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class FirstView(View):
    def get(self, request):
        return render(request, 'library/route.html')


class SecondView(View):
    def get(self, request):
        u = reverse('library:authors')
        u2 = reverse('library:books')
        u3 = reverse('library:books')
        ctx = {'x1': u, 'x2': u2, 'x3': u3}
        return render(request, 'library/second.html', ctx)


def cookie(request):
    print(request.COOKIES)
    oldval = request.COOKIES.get('zap', None)
    resp = HttpResponse('In a view - the zap cookie value is ' + str(oldval))
    if oldval:
        resp.set_cookie('zap', int(oldval) + 1)  # No expired date = until browser close
    else:
        resp.set_cookie('zap', 42)  # No expired date = until browser close
    resp.set_cookie('sakaicar', 42, max_age=1000)  # seconds until expire
    return resp


# https://www.youtube.com/watch?v=Ye8mB6VsUHw

def sessfun(request):
    num_visits = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = num_visits
    if num_visits > 4: del (request.session['num_visits'])
    resp = HttpResponse('view count=' + str(num_visits))
    return resp
