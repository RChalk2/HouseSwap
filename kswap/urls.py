from django.urls import path
from . import views

urlpatterns = [
   # in the path() function below, the urlpattern is an empty string
   # this urls.py file is included into the project by urls.py in HouseSwap
   # and the path there is ALSO blank
   # this means that the houme page will be found at 127.0.0.1:8000
   # If I add extra apps, then I could change the path there to kswap/
   # and then all the pages here would be found under 127.../kwsap
   path('', views.home, name='home'),
  ]
