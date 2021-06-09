from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import Http404
from .forms import SignUpForm, FamilyForm, AddressForm
from .models import Family, Address, Child


def logout_request(request):
    """Logout view"""

    logout(request)
    return render(request, 'registration/logout.html')


def signup(request):
    """Signup view"""

    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        family_form = FamilyForm(request.POST)
        address_form = AddressForm(request.POST)

        if (user_form.is_valid() and family_form.is_valid()
                and address_form.is_valid()):
            user = user_form.save()
            user.save()

            address = address_form.save()
            address.save()

            group, created = Group.objects.get_or_create(name='parents')
            user.groups.add(group)

            family = family_form.save(commit=False)
            family.user = user
            family.address = address
            family.save()

            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('home:index')
    else:
        user_form = SignUpForm()
        family_form = FamilyForm()
        address_form = AddressForm()

    context = {
        'user_form': user_form,
        'family_form': family_form,
        'address_form': address_form
    }

    return render(request, 'registration/signup.html', context)


def manage_account(request):
    """User's account informations view"""

    if request.user.is_authenticated:
        family = Family.objects.get(user=request.user.id)
        children = Child.objects.filter(family=family.id)
        context = {
            'family': family,
            'children': children
        }
        return render(request, 'registration/myaccount.html', context)
    else:
        raise Http404()


def register_new_child(request):
    return render(request, 'registration/regchild.html')
