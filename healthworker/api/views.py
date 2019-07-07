#generic views
from rest_framework import generics, mixins
from healthworker.models import HealthWorker
from .serializers import HealthWorkerSerializer
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q


class HealthWorkerAPIView(mixins.CreateModelMixin, generics.ListAPIView):
	lookup_field = 'pk' # url(r'?P<pk>\d+')
	serializer_class = HealthWorkerSerializer

	def get_queryset(self):
		qs = HealthWorker.objects.all()
		query = self.request.GET.get("q")

		if query is not None:
			qs = qs.filter(Q(name__icontains= query)|Q(timestamp__icontains = query)).distinct()
		return qs

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def get_serializer_context(self, *args, **kwargs):
		return {"request":self.request}


class HealthWorkerRUDView(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = 'pk' # url(r'?P<pk>\d+')
	serializer_class = HealthWorkerSerializer
	permission_classes = [IsOwnerOrReadOnly]

	def get_serializer_context(self, *args, **kwargs):
		return {"request":self.request}

	def get_queryset(self):
		return HealthWorker.objects.all()

	#def get_object(self):
	#	pk = self.kwargs.get("pk")
	#	return HealthWorker.objects.all()

