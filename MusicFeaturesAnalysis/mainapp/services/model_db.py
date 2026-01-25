from django.db import transaction

class ModelData:
	def __init__(self, model):
		self.model = model
		
	@transaction.atomic
	def get_or_update(self, kwargs: dict, defaults: dict):
		obj, created = self.model.objects.update_or_create(
			**kwargs,
			defaults=defaults,
		)
		return obj, created
	
	@transaction.atomic
	def get_or_create(self, kwargs: dict, defaults: dict = None):
		if defaults is None:
			defaults = {}

		obj, created = self.model.objects.get_or_create(
			**kwargs,
			defaults=defaults
		)
		return obj, created

	def get(self, **kwargs):
		return self.model.objects.filter(**kwargs).first()

	def delete(self, **kwargs):
		return self.model.objects.filter(**kwargs).delete()

	def _get_all(self, filters=None, select_related=None, prefetch_related=None):
		qs = self.model.objects.all()
		if filters:
			qs = qs.filter(**filters)
		if select_related:
			qs = qs.select_related(*select_related)
		if prefetch_related:
			qs = qs.prefetch_related(*prefetch_related)
		return qs

	def get_all(self, filters=None, select_related=None, prefetch_related=None):
		return self._get_all(filters, select_related, prefetch_related)
