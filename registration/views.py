from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .forms import SignUpForm, FamilyForm, AddressForm


def logout_request(request):
    logout(request)
    return render(request, 'registration/logout.html')


def signup(request):
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
