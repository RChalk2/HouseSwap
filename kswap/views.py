# render is a standard Django function which takes data from
# the request object and presents it to the user according to the
# layout of a html file or according to a form
# get_object_or_404 is a function which tries to get something from
# my database and if it not there then it will show an error message
from django.shortcuts import render, redirect, get_object_or_404

# There are all my database tables.  The first line is all the ones
# I made myself and the second one is the standard User file
# from Django authentication
from .models import Kashrut, Profile, Property, Image, Booking, Review
from django.contrib.auth.models import User

# theses are forms that I wrote in the forms.py file which I use here
# in the views.py file to prepare the form to the user
from .forms import ProfileForm, PropertyForm, PropertyBookForm

# This import allows me to add @login_required before any view that I only
# want to be available to users who are logged in
from django.contrib.auth.decorators import login_required

from datetime import datetime, timedelta

# Q is an object which allows me to add SQL filtering conditions together
# so that I can return records if something is true AND something else is also true
from django.db.models import Q

from django.views import generic


# my own merge sort code
def merge_sort(array):
    # Base case for recursion: if the array is empty or has a single element, it's already sorted
    if len(array) > 1:
        # Finding the middle of the array
        mid = len(array) // 2
        # Dividing the array elements into two halves
        left = array[:mid]
        right = array[mid:]

        # Recursive call on each half
        merge_sort(left)
        merge_sort(right)

        # Initial indexes for left, right and merged subarrays
        i = 0  # Index for the left subarray
        j = 0  # Index for the right subarray
        k = 0  # Index for the merged array

        # Merging the subarrays back into array
        # Sorting in descending order based on the 'date_from' attribute
        while i < len(left) and j < len(right):
            if left[i].date_from > right[j].date_from:
                # If the current element in left is greater, add it to the merged array
                array[k] = left[i]
                i += 1
            else:
                # If the current element in right is greater, add it to the merged array
                array[k] = right[j]
                j += 1
            k += 1

        # Checking if any element was left in the left subarray
        while i < len(left):
            array[k] = left[i]
            i += 1
            k += 1

        # Checking if any element was left in the right subarray
        while j < len(right):
            array[k] = right[j]
            j += 1
            k += 1

        # The merged array is returned, sorted in descending order based on 'date_from'
        return array



# The view below updates a user profile - it is copied from a tutorial
# and the explanation of it is like this:
# It follows the pseudo code that I wrote in the design section
# It uses the request object which I explained in the design section
# IF the user is posting data to the database then it creates a form
# with that data, then it validates the data and if it is OK then it
# posts the data to the database
# If it is not OK then it creates the form again and displays it to
# the user using the html template called profile.html
def update_profile(request):

    url = request.path
    is_back_link = request.GET.get('back', 'false') == 'true'
    visit_page(request, url, is_back_link)

    # POST is adding data to the Profile table in my database
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        # This checks if the data is valid.  Because I removed most checks all data should be valid
        if form.is_valid():
            form.save()
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

    url = request.path
    is_back_link = request.GET.get('back', 'false') == 'true'
    visit_page(request, url, is_back_link)

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


# This view allows the user to enter details about one property
# They can visist this page many time if they want to put on
# lots of properties.
# It follows exaxctly the same pseudo code as lots of the other views
# One thing it does differnt is that it does not ask the user to enter
# wno they are because it already knows this from the request object
# instead it adds this in itself using the code:
# property_form.owner = request.user
def property_registration(request):

    url = request.path
    is_back_link = request.GET.get('back', 'false') == 'true'
    visit_page(request, url, is_back_link)

    if request.method == "POST":
        form = PropertyForm(request.POST)
        if form.is_valid():
            # create a variable called property_form which can then be added to
            # but don't save it to the database yet
            property_form = form.save(commit=False)
            # add the owner (which is the user) to property form
            property_form.owner = request.user
            # now sabe it to the database
            property_form.save()

            images = request.FILES.getlist("images")
            for image in images:
                photo = Image(property=property_form, image=image)
                photo.save()
            return redirect("home")
    else:
        form = PropertyForm()
    return render(request, "property_registration.html", {"form": form})


# This view is to show a list of all properties which are
# available for booking.  I based it on generic.ListView
# because without doing anything this class will already
# display for me all the properties in the database
# and I can easily limit the display to include just a small number
# of important information about each property
# Because it is a class based view, I need to add my back link code
# ito the get method.  The get method gets used when this class based
# view is used.  So the stack code will be done
class PropertyListView(generic.ListView):
    model = Property
    context_object_name = 'property_list'

    def get(self, request, *args, **kwargs):
        url = request.path
        is_back_link = request.GET.get('back', 'false') == 'true'
        visit_page(request, url, is_back_link)
        # Beside the code that I added - I still need to make sure
        # that the get method does what it is normally meant to do
        # It normaly inherits get based on generic.DetailView which
        # is called the superclass so I now call
        # the superclass get method and return its result
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # Capture start_date and end_date from the request
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        # include all properties and also include the Profile for this user
        queryset = Property.objects.select_related('owner__profile')

        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            # Filter out properties that have conflicting bookings
            booked_properties = Booking.objects.filter(
                Q(date_from__lte=end_date) & Q(date_to__gte=start_date)
            ).values_list('property', flat=True)

            # finaly exclude properties that have already been booked
            queryset = queryset.exclude(id__in=booked_properties)

        return queryset


# The view of property detail is a standard generic view
# and so I based it on the class that Django provides for
# this which is called generic.DetailView
# Because it is a class based view, I need to add my back link code
# ito the get method.  The get method gets used when this class based
# view is used.  So the stack code will be done
class PropertyDetailView(generic.DetailView):
    model = Property

    def get(self, request, *args, **kwargs):
        url = request.path
        is_back_link = request.GET.get('back', 'false') == 'true'
        visit_page(request, url, is_back_link)

        # Beside the code that I added - I still need to make sure
        # that the get method does what it is normally meant to do
        # It normaly inherits get based on generic.DetailView which
        # is called the superclass so I now call
        # the superclass get method and return its result
        return super().get(request, *args, **kwargs)


# View for booking a property
def property_book(request, pk):

    url = request.path
    is_back_link = request.GET.get('back', 'false') == 'true'
    visit_page(request, url, is_back_link)

    if request.method == "POST":
        form = PropertyBookForm(request.POST, user=request.user)
        if form.is_valid():
            booking_form = form.save(commit=False)
            booking_form.property = Property.objects.get(pk=pk)
            booking_form.user = request.user
            booking_form.save()
            return redirect("home")
    else:
        form = PropertyBookForm(user=request.user)
    return render(request, "booking.html", {"form": form})


def pending_bookings(request):

    url = request.path
    is_back_link = request.GET.get('back', 'false') == 'true'
    visit_page(request, url, is_back_link)

    if request.method == 'POST':
        # Capture the booking ID and action from POST data
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')

        # Retrieve the booking object
        booking = Booking.objects.get(id=booking_id)

        # Update the booking status based on the action
        if action == "accept":
            booking.status = 'accepted'
        elif action == "decline":
            booking.status = 'declined'

        booking.save()
        return redirect("home")

    else:
        # Decline bookings with a start date in less than one day
        Booking.objects.filter(date_from__lte=datetime.now() + timedelta(days=1), status='pending').update(status='declined')

        # In the end,  I  created  the pending_requests_count  as a dict
        # using something called a context processor which I stored in   the file
        # called  context_processors.py in the same directory as this file
        # And  then  I  had to add it to settings.py under HouseSwap
        # and then the variable is always available in any template and not just
        # when this view is being used
        # Get pending bookings for current user's properties

        # in order to see if I can do this with my own sort, I commented out this line
        #bookings = Booking.objects.filter(property__owner=request.user, status='pending').order_by('-date_from')
        # and instead I just fetch the data and then try to sort it

        # fetch the data
        bookings = list(Booking.objects.filter(property__owner=request.user, status='pending'))

        # apply merge sort
        bookings = merge_sort(bookings)

        #pending_requests_count = bookings.count()

        return render(request, 'pending_bookings.html', {'bookings': bookings})


def your_next_escapes(request):

    url = request.path
    is_back_link = request.GET.get('back', 'false') == 'true'
    visit_page(request, url, is_back_link)

    bookings = Booking.objects.filter(Q(property__owner=request.user) | Q(my_property__owner=request.user), status='accepted').order_by('-date_from')
    return render(request, 'your_next_escapes.html', {'bookings': bookings})


def user_dashboard(request):

    url = request.path
    is_back_link = request.GET.get('back', 'false') == 'true'
    visit_page(request, url, is_back_link)

    # Count the number of properties and users
    num_properties = Property.objects.filter(owner=request.user).count()
    profile = Profile.objects.get(user=request.user)
    user_kashrut = profile.kashrut

    context = {
        "num_properties": num_properties,
        "user_kashrut": user_kashrut,
    }

    # Render the template home.html with data in the context dictionary
    return render(request, "user_dashboard.html", context=context)


# This view is the last view I will need for the proof of concept
# (besides the back buttton)
# It calls the function below which I called leave_review_sub
def leave_review(request):

    url = request.path
    is_back_link = request.GET.get('back', 'false') == 'true'
    visit_page(request, url, is_back_link)

    # Fetch eligible bookings for the current user
    # Allow for review for pending, accpeted or declined
    # for example if it stays pending and the other person did not even decline
    # then a review could be that the other person is not very responsive
    eligible_bookings = Booking.objects.filter(
        #status='accepted',  # Assuming 'accepted' status means eligible for review
        user=request.user
    )

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        review_text = request.POST.get('review_text')
        review_stars = request.POST.get('review_stars')
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)

        leave_review_sub(booking, request.user, review_text, int(review_stars))
        return redirect("home")

    return render(request, 'leave_review.html', {'bookings': eligible_bookings})


def leave_review_sub(booking, reviewer, review_text, review_stars):

    # Determine the property to be reviewed and the reviewer
    if booking.property.owner == reviewer:
        property_reviewed = booking.my_property
    elif booking.my_property.owner == reviewer:
        property_reviewed = booking.property
    else:
        raise Exception("Invalid reviewer for this booking.")

    # Create a review
    review = Review.objects.create(
        booking=booking,
        property_reviewed=property_reviewed,
        reviewer=reviewer,
        text=review_text,
        stars=review_stars
    )
    return review


# This creates a stack class for the go back link
# I have used the Python inbuilt list to do this
# I don't need the peek method which stacks normally have
# because I will never look at and item in the stack without removing it
# but I programmed it in anyway
# I had a big problem that I am storing this Stack with all the other session
# information that Django stores.  And Django stores it in a json format and
# it can only deal with simple things like dictionaries or lists.
# So each time I use this stack I have to turn it into a simple list.
# so I added two methods at the end.  One which extracts the list of items
# from the Stach and another one which creates a stack from a list of items

class Stack:
    # when I first called the stack, the items in it is an empty list
    def __init__(self):
        self.items = []

    # I do the push method using the append method of python lists
    def push(self, item):
        self.items.append(item)

    # I do the pop method using the pop method of lists
    def pop(self):
        return self.items.pop() if len(self.items) >= 1 else None

    # I dont use this and I have not checked what happens if it tries
    # to peek at a list which has nothing in it
    def peek(self):
        return self.items[-1]

    # I will probably need to use is_empty to handle cases where the user
    # presses the back link and the stack is empty
    def is_empty(self):
        return len(self.items) == 0

    # I might used the size method to make sure I dont ever grow the stack too big
    def size(self):
        return len(self.items)

    # I need to turn this class in to a dictionary since Django will not save
    # it properly otherwise
    def to_json(self):
        return self.items

    # and here I need to turn it back again
    # I added the @staticmethod because I was getting errors because I don't
    # need this method to receive self autmatically as the first argument
    # because it actually makes a Stack in the first line when it says
    # stack = Stack()
    @staticmethod
    def from_json(json_data):
        stack = Stack()
        for item in json_data:
            stack.push(item)
        return stack

# This view is for the 'back' link
# It is actually quite complicated to do this
# because the url is added to the stack at the beginning of each view
# and that means that if I just do that, then every time I pop the url
# then when I go and visit that page, the url will be added back to the list!!
# So I need some kind of argument which tells me if I am visting the page
# normally or because I am coming from the go_back view
# It turns out that I can do this using the normal redirect function and add
# to it the argument back=true by typing ?back=true
def go_back(request):
    visited_links = request.session.get('visited_links', Stack())
    print('start of go_back - visited links')
    if not isinstance(visited_links, Stack):
        temp = Stack()
        visited_links = temp.from_json(visited_links)

    print('before pop')
    print(visited_links)
    last_visited = visited_links.pop()
    # put the list I am using for a stack back into the session
    request.session['visited_links'] = visited_links.to_json()
    # check if anything came off the stack
    # I mean that if it is empty then nothing will come off it
    if last_visited:
        return redirect(f"{last_visited}?back=true")
    else:
        return redirect(home)


# This function is called in every single view
# and it add the page if the user is not coming from the go_back
# view just above here in the code
def visit_page(request, url, is_back_link):
    print('is_back_link')
    print(is_back_link)
    visited_links = request.session.get('visited_links', Stack())
    if not isinstance(visited_links, Stack):
        temp = Stack()
        visited_links = temp.from_json(visited_links)
    print(visited_links.items)

    if not is_back_link:
        visited_links.push(url)
        # Save the updated stack is saved back to the session
        request.session['visited_links'] = visited_links.to_json()
