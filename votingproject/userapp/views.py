from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import View
from votingapp.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.contrib import messages

# Create your views here.



class Signup(View):

    def get(self, request):
        return render(request, 'usertemp/signup.html')

    def post(self, request):
        username = request.POST.get('username')
        fullname = request.POST.get('fullname')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        
        
        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email address already exists.')
            return render(request, 'usertemp/signup.html')
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'usertemp/signup.html')
        
        # Validate the inputs as needed
        if password != password2:
            messages.error(request, 'The two password not same.')
            return render(request, 'usertemp/signup.html')    

        # Create User
        user = User.objects.create_user(username=username, password=password, email=email)

        # Create Userprofile
        Userprofile.objects.create(
            user=user,
            dob=dob,
            fullname=fullname,
            address=address,
            # Add other fields from the form or set default values
        )
        return redirect('login')  # Redirect to login page or any other page


class Login(View):
    def get(self, request):
        return render(request, 'usertemp/login.html') 
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return HttpResponse('Username and password are required', status=400)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse('Username not found', status=404)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse('Incorrect password, try again', status=401)



@login_required(login_url="login")
def Logout(request):
	logout(request)
	return redirect('login')



class BaseProfileView(View):
    def get_profile_info(self, user):
        try:
            profile = get_object_or_404(Userprofile, user=user)  
        
            profile_info = {
                'profile_image': profile.profile_image if profile.profile_image else None,
                'username': profile.fullname,
                'fullname': profile.fullname,
                'email': profile.user.email,
                'address': profile.address,
                'dob': profile.dob,
                'user': profile.user,
            }
            return {'profile_info': profile_info}

        except Userprofile.DoesNotExist:
            return {}



class ProfilePage(LoginRequiredMixin, BaseProfileView):
    login_url = 'login'

    def get(self, request):
        context = {}  # Initialize context
        try:
            context = self.get_profile_info(request.user)
          
        except:
            if request.user.is_superuser:
                Userprofile.objects.create(user=request.user)
        return render(request, 'usertemp/profile.html', context=context)

    def post(self, request):
        # Process the submitted form data
        return render(request, 'usertemp/profile.html')




class UserProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Userprofile, user=request.user)
        context = {'profile': profile}
        return render(request, 'usertemp/profile_update.html', context)

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Userprofile, user=request.user)

        # Update profile fields based on POST data
        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        dob = request.POST.get('dob')

        # Validate and update fullname
        if fullname:
            profile.fullname = fullname

        # Validate and update address
        if address:
            profile.address = address

        # Validate and update dob
        if dob:
            try:
                # Attempt to parse the provided date
                dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
                profile.dob = dob_date
            except ValueError:
                # Handle invalid date format
                messages.error(request, 'Invalid date format for Date of Birth. Use YYYY-MM-DD.')
                return redirect('updateprofile')

        # Handle profile image
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            profile.profile_image = profile_image

        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profilepage')



