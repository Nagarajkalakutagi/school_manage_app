from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .form import Register, UpdateForm
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
        image = request.FILES['image']
        pass1 = form.cleaned_data['password']
        pass2 = form.cleaned_data['conform_password']
        class_name = form.cleaned_data['class_name']

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


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(email=username, password=pass1)
        
        if user is not None:
            login(request, user)
            user = MyUser.objects.get(email=username)
            update_form = UpdateForm()
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "school/index.html", {"user": user, 'update_form': update_form})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "school/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')


def update_form(request):

    obj = MyUser.objects.get(email=request.user)
    form = UpdateForm(request.POST or None, instance=obj)

    if form.is_valid():
        ob = form.save(commit=False)
        obj.save()
        context = {"form": form}
        return render(request, "school/update.html", context)
    else:
        context = {"form": form, "error": "something went wrong"}
        return render(request, "school/update.html", context)

