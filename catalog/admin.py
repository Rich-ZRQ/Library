from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register your models in admin website.
#  admin.site.register(Author)
# 更改admin界面显示 Author

class BookInline(admin.TabularInline):
    model = Book
    extra = 0

# Define the author admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        'last_name',
        'first_name',
        'date_of_birth',
        'date_of_death'
    ]

    '''
    fields 指的是model里的 “列”
    在fields 属性列表只是要显示在表格上那些领域，如此才能。字段默认情况下垂直显示，
    但如果你进一步将它们分组在元组中（如上述“日期”字段中所示），则会水平显示。
    '''
    fields = ('last_name', 'first_name', ('date_of_birth',
        'date_of_death'))

    inlines = [BookInline] # 关联记录的内联编辑: 每个作者对应的所有书籍

admin.site.register(Author, AuthorAdmin)     # author admin class(定义Author model的显示方式) 和 Author model 一起注册到admin界面

admin.site.register(Genre)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


# admin.site.register(Book)
# Define the author admin class
@admin.register(Book)                 # Book admin class(定义Book model的显示方式) 和 Book model 一起注册到admin界面
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author',
        'display_genre',
        'language',
    ]
    inlines = [BooksInstanceInline]    # 关联记录的内联编辑：每本书对应的对应的书本实例


# admin.site.register(BookInstance)
@admin.register(BookInstance)         # BookInstance admin class(定义BookInstance model的显示方式) 和 BookInstance model 一起注册到admin界面
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'book',
        'imprint',
        'borrower',
        'due_back',
        'status',
    ]

    fieldsets = [
        (None,{
            'fields':('book', 'imprint', 'id')
        }),
        ('Availability',{
            'fields':('status', 'due_back', 'borrower')
        }),
    ]

    list_filter = [
        'status',
        'due_back'
    ]

admin.site.register(Language)


