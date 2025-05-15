from django.test import TestCase
from books.models import Book, Review
from django.urls import reverse
from django.contrib.auth import get_user_model


# Create your tests here.
class BookTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="reviewuser",
            email="reviewuser@email.com",
            password="testpass123",
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

    def test_book_list_view(self):
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter")
        self.assertTemplateUsed(response, "books/book_list.html")

    def test_book_detail_view(self):
        no_response = self.client.get("/books/1234567890/")
        self.assertEqual(no_response.status_code, 404)

        response = self.client.get(self.book.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter")
        self.assertContains(response, "An excellent review")
        self.assertTemplateUsed(response, "books/book_detail.html")
