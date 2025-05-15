from django.views.generic import ListView, DetailView
from .models import Book, Review
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin  # noqa: E501


# Create your views here.
class BookListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/book_list.html'
    login_url = 'account_login'


class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DetailView):  # noqa: E501
    model = Book
    context_object_name = 'book'
    template_name = 'books/book_detail.html'
    login_url = 'account_login'
    permission_required = 'books.special_status'

    # 仅允许VIP组的用户访问此视图
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.groups.filter(name='VIP').exists()
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()  # 获取当前书籍对象
        # 获取这本书的所有评论，按创建时间降序
        reviews = Review.objects.filter(book=book).order_by('-created_at')

        # 设置每页显示的评论数量
        reviews_per_page = 5  # 您可以根据需要调整这个值

        # 创建 Paginator 对象
        paginator = Paginator(reviews, reviews_per_page)

        # 从请求中获取当前页码 (e.g., ?page=2)
        page_number = self.request.GET.get('page')

        # 获取当前页的对象列表 (page_obj)
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj  # 将分页后的评论对象添加到上下文中
        return context
