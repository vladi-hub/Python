from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect

# Create your views here.
from .models import Location
from .models import Asset
from .models import Service

from homeinventory.forms import SignUpForm,LocationForm,AssetForm, LoginForm
from homeinventory.tokens import account_activation_token

@login_required
def home(request):
    return render(request, 'dashboard.html')
	
def loginUser(request):
	print("login.......")
	if request.method == 'POST':
		form = LoginForm(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			l_list = Location.objects.filter(user__pk=request.user.id)
			context = {'locations': l_list}
			return render(request, 'dashboard.html', context)
		else:
			# Return an 'invalid login' error message.
			 return 
	else:
		form = LoginForm()
		return render(request, 'login.html', {'form': form})
	
	
def main(request,cmd):
	if cmd == 'login':
		form = LoginForm()
	else:
		form = SignUpForm()
	context = {'cmd': cmd, 'form' : form}
	return render(request, 'index.html',context)
	
def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')	
	
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')

def signup(request):
	print("Signup ...... " + request.method)
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			subject = 'Activate Your HomeInventory Account'
			message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
			user.email_user(subject, message)
			return redirect('account_activation_sent')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})	


def locations(request):
	location = Location.objects.get(id=request.id)
	asset = Asset.objects.filter(location=location.id)
	service = Service.objects.filter(location=location.id)
	context = {'location': location,'assets':asset,'services':service}
	return render(request, 'locationsview.html', context)
	
@login_required	
def location_id(request,id):
	location = None
	try:
		location = Location.objects.get(pk=id)
		print(location)
	except Location.DoesNotExist:
		print('New Location')
	print(request.method)	
	#New - save
	if request.method == 'POST' and location is None:
        # create a form instance and populate it with data from the request:
		form = LocationForm(request.POST)
        # check whether it's valid:
		if form.is_valid():
			location = form.save(commit=False)
			location.user = request.user;
			location.save()
			return redirect('dashboard')
	# NEW Object
	elif request.method != 'POST' and location is None:
		form = LocationForm()
		return render(request, 'locationsview.html', {'form':form})
    # Edit
	elif request.method != 'POST' and location is not None:
		form = LocationForm(instance=location)
		return render(request,'locationsview.html',{'form':form,'location':location})
	# Update
	elif request.method == 'POST' and location is not None:
		print('POST and location')
		form = LocationForm(request.POST,instance=location)
		if form.is_valid():
			location = form.save(commit=False)
			location.user = request.user;
			location.save()
		return redirect('dashboard')
	else:
    #context = {'location': location}
		#return HttpResponseRedirect('dashboard.html')
		return redirect('dashboard')
	
def asset(request,id):
    asset = Asset.objects.filter(id=request.id)
    context = {'asset': asset}
    return render(request, 'assetview.html', context)
	
def service(request, id):
    service = Service.objects.filter(id=request.id)
    context = {'service': service}
    return render(request, 'serviceview.html', context)
	
@login_required	
def user(request):
    user = User.objects.get(pk=request.user.id)
    context = {'user': user}
    return render(request, 'profile.html', context)
	
@login_required	
def user_save(request):
	user = User.objects.get(pk=request.user.id)
	if check_password('the default password', user.password):
		user.save()
		return render(request, 'dashboard.html')
	else:
		context = {'msg':'Old Password is wrong'}
		return render(request, 'profile.html', context)
	
	
@login_required		
def asset_id(request, id, location_id):
	asset = None
	try:
		asset = Asset.objects.get(pk=id)
		print(asset)
	except Asset.DoesNotExist:
		print('New Asset')
	#New - save
	if request.method == 'POST' and asset is None:
        # create a form instance and populate it with data from the request:
		form = AssetForm(request.POST)
        # check whether it's valid:
		if form.is_valid():
			asset = form.save(commit=False)
			asset.user = request.user;
			asset.save()
			return redirect('dashboard')
	# NEW Object
	elif request.method != 'POST' and asset is None:
		
		location = Location.objects.get(pk=location_id)
		form = AssetForm()
		form.fields['location'].initial = location
		return render(request, 'assetview.html', {'form':form})
    # Edit
	elif request.method != 'POST' and asset is not None:
		form = AssetForm(instance=asset)
		form.location = asset.location
		return render(request,'assetview.html',{'form':form,'asset':asset})
	# Update
	elif request.method == 'POST' and asset is not None:
		form = AssetForm(request.POST,instance=asset)
		if form.is_valid():
			asset = form.save(commit=False)
			asset.user = request.user;
			asset.save()
		return redirect('dashboard')
	else:
    #context = {'location': location}
		#return HttpResponseRedirect('dashboard.html')
		return redirect('dashboard')
	
@login_required		
def newasset(request):
	form = AssetForm()
	return render(request, 'assetview.html', {'form':form})

@login_required		
def service_id(request, id):
    service = Service.objects.get(pk=id)
    context = {'service': service}
    return render(request, 'servicesview.html', context)
	