from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from snippets.models import Snippet
from snippets.views import top

UserModel = get_user_model()


class TopPageRenderSnippetsTest(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="top_secret_pass0001",
        )
        self.snippet = Snippet.objects.create(
            title="title1",
            code='print("hello")',
            description="description1",
            created_by=self.user,
        )

    def test_should_return_snippet_title(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.snippet.title)

    def test_should_return_snippet_username(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.user.username)


class SnippetDetailTest(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="secret",
        )
        self.snippet = Snippet.objects.create(
            title="タイトル",
            code="コード",
            description="解説",
            created_by=self.user,
        )

    def test_should_use_expected_template(self):
        response = self.client.get(f"/snippets/{self.snippet.id}/")
        self.assertTemplateUsed(response, "snippets/snippet_detail.html")

    def test_top_page_returns_200_and_expected_heading(self):
        response = self.client.get(f"/snippets/{self.snippet.id}/")
        self.assertContains(response, self.snippet.title, status_code=200)
