from http import HTTPStatus

from django.http import HttpResponse
from django.urls import reverse
from rest_framework.test import APITestCase

from blog.models import Post
from tests.factories import PostFactory


class BaseTestCase(APITestCase):
    base_name: str

    @classmethod
    def get_response_data(cls, response: HttpResponse) -> dict:
        return response.data  # type: ignore

    def detail_url(self, args: list[str | int] = None) -> str:
        return reverse(f'{self.base_name}-detail', args=args)

    def list_url(self, args: list[str | int] = None) -> str:
        return reverse(f'{self.base_name}-list', args=args)

    def create(self, attributes: dict, args: list[str | int] = None) -> dict:
        response = self.client.post(self.list_url(args), data=attributes)

        assert response.status_code == HTTPStatus.CREATED
        return self.get_response_data(response)

    def list_all(self, attributes: dict = None, args: list[str | int] = None) -> dict:
        response = self.client.get(self.list_url(args), data=attributes)

        assert response.status_code == HTTPStatus.OK
        return self.get_response_data(response)

    def retrieve(self, args: list[str | int]) -> dict:
        response = self.client.get(self.detail_url(args))

        assert response.status_code == HTTPStatus.OK
        return self.get_response_data(response)

    def update(self, attributes: dict, args: list[str | int] = None) -> dict:
        response = self.client.put(self.detail_url(args), data=attributes)

        assert response.status_code == HTTPStatus.OK
        return self.get_response_data(response)

    def partial_update(self, attributes: dict, args: list[str | int] = None) -> dict:
        response = self.client.patch(self.detail_url(args), data=attributes)

        assert response.status_code == HTTPStatus.OK
        return self.get_response_data(response)

    def delete(self, args: list[str | int] = None) -> None:
        url = reverse('posts-detail', args=args)
        response = self.client.delete(url)

        assert response.status_code == HTTPStatus.NO_CONTENT


class TestPostViewSet(BaseTestCase):
    base_name = 'posts'

    def setUp(self) -> None:
        self.post_attributes = PostFactory.build()
        self.post = Post.objects.create(**self.post_attributes)
        self.expected_response = {'id': self.post.id, **self.post_attributes}

    def test_create(self) -> None:
        post_attributes = PostFactory.build()
        post = self.create(post_attributes)
        expected_response = {'id': post['id'], **post_attributes}

        assert post == expected_response
        assert Post.objects.filter(**expected_response).exists()

    def test_list(self) -> None:
        post_attributes = PostFactory.build()
        post = Post.objects.create(**post_attributes)
        posts = self.list_all()
        expected_response = [
            self.expected_response,
            {
                'id': post.id,
                **post_attributes,
            },
        ]
        assert posts == expected_response

    def test_retrieve(self) -> None:
        post = self.retrieve(args=[self.post.id])
        assert post == self.expected_response

    def test_put(self) -> None:
        updated_post_attributes = PostFactory.build()
        updated_post = self.update(updated_post_attributes, args=[self.post.id])
        expected_response = {**self.expected_response, **updated_post_attributes}

        assert updated_post == expected_response
        assert Post.objects.filter(**expected_response).exists()

    def test_patch(self) -> None:
        updated_post_attributes = {'title': 'New title'}
        updated_post = self.partial_update(updated_post_attributes, args=[self.post.id])
        expected_response: dict = {**self.expected_response, **updated_post_attributes}

        assert updated_post == expected_response
        assert Post.objects.filter(**expected_response).exists()

    def test_delete(self) -> None:
        post_attributes = PostFactory.build()
        post = Post.objects.create(**post_attributes)

        self.delete(args=[self.post.id])
        assert not Post.objects.filter(id=self.post.id).exists()

        posts = self.list_all()
        assert posts[0]['id'] == post.id
