from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Kashrut, User, Property, Image


# The view function below is based on code from the local library tutorial index page at
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Home_page
# The "request" object passed to the function below is an "HttpRequest" object
# django docs say that
# When a page is requested, Django creates an HttpRequest object that
# contains information about the request.
def home(request):

    # Count the number of properties and users
    num_properties = Property.objects.all().count()
    num_users = User.objects.all().count()
    num_kashrut = Kashrut.objects.count()

    context = {
        'num_properties': num_properties,
        'num_users': num_users,
        'num_kashrut': num_kashrut,
    }

    # Render the template home.html with data in the context dictionary above
    return render(request, 'home.html', context=context)


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # you might want to authenticate and log the user in at this point
            # then, redirect to a success page or homepage
            return redirect('some-view-name')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})
