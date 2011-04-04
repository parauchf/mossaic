from django.contrib.gis.db import models
from django.contrib.auth.models import User

class MossaicUser(User):
	class Meta:
		proxy = True

