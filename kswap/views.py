from django.shortcuts import render, redirect

from .models import Kashrut, Profile, Property, Image
from django.contrib.auth.models import User

from .forms import ProfileForm, PropertyForm, PropertyBookForm
from django.contrib import messages

# This import allows me to add @login_required before any view that I only
# want to be available to users who are logged in
from django.contrib.auth.decorators import login_required


# The view below updates a user profile - it is copied from a tutorial
def update_profile(request):
    # POST is adding data to the Profile table in my database
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        # This checks if the data is valid.  Because I removed most checks all data should be valid
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully updated your profile.")
            return redirect("home")
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "profile.html", {"form": form})


# The view function below is based on the local library tutorial index page
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Home_page
# The "request" passed to the function below is an "HttpRequest" object
# django docs say that
# When a page is requested, Django creates an HttpRequest object that
# contains information about the request.
def home(request):
    # Count the number of properties and users
    num_properties = Property.objects.all().count()
    num_users = User.objects.all().count()
    num_kashrut = Kashrut.objects.count()

    context = {
        "num_properties": num_properties,
        "num_users": num_users,
        "num_kashrut": num_kashrut,
    }

    # Render the template home.html with data in the context dictionary
    return render(request, "home.html", context=context)


def property_registration(request):
    if request.method == "POST":
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_form = form.save(commit=False)
            property_form.owner = request.user
            property_form.save()

            images = request.FILES.getlist("images")
            for image in images:
                photo = Image(property=property_form, image=image)
                photo.save()
            return redirect("home")
    else:
        form = PropertyForm()
    return render(request, "property_registration.html", {"form": form})


from django.views import generic

class PropertyListView(generic.ListView):
    model = Property
    context_object_name = 'property_list'


class PropertyDetailView(generic.DetailView):
    model = Property

def property_book(request):
    # POST is adding data to the Profile table in my database
    if request.method == "POST":
        form = PropertyBookForm(request.POST, instance=request.user.profile)
        # This checks if the data is valid.  Because I removed most checks all data should be valid
        if form.is_valid():
            form.save()
            messages.success(request, "You have sent a booking request")
            return redirect("home")
    else:
        form = PropertyBookForm(instance=request.user.profile)
    return render(request, "profile.html", {"form": form})