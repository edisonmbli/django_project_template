from django.views.generic import ListView, DetailView
from .models import Book, Review
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin  # noqa: E501
from django.db.models import Q, Prefetch


# Create your views here.
class BookListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/book_list.html'
    login_url = 'account_login'


class SearchResultListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )


class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DetailView):  # noqa: E501
    model = Book
    context_object_name = 'book'
    template_name = 'books/book_detail.html'
    login_url = 'account_login'
    permission_required = 'books.special_status'
    queryset = Book.objects.prefetch_related(
        Prefetch(
            'reviews',
            queryset=Review.objects.order_by('-created_at').select_related('author')  # noqa: E501
        )
    )

    # 仅允许VIP组的用户访问此视图
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.groups.filter(name='VIP').exists()
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 使用self.object, 它已经被内置的get_object()获取并应用了预抓取
        book_instance = self.object

        # book_instance.reviews.all() 现在会使用上面 Prefetch 对象定义的预抓取数据
        # 这些reviews已经按'-created_at'排序，并且每个review的author也被select_related加载了
        reviews = book_instance.reviews.all()

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
