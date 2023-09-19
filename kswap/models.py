# Models created:
# Kashrut
# User
# Property
#

from django.db import models

# Used to generate URLs by reversing the URL patterns
from django.urls import reverse

# uuid is a library that can generate random 128 bit objects for unqiue ids
import uuid

from cities_light.models import City
from cities_light.models import Country


class Kashrut(models.Model):
    """
    Model representing a kashrut organisation.
    Right now we only have the name but we could include more detail
    usefull for users, such as
     - who is the Rabbi that supervises the organisation
     - a contact telephone number
    """

    name = models.CharField(max_length=200, help_text="Enter a kashrut organisation")

    class Meta:
        # ensure this table is always displayed in alphabetical order
        ordering = ["name"]

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class User(models.Model):
    """
    Model representing a user
    Notes - each user must have at least one property, but may have more
          - possibly reviews could be linked to users - but it seems easier
            to link reviews to properties - which will then link back to users
            since each property has only one user
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text="Unique ID for this user"
    )

    # Ideally phone numbers should be validated.  One way to do this is using
    # the package: django-phonenumber-field. See the link below for details
    # https://django-phonenumber-field.readthedocs.io/en/latest/index.html
    # At the moment I stick with a charfield
    telno_mobile = models.CharField(max_length=15, unique=True)

    # Ideally there should be a separate table of Rabbis - which are somehow
    # authenticated.  And then the user chooses a drop down from the rabbis table
    # and if the Rabbi is not available then there would be a way to ask for one
    # to be authenticated and added
    rabbi = models.CharField(max_length=100)

    # Kashrut could be freeform - but I have chosen to have a separate table
    # The table could be maintained by admin only so that users have to select
    # from a given known authenticated list
    # There could be more than one kashrut that a user is comfortable with
    # but I have used a ForeignKey rather than onetomany
    # on_delete=models.RESTRICT means that the kashrut cannot be delete whilst
    # any user has selected it
    # null=False means that the database will not accept a null value - a user has to select
    # a kashrut.  This is not ideal if the kashrut they use is not in the Kashrut table
    # however admin can ensure that "not in list" is in the Kashrut table - and this
    # could raise an action for admin to contact the user and find their kashrut
    kashrut = models.ForeignKey("Kashrut", on_delete=models.RESTRICT, null=False)

    email = models.EmailField(max_length=255, unique=True, default="xxx@xxx")

    # user rating will need to be displayed by finding the mean of user reviews
    # from the reviews table
    # UserRating = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.telno_mobile

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this user."""
        return reverse("user-detail", args=[str(self.id)])


class Property(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text="Unique ID for this property"
    )

    # to store cities and countries I looked at this link
    # https://medium.com/@FatemeFouladkar/how-to-add-country-and-city-field-in-django-864f80b4c19e
    # I needed to pip3 install django-cities-light - and this will be added to the venv
    # I also needed to add   'cities_light', to INSTALLED_APPS and then
    #  python manage.py makemigrations
    #  python manage.py migrate
    # to add the (empty) models to sqllite3 database
    # then populate with
    # python manage.py cities_light
    # city = models.CharField(max_length=100)
    # country = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.RESTRICT, null=False)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT, null=False)

    postcode = models.CharField(max_length=20)
    address = models.TextField()
    no_of_rooms = models.PositiveIntegerField()
    estimated_value = models.FloatField()
    property_type = models.CharField(max_length=100)
    amenities = models.TextField()
    pet_friendly = models.BooleanField()
    accessibility_features = models.TextField()
    proximity_to_public_transport = models.TextField()
    nearby_attractions = models.TextField()
    succah = models.BooleanField()
    passover_kitchen = models.BooleanField()
    max_occupancy = models.PositiveIntegerField()
    smoking_allowed = models.BooleanField()
    home_description = models.TextField()

    # property rating will need to come from an average of the reviews
    # property_rating = models.FloatField(null=True, blank=True)

    # the line below only allows one image per property
    # I change the models to have an image class - see below
    # pictures_of_property = models.ImageField(upload_to='properties/')

    # Assuming each property is tied to a one user
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.address


# based on help from
# https://medium.com/@biswajitpanda973/creating-a-dynamic-product-gallery-in-django-a-guide-to-multi-image-uploads-1cefdb418201
# the class below is to store Images
# they are stored in MEDIA_ROOT/images
# set MEDIA_ROOT to /media
# this means that alonside HouseSwap and kswap we need media
# and under media we need /images
# and also in setting.py I needed
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'
# and urls.py needs to add
# from django.conf import settings
# from django.conf.urls.static import static
# if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
class Image(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
