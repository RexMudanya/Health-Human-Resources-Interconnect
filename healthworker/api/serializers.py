from  rest_framework import serializers
from healthworker.models import HealthWorker

class HealthWorkerSerializer(serializers.ModelSerializer):# converts to json, validates data passed

	url = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = HealthWorker
		fields = [
			'url',
			'pk',
			'user',
			'name',
			'education_level',
			'employment_type',
			'date_of_hire',
			'deployment_facility',
			'end_of_contract',
			'terminated_employee',
			'timestamp'
		]
		read_only_fields = ['pk','user']

	def get_url(self, obj):

		request = self.context.get("request")
		return obj.get_api_url(request = request)

	def validate_name(self, attrs):
		qs = HealthWorker.objects.filter(title__iexact = value)
		if self.instance:
			qs = qs.exclude(pk = self.instance.pk)
		if qs.exists():
			raise serializers.ValidationError("Name already exists")
		return value

