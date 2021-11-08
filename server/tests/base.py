from http import HTTPStatus

from django.http import HttpResponse
from django.urls import reverse
from rest_framework.test import APITestCase


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
