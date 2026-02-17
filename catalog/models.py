from django.urls import reverse
import uuid  # Required for unique book instances
from django.db import models
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

# 这部分是教程测试时使用的
# class MyModelName(models.Model):
#     # Fields
#     my_field_name = models.CharField(max_length=20, help_text="Enter field name")
#
#     # Metadata
#
#     class Meta:
#         ordering=['-my_field_name']   # 如果没有按order_by()检索那么，默认按my_field_name倒叙为顺序输出
#
#
#     # Methods
#     def __str__(self):
#         return self.my_field_name


class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre(e.g. Science Fiction, French Poetry etc.)")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name='genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists (case insensitive match)"
            )
        ]

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

    def get_absolute_url(self):
        return reverse("genre-detail", args=[self.id])


class Language(models.Model):
    """
    Model representing a book language.
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)",
    )

    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message="Language already exists (case insensitive match)"
            )
        ]




class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)   # 当外键指向的author对象被删除时，引用它的记录字段（这里是ForeignKey）会被自动设为NULL

    summary = models.TextField(blank=True, null=True, max_length=1000,
                               help_text="Enter a brief description of the book")
    isbn = models.CharField("ISBN", max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('book-detail', args=[str(self.id)])  # 根据路由名字book-detail反向生成URL + args

    def display_genre(self):     # 用于显示genre（多对多情况下）正常不能显示在Book管理界面下的情况
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])      # self.genre.all()[:3]找到对应实例的genre，然后拼接成字符串就可以使用了

    display_genre.short_description = 'Genre'    # 定义该方法的域字段名（列表头名）


    # def display_Language(self):
    #     return str(self.)
    # display_Language.short_description = 'Language'

class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")

    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),    # 数据库存 'm'，界面显示 Maintenance
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              default='m', blank=True, help_text="Book availability")

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)     # 给表bookinstance添加一个权限，除了增删改查还可以 can_mark_returned（但显示选项是"Set book as returned"），没有实际作用也就是可以做身份识别，可能后续基于此身份识别可以做相应的功能

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return '%s (%s)' % (self.id, self.book.title)





class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null = True, blank=True)
    date_of_death = models.DateField(null = True, blank=True)


    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])


    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' %(self.last_name, self.first_name)







