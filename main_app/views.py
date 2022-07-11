from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Home, Amenity, Photo
import uuid
import boto3


S3_BASE_URL = 'http://s3.us-east-1.amazonaws.com/'
BUCKET = 'homebase-yas'


def home(request):
  return render(request, 'home.html')


def about(request):
  return render(request, 'about.html')


@login_required
def homes_index(request):
  homes = Home.objects.filter(user=request.user)
  return render(request, 'homes/index.html', {'homes': homes})


@login_required
def homes_detail(request, home_id):
  home = Home.objects.get(id=home_id)
  # Get the amenities the home doesn't have
  amenities_home_doesnt_have = Amenity.objects.exclude(
      id__in=home.amenities.all().values_list('id'))
  return render(request, 'homes/detail.html', {
      # Add the amenities to be displayed
      'amenities': amenities_home_doesnt_have
  })


@login_required
def assoc_amenity(request, home_id, amenity_id):
  # Note that you can pass a amenity's id instead of the whole object
  Home.objects.get(id=home_id).amenities.add(amenity_id)
  return redirect('detail', home_id=home_id)


@login_required
def assoc_amenity_delete(request, home_id, amenity_id):
  Home.objects.get(id=home_id).amenities.remove(amenity_id)
  return redirect('detail', home_id=home_id)


@login_required
def add_photo(request, home_id):
    # attempt to collect the photo file data
    photo_file = request.FILES.get('photo-file', None)
    # use conditional logic to determine if file is present
    if photo_file:
       #if it's present, we will create a reference to the boto3 client
        s3 = boto3.client('s3')
        #create a unique id for each photo file
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # upload the photo file to aws s3
        try:
          #if successful
            s3.upload_fileobj(photo_file, BUCKET, key)
            #take the exchanged url and save it to the database
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            #1) create photo instance with photo model and provide home_id as foreign key val
            photo = Photo(url=url, home_id=home_id)
            #2) save the photo instance to the database
            photo.save()
        except Exception as error:
          # print an error message
            print('An error occurred uploading file to S3')
            return redirect('detail', home_id=home_id)
        return redirect('detail', home_id=home_id)


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


class HomeCreate(LoginRequiredMixin, CreateView):
  model = Home
  fields = ['address', 'price', 'beds', 'baths', 'sqft', 'description']
  success_url = '/homes/'
  # This inherited method is called when a
  # valid home form is being submitted

  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the home
    # Let the CreateView do its job as usual
    return super().form_valid(form)


class HomeUpdate(LoginRequiredMixin, UpdateView):
  model = Home
  # Let's disallow the renaming of a home by excluding the name field!
  fields = ['address', 'price', 'beds', 'baths', 'sqft', 'description']


class HomeDelete(LoginRequiredMixin, DeleteView):
  model = Home
  success_url = '/homes/'


class AmenityList(LoginRequiredMixin, ListView):
  model = Amenity
  template_name = 'amenities/index.html'


class AmenityDetail(LoginRequiredMixin, DetailView):
  model = Amenity
  template_name = 'amenities/detail.html'


class AmenityCreate(LoginRequiredMixin, CreateView):
    model = Amenity
    fields = ['name', 'color']


class AmenityUpdate(LoginRequiredMixin, UpdateView):
    model = Amenity
    fields = ['name', 'color']


class AmenityDelete(LoginRequiredMixin, DeleteView):
    model = Amenity
    success_url = '/amenities/'
