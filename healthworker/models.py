from django.db import models
from django.conf import settings
from django.urls import reverse

from rest_framework.reverse import reverse as api_reverse #todo: update to django hosts

# Create your models here.

class HealthWorker(models.Model):

	EDUCATION_LEVEL = (
		('Degree','Degree'),
		('Diploma','Diploma'),
		('Certificate','Certificate'),
	)

	EMPLOYEE_TYPE = (
		('Permanent','Permanent'),
		('Contract','Contract')
	)

	TERMINATED=(
		('Yes','Yes'),
		('No','No'),
	)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, null=False, blank=False)

	education_level = models.CharField(max_length=100, null=True, choices=EDUCATION_LEVEL)
	employment_type = models.CharField(max_length=100, null=True, choices=EMPLOYEE_TYPE)

	date_of_hire = models.CharField(max_length=100, null=False, blank=False)
	deployment_facility = models.CharField(max_length=100, null=False, blank=False)

	end_of_contract = models.CharField(max_length=100, null=True, blank=True)

	terminated_employee = models.CharField(max_length=100,null=True, choices= TERMINATED)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.user.username)

	@property
	def owner(self):
		return self.user

	def get_api_url(self, request = None):
		return api_reverse("api-healthworker:post-rud", kwargs={'pk': self.pk}, request = request)

# todo: create dropdown fields for the health worker class
# todo: create a list of types of employment
