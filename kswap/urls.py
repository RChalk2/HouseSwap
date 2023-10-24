from django.urls import path
from . import views

urlpatterns = [
    # in the path() function below, the urlpattern is an empty string
    # this urls.py file is included into the project by urls.py in HouseSwap
    # and the path there is ALSO blank
    # this means that the homepage will be found at 127.0.0.1:8000
    # If I add extra apps, then I could change the path there to kswap/
    # and then all the pages here would be found under 127.../kwsap
    path("", views.home, name="home"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path(
        "property_registration/",
        views.property_registration,
        name="property_registration",
    ),
    path('property_search/', views.PropertyListView.as_view(), name='property_search'),
    path('property_detail/<int:pk>', views.PropertyDetailView.as_view(), name='property_detail'),
    path('property_book/<int:pk>', views.property_book, name='property_book'),
    path('pending_bookings/', views.pending_bookings, name='pending_bookings'),
    path('your_next_escapes/', views.your_next_escapes, name='your_next_escapes'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
]

