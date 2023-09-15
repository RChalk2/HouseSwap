from django.shortcuts import render, redirect
from .forms import RegistrationForm

def home(request):
    return render(request, 'users/home.html')


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
