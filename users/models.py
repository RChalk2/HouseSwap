from django.db import models

class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    MobileNumber = models.CharField(max_length=15, unique=True)
    Rabbi = models.CharField(max_length=100)
    Kashrut = models.CharField(max_length=200)
    email = models.EmailField(max_length=255, unique=True)
    UserRating = models.FloatField(null=True, blank=True)


    
    def __str__(self):
        return self.MobileNumber
