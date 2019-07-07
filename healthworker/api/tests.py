from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from healthworker.models import HealthWorker
from rest_framework import status
from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

from rest_framework.reverse import reverse as api_reverse

User = get_user_model()


class HealthWorkerPostAPITestCase(APITestCase):
	def setUp(self):
		user_obj = User(username='testuser', email='test@test.com')
		user_obj.set_password("123456")
		user_obj.save()
		healthworker_post = HealthWorker.objects.create(user=user_obj, name = '', date_of_hire = '', deployment_facility = '', end_of_contract ='')

	def test_single_user(self):
		user_count = User.objects.count()
		self.assertEqual(user_count, 1)

	def test_single_post(self):
		post_count = HealthWorker.objects.count()
		self.assertEqual(post_count, 1)

	def test_get_list(self):
		data = {}
		url = api_reverse("api-healthworker:post-listcreate")
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		print(response.data)

	def test_post_item(self):
		data = {"title": "rand title", "content": "rand content"}
		url = api_reverse("api-healthworker:post-listcreate")
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		print(response.data)

	def test_get_item(self):
		_post = HealthWorker.objects.first()
		data = {}
		url = _post.get_api_url()
		response = self.client.get(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		print(response.data)

	def test_update_item(self):
		_post = HealthWorker.objects.first()
		data = {"title": "rand title", "content": "rand content"}
		url = _post.get_api_url()
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
		print(response.data)

		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		print(response.data)

	def test_update_item_with_user(self):
		_post = HealthWorker.objects.first()
		url = HealthWorker.get_api_url()
		data = {"title": "rand title", "content": "rand content"}
		user_obj = User.objects.first()
		payload = payload_handler(user_obj)
		token_rsp = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		print(response.data)

	def test_post_item_with_user(self):
		user_obj = User.objects.first()
		payload = payload_handler(user_obj)
		token_rsp = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
		data = {"title": "rand title", "content": "rand content"}
		url = api_reverse("api-postings:post-listcreate")
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		print(response.data)

	def test_user_ownership(self):
		owner = User.objects.create(username='testuser2')
		_post = HealthWorker.objects.create(user=owner, title='new title', content='random')
		user_obj = User.objects.first()
		self.assertNotEqual(user_obj.username, owner.username)

		url = _post.get_api_url()
		payload = payload_handler(user_obj)
		token_rsp = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
		data = {"title": "rand title", "content": "rand content"}
		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_user_login_and_update(self):
		data = {
			'username': 'testcfeuser',
			'password': '123456'
		}
		url = api_reverse("api-login")
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		token = response.data.get("token")
		if token is not None:
			_post = HealthWorker.objects.first()
			url = _post.get_api_url()
			data = {"title": "rand title", "content": "rand content"}
			self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
			response = self.client.put(url, data, format='json')
			self.assertEqual(response.status_code, status.HTTP_200_OK)
			print(response.data)
