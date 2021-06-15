from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import (SignUpForm, FamilyForm, ChildForm, LegalGuardianForm,
    AuthorizedPersonForm, ParentalAuthorizationForm, DoctorForm)
from .models import Family, Child, Adult


def logout_request(request):
    """Logout view"""

    logout(request)
    return render(request, 'registration/logout.html')


def signup(request):
    """Signup view"""

    user_form = SignUpForm(request.POST or None)
    family_form = FamilyForm(request.POST or None)
    doctor_form = DoctorForm(request.POST or None)

    if request.method == 'POST':
        if (user_form.is_valid() and family_form.is_valid()
            and doctor_form.is_valid()):
            user = user_form.save()

            group, created = Group.objects.get_or_create(name='parents')
            user.groups.add(group)

            family = family_form.save(commit=False)
            family.name = family_form.cleaned_data.get('name').upper()
            family.address = family_form.cleaned_data.get('address').upper()
            family.user = user
            family.doctor = Adult.create_doc(doctor_form)
            family.save()

            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('home:index')

    context = {
        'user_form': user_form,
        'family_form': family_form,
        'doctor_form': doctor_form
    }

    return render(request, 'registration/signup.html', context)


def manage_account(request):
    """User's account informations view"""

    if request.user.is_authenticated:
        family = Family.objects.get(user=request.user.id)
        children = Child.objects.filter(family=family.id)
        authorized_persons = Adult.objects.filter(family_friends=family)

        context = {
            'family': family,
            'children': children,
            'authorized_persons': authorized_persons
        }
        return render(request, 'registration/myaccount.html', context)
    else:
        raise Http404()

# class ChildWizard(SessionWizardView):
#     template_name = 'registration/regchild.html'
#     form_list = [ChildForm, LegalGuardianForm]
#
#     def done(self, form_list, **kwargs):
#         return render(self.request, 'done.html', {
#             'form_data': [form.cleaned_data for form in form_list],
#         })


def regchild_step1(request):
    """ first step form to register a child """

    initial = {'child': request.session.get('child', None)}
    form = ChildForm(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            request.session['child'] = form.cleaned_data
            return redirect('registration:regchild_step2')

    context  = {
        'form': form,
        'h2': 'Enfant',
        'step': 1
    }

    return render(request, 'registration/regchild.html', context)


def regchild_step2(request):
    """ second step form to register a child """

    form = LegalGuardianForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            request.session['lg1'] = form.cleaned_data
            return redirect('registration:regchild_step3')

    context  = {
        'form': form,
        'h2': 'Mère / Responsable Légal 1',
        'step': 2
    }

    return render(request, 'registration/regchild.html', context)


def regchild_step3(request):
    """ third step form to register a child """

    form = LegalGuardianForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            request.session['lg2'] = form.cleaned_data
            return redirect('registration:regchild_step4')

    context  = {
        'form': form,
        'h2': "Père / Responsable légal 2",
        'step': 3
    }

    return render(request, 'registration/regchild.html', context)


def regchild_step4(request):
    """ fourth step form to register a child """

    form = ParentalAuthorizationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            family = Family.objects.get(user=request.user.id)
            child = Child.create_child(family, request.session['child'])
            lg1 = Adult.create_lg(request.session['lg1'])
            lg2 = Adult.create_lg(request.session['lg2'])
            child.legal_guardian_1 = lg1
            child.legal_guardian_2 = lg2
            child.go_alone = form.cleaned_data['go_alone']
            child.activity = form.cleaned_data['activity']
            child.image_rights = form.cleaned_data['image_rights']
            child.save()
            return redirect('registration:myaccount')

    context  = {
        'form': form,
        'h2': "Autorisations parentales",
        'step': 4
    }

    return render(request, 'registration/regchild.html', context)


def regperson(request):

    form = AuthorizedPersonForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            family = Family.objects.get(user=request.user.id)
            person = Adult.create_person(form)
            family.authorized_person.add(person)

            return redirect('registration:myaccount')

    context = {'form': form}

    return render(request, 'registration/regperson.html', context)
