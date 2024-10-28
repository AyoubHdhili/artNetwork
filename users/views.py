from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from .forms import UserRegisterForm, UserLoginForm , UserUpdateForm
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import User
from django.conf import settings
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) 
            user.role = 'user'  
            user.save()  
            return redirect('login') 
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']  
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password) 
            if user is not None:
                if not user.is_active:  
                    form.add_error(None, "Votre compte est désactivé. Veuillez contacter l'administrateur.")
                else:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    request.session['access_token'] = access_token
                    request.session['full_name'] = user.fullname
                    request.session['email'] = user.email
                    request.session['userphoto'] = user.user_photo.url if user.user_photo else None
                    if user.role == 'admin' and user.is_superuser and user.is_staff:
                        return redirect('/admin/') 
                    else:
                        return redirect('/posts')
            else:
                form.add_error(None, "invalid credentials or your account is not active.")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request) 
    if 'access_token' in request.session:
        del request.session['access_token']
        del request.session['full_name']
        del request.session['email']
        del request.session['userphoto']
    return redirect('login') 

@login_required
@csrf_exempt
def toggle_user_status(request, user_id):
    user = User.objects.get(pk=user_id)
    user.toggle_active()  
    return JsonResponse({'status': 'success', 'is_active': user.is_active})




@login_required
def update_user(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
          
            request.session['full_name'] = user.fullname
            request.session['userphoto'] = user.user_photo.url if user.user_photo else None
            
         
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            request.session['access_token'] = access_token 
            
            return redirect('update_user')  
    else:
        form = UserUpdateForm(instance=user)  

    return render(request, 'ProfileFront.html', {
        'form': form,
        'user': user,
        'MEDIA_URL': settings.MEDIA_URL  
    })


