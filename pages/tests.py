from django.test import SimpleTestCase
from django.urls import reverse, resolve
from pages.views import HomePageView

# Create your tests here.


class HomePageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("home")
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_correct(self):
        self.assertTemplateUsed(self.response, "home.html")

    def test_contains_correct_content(self):
        self.assertContains(self.response, "our homepage")

    def test_not_contains_incorrect_content(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")  # noqa: E501

    def test_homepage_url_resolves_homepageview(self):
        view = resolve("/")
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)  # noqa: E501
