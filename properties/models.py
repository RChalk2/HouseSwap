from django.db import models

from users.models import User

class Property(models.Model):
    PropertyID = models.AutoField(primary_key=True)
    City = models.CharField(max_length=100)
    Country = models.CharField(max_length=100)
    Postcode = models.CharField(max_length=20)
    Address = models.TextField()
    NoOfRooms = models.PositiveIntegerField()
    EstimatedValue = models.FloatField()
    PropertyType = models.CharField(max_length=100)
    Amenities = models.TextField()
    PetFriendly = models.BooleanField()
    AccessibilityFeatures = models.TextField()
    ProximityToPublicTransport = models.TextField()
    NearbyAttractions = models.TextField()
    Suckah = models.BooleanField()
    PassoverKitchen = models.BooleanField()
    MaxOccupancy = models.PositiveIntegerField()
    SmokingAllowed = models.BooleanField()
    PicturesOfProperty = models.ImageField(upload_to='properties/')
    HomeDescription = models.TextField()
    PropertyRating = models.FloatField(null=True, blank=True)

    
    # Assuming each property is tied to a user
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.Address
