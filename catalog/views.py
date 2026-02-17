from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings

from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import  RenewBookForm
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# Create your views here.


def index(request):
    """
    View function for home page of site.
    """

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()


    '''
    num_instances = BookInstance.objects.all().count() 效果上等于 num_instances = BookInstance.objects.count()
    '''

    num_instances_maintenance = BookInstance.objects.filter(status__exact='m').count()
    num_instances_on_loan = BookInstance.objects.filter(status__exact='o').count()
    num_instances_reserved = BookInstance.objects.filter(status__exact='r').count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    print("DB PATH:", settings.DATABASES["default"]["NAME"])

    return render(
        request,
        'index.html',
        context={
            'num_books':num_books,
            'num_instances':num_instances,
            'num_instances_available':num_instances_available,
            'num_instances_on_loan': num_instances_on_loan,
            'num_instances_reserved': num_instances_reserved,
            'num_instances_maintenance': num_instances_maintenance,
            'num_authors':num_authors,
            'num_visits': num_visits,
            'test': request.session['num_visits'],
        }
    )

@permission_required('catalog.can_mark_returned')   # 只有授权用户才可以访问它
def renew_book_librarian(request, pk):
    """
        View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all_borrowed_books'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })

    return render(
        request,
        'book_renew_librarian.html',
        {'form': form, 'bookinst': book_inst})

class BookListView(generic.ListView):    # 基于类的通用列表视图, 类似于模板
    model = Book
    queryset = Book.objects.all()

    context_object_name = "book_list"

    template_name = 'books_list.html'

    paginate_by = 2 # 只要超过10条记录，视图就会开始对它发送到模板的数据，进行分页， 可以使用 URL：/catalog/books/?page=2访问


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    queryset = BookInstance.objects.all()
    context_object_name = "bookinstance_list"
    template_name ='bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class BorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'borrowed_books_list.html'
    context_object_name = 'borrowed_books'

    # 限制用户必须拥有 can_mark_returned 权限才能访问
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        """返回所有借阅的书本，包含借用人的名字"""
        return BookInstance.objects.filter(status='o').select_related('borrower')

class BookDetailView(generic.DetailView):  # 基于类的通用详情信息视图，类似于模板
    model =Book
    template_name = 'book_detail.html'



class AuthorListView(generic.ListView):
    model = Author
    queryset = Author.objects.all()
    context_object_name = "author_list"
    template_name = 'author_list.html'

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'


class AuthorCreate(PermissionRequiredMixin, CreateView):   # 先get获得一个表单填写，然后再post原URL修改数据库内容并重定向到author detail页面
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = '__all__'
    initial={'date_of_death':'3000-05-01 ',}
    template_name = 'author_form.html'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    permission_required = 'catalog.can_mark_returned'
    template_name = 'author_form.html'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'
    template_name = 'author_confirm_delete.html'


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required='catalog.can_mark_returned'
    template_name = 'book_form.html'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['author', 'summary', 'isbn', 'genre', 'language']
    permission_required='catalog.can_mark_returned'
    template_name = 'book_form.html'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required='catalog.can_mark_returned'
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('books')