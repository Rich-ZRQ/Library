from catalog import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),     # name 参数用于反向解析 即：<a href="{% url 'books' %}">Books</a>   url 'books' ---> /catalog/books/指代这个

    path('books/', views.BookListView.as_view(), name='books'),   # 将一个基于类的视图BookListView， 转换为Django能调用的视图函数.as_view()
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),   # <int:pk>捕获book id，并令pk=book id传递给视图作为参数

    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.BorrowedBooksListView.as_view(), name='all_borrowed_books'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name = 'renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete', views.AuthorDelete.as_view(), name = 'author_delete'),
    path('book/create/', views.BookCreate.as_view(), name = 'book_create'),
    path('book/<int:pk>/update', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete', views.BookDelete.as_view(), name = 'book_delete'),

]



