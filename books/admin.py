from django.contrib import admin

from books.models import Book, Review


class ReviewInline(admin.TabularInline):
    model = Review


class BookAdmin(admin.ModelAdmin):
    inlines = [
        ReviewInline,
    ]
    list_display = ('title', 'author', 'price')
    list_filter = ('author',)
    search_fields = ('title', 'author')
    ordering = ('title',)


# Register your models here.
admin.site.register(Book, BookAdmin)
