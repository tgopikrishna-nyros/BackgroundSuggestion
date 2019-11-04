from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
def generate_background_id():
    return str(uuid.uuid4()).split("-")[-1] #generate unique ticket id

class Picture(models.Model):
	img_name = models.CharField(max_length=50, null=True, blank=True)
	upload_img = models.ImageField(upload_to='images/')
	occupied_color = models.CharField(max_length=50, null=True, blank=True)
	opposite = models.CharField(max_length=50, null=True, blank=True)
	complementary = models.CharField(max_length=50, null=True, blank=True)

	def __str__(self):
		return self.img_name

