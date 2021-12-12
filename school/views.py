from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .form import Register
from .models import MyUser, ClassName


# Create your views here.
def home(request):
    return render(request, "school/index.html")


def my_class(request):
    if request.method == "POST":
        class_name = request.POST['class']
        data = ClassName.objects.create(class_name=class_name)

        if data:
            messages.error(request, "Class is created")
            return render(request, "school/class.html")
    return render(request, "school/class.html")


def signup(request):
    if request.method == "POST":
        form = Register(request.POST, request.FILES)
        print(form)
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        dob = form.cleaned_data['dob']
        status = form.cleaned_data['status']
        email = form.cleaned_data['email']
        image = request.FILES.get['image']
        pass1 = form.cleaned_data['password']
        pass2 = form.cleaned_data['conform_password']
        class_name = form.cleaned_data['class_name']
        print(class_name)

        if MyUser.objects.filter(email=email):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        user = MyUser.objects.create_user(email, pass1)
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.dob = dob
        user.status = status
        user.is_active = False
        user.image = image
        user.class_name = class_name
        user.save()

        return redirect('signin')
    else:
        form = Register()

    return render(request, "school/signup.html", {'form': form})


# def activate(request,uidb64,token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         myuser = User.objects.get(pk=uid)
#     except (TypeError,ValueError,OverflowError,User.DoesNotExist):
#         myuser = None
#
#     if myuser is not None and generate_token.check_token(myuser,token):
#         myuser.is_active = True
#         # user.profile.signup_confirmation = True
#         myuser.save()
#         login(request, myuser)
#         messages.success(request, "Your Account has been activated!!")
#         return redirect('signin')
#     else:
#         return render(request,'activation_failed.html')html


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "school/index.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "school/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')