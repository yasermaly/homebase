from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class Amenity(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('amenities_detail', kwargs={'pk': self.id})


class Home(models.Model):
  address = models.CharField(max_length=100)
  price = models.CharField(max_length=100)
  beds = models.IntegerField()
  baths = models.IntegerField()
  sqft = models.CharField(max_length=100)
  description = models.TextField(max_length=1000)
  amenities = models.ManyToManyField(Amenity)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('detail', kwargs={'home_id': self.id})



class Photo(models.Model):
    url = models.CharField(max_length=200)
    home = models.ForeignKey(Home, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for home_id: {self.home_id} @{self.url}"
