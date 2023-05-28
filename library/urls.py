from django.urls import path, re_path, reverse_lazy, include
from django.views.static import serve
from . import views
from django.views.generic import TemplateView
import os
from rest_framework import routers


app_name = 'library'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthoriewSet)

urlpatterns = [

    path('', views.MainView.as_view(), name='all'),
    # path('book/<int:pk>', views.BookCreateView.as_view(), name='ad_detail'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('book/create', views.BookCreateView.as_view(), name='book_create'),
    path('book/<int:pk>/update', views.BookUpdateView.as_view(), name='book_update'),
    path('book/<int:pk>/delete', views.BookDeleteView.as_view(), name='book_delete'),
    path('book/<int:pk>/favorite', views.AddFavoriteView.as_view(), name='book_favorite'),
    path('book/<int:pk>/unfavorite', views.DeleteFavoriteView.as_view(), name='book_unfavorite'),
    path('book_picture/<int:pk>', views.stream_file, name='book_picture'),
    path('language/', views.LanguageView.as_view(), name='language_list'),
    path('language/create/', views.LanguageCreateView.as_view(), name='language_create'),
    path('language/<int:pk>/update', views.LanguageUpdateView.as_view(), name='language_Update'),
    path('language/<int:pk>/delete', views.LanguageDeleteView.as_view(), name='language_Delete'),
    path('place/', views.PlaceView.as_view(), name='place_list'),
    path('place/create/', views.PlaceCreateView.as_view(), name='place_create'),
    path('place/<int:pk>/update', views.PlaceUpdateView.as_view(), name='place_Update'),
    path('place/<int:pk>/delete', views.PlaceDeleteView.as_view(), name='place_Delete'),
    path('category/', views.CategoryView.as_view(), name='category_list'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/update', views.CategoryUpdateView.as_view(), name='category_Update'),
    path('category/<int:pk>/delete', views.CategoryDeleteView.as_view(), name='category_Delete'),
    path('author/', views.AuthorView.as_view(), name='author_list'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author_create'),
    path('author/<int:pk>/update', views.AuthorUpdateView.as_view(), name='author_Update'),
    path('author/<int:pk>/delete', views.AuthorDeleteView.as_view(), name='author_Delete'),

    path('syntax', TemplateView.as_view(template_name='library/syntax.html'),
         name='syntax'),
    path('jsonfun', views.jsonfun, name='jsonfun'),

    path('talk', views.TalkMain.as_view(), name='talk'),
    path('messages', views.TalkMessages.as_view(), name='messages'),

    # Serve up a local static folder to serve spinner.gif
    re_path(r'^static/(?P<path>.*)$', serve,
            {'document_root': os.path.join(BASE_DIR, 'static'), 'show_indexes': True},
            name='static'
            ),

    path('book/<int:pk>/comment',
         views.CommentCreateView.as_view(), name='book_comment_create'),
    path('comment/<int:pk>/delete',
         views.CommentDeleteView.as_view(success_url=reverse_lazy('library:all')), name='book_comment_delete'),
    path('books', views.BookListView.as_view(), name='books'),
    path('authors', views.AuthorlistView.as_view(), name='authors'),
    path('wacky', views.WackyEquinesView.as_view(), name='whatever'),
    path('grid', TemplateView.as_view(template_name='library/grid_main.html')),

    path('rest', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('route', TemplateView.as_view(template_name='library/route.html')),
    path('first', views.FirstView.as_view(), name='first-view'),
    path('second', views.SecondView.as_view(), name='second-view'),
    path('cookie', views.cookie),
    path('sessfun', views.sessfun),
    path('cookie_main', TemplateView.as_view(template_name='library/cookie.html')),
]
