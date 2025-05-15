from django.test import TestCase
from books.models import Book, Review
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group


# Create your tests here.
class BookTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="reviewuser",
            email="reviewuser@email.com",
            password="testpass123",
        )
        cls.test1_user = get_user_model().objects.create_user(
            username="test1",
            email="test1@test.com",
            password="Test12344321",
        )
        cls.test2_user = get_user_model().objects.create_user(
            username="test2",
            email="test2@test.com",
            password="Test12344321",
        )
        cls.vip_group = Group.objects.create(name='VIP')
        cls.special_permission = Permission.objects.get(
            codename="special_status"
        )
        cls.book = Book.objects.create(
            title="Harry Potter",
            author="JK Rowling",
            price="25.00"
        )
        cls.review = Review.objects.create(
            book=cls.book,
            author=cls.user,
            review='An excellent review'
        )

    def test_book_content(self):
        self.assertEqual(f"{self.book.title}", "Harry Potter")
        self.assertEqual(f"{self.book.author}", "JK Rowling")
        self.assertEqual(f"{self.book.price}", "25.00")

    def test_book_list_view_for_logged_in_user(self):
        self.client.login(email="test2@test.com", password="Test12344321")
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter")
        self.assertTemplateUsed(response, "books/book_list.html")

    def test_book_list_view_for_logged_out_user(self):
        self.client.logout()

        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "%s?next=/books/" % (reverse("account_login")))  # noqa: E501

        response = self.client.get(reverse("book_list")+"?next=/books/", follow=True)  # noqa: E501
        self.assertContains(response, "Log In")

    def test_book_detail_view_with_permission(self):
        self.client.login(email="test1@test.com", password="Test12344321")
        self.test1_user.user_permissions.add(self.special_permission)
        self.test1_user.groups.add(self.vip_group)

        no_response = self.client.get("/books/1234567890/")
        self.assertEqual(no_response.status_code, 404)

        response = self.client.get(self.book.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter")
        self.assertContains(response, "An excellent review")
        self.assertTemplateUsed(response, "books/book_detail.html")

    # def test_book_detail_view_without_permission(self):
    #     self.client.login(email="test2@test.com", password="Test12344321")
    #     response = self.client.get(self.book.get_absolute_url())
    #     self.assertEqual(response.status_code, 403)
