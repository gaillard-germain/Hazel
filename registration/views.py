from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import SignUpForm, FamilyForm, ChildForm, LegalGuardianForm
from .models import Family, Child


def logout_request(request):
    """Logout view"""

    logout(request)
    return render(request, 'registration/logout.html')


def signup(request):
    """Signup view"""

    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        family_form = FamilyForm(request.POST)

        if user_form.is_valid() and family_form.is_valid():
            user = user_form.save()

            group, created = Group.objects.get_or_create(name='parents')
            user.groups.add(group)

            family = family_form.save(commit=False)
            family.name = family_form.cleaned_data.get('name').upper()
            family.address = family_form.cleaned_data.get('address').upper()
            family.user = user
            family.save()

            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('home:index')
    else:
        user_form = SignUpForm()
        family_form = FamilyForm()

    context = {
        'user_form': user_form,
        'family_form': family_form,
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

    if request.method == 'POST':
        child_form = ChildForm(request.POST)
        lg1_form = LegalGuardianForm(request.POST)

        if child_form.is_valid():
            family = Family.objects.get(user=request.user.id)

            lg1 = lg1_form.save(commit=False)
            lg1.firstname = lg1_form.cleaned_data.get('firstname').title()
            lg1.lastname = lg1_form.cleaned_data.get('lastname').upper()
            lg1.address = lg1_form.cleaned_data.get('address').upper()
            lg1.save()

            child = child_form.save(commit=False)
            child.family = family
            child.firstname = child_form.cleaned_data.get('firstname').title()
            child.lastname = child_form.cleaned_data.get('lastname').upper()
            child.legal_guardian_1 = lg1
            child.save()

            return redirect('registration:myaccount')

    else:
        family = Family.objects.get(user=request.user.id)

        child_form = ChildForm()
        lg1_form = LegalGuardianForm()

        lg1_form['address'].initial = family.address

    context = {
        'child_form': child_form,
        'lg1_form': lg1_form,
    }

    return render(request, 'registration/regchild.html', context)
