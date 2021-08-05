from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.http import Http404, JsonResponse
from django.forms.models import model_to_dict
from .forms import (SignUpForm, FamilyForm, ChildForm, AuthorizedPersonForm,
                    ParentalAuthorizationForm, DoctorForm)
from .models import User, Family, Child, Adult
from booking.models import Booking, Slot
from datetime import date


class SignUp(View):
    """ A view to register a new user """

    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST or None)

        if form.is_valid():
            user = form.save()

            group, created = Group.objects.get_or_create(name='parents')
            user.groups.add(group)

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('home:index')

        context = {'form': form}

        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class RegFamily(View):
    """ A view to register a new family or to modify the informations """

    modify = False
    family_form_class = FamilyForm
    doctor_form_class = DoctorForm
    template_name = 'registration/regfamily.html'

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)

        if self.modify:
            old_family = Family.objects.get(user=user)
            old_doctor = Adult.objects.get(id=old_family.doctor.id)
            family_form = self.family_form_class(
                request.POST or None,
                initial=model_to_dict(old_family)
            )
            doctor_form = self.doctor_form_class(
                request.POST or None,
                initial=model_to_dict(old_doctor)
            )

        else:
            family_form = self.family_form_class(request.POST or None)
            doctor_form = self.doctor_form_class(request.POST or None)

        if family_form.is_valid() and doctor_form.is_valid():
            family = family_form.save(commit=False)
            if self.modify:
                family.id = old_family.id

            family.user = user
            family.doctor = Adult.create_doc(doctor_form)
            family.save()

            return redirect('registration:myaccount')

        context = {
            'modify': self.modify,
            'family_form': family_form,
            'doctor_form': doctor_form
        }

        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ManageAccount(View):
    """ A view to display user's account informations """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                family = Family.objects.get(user=request.user.id)

            except Family.DoesNotExist:
                return redirect('registration:regfamily')

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


class RegChild(View):
    """ A view to register a new child (step-by-step) """

    form_class = ChildForm
    template_name = 'registration/regchild.html'
    session_key = 'child'
    title = 'Enfant'
    step = 1

    def post(self, request, *args, **kwargs):
        if request.session.get(self.session_key):
            data = request.session[self.session_key]
        else:
            data = None

        form = self.form_class(request.POST or None, initial=data)

        if form.is_valid():
            birth_date = form.cleaned_data.get('birth_date')
            if birth_date:
                form.cleaned_data['birth_date'] = date.isoformat(birth_date)

            request.session[self.session_key] = form.cleaned_data
            return redirect('registration:regchild_step{}'.format(self.step+1))

        context = {
            'form': form,
            'h2': self.title,
            'step': self.step
        }

        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class RegChildFinal(RegChild):
    """ Final view to complet child registration """

    form_class = ParentalAuthorizationForm
    title = 'Autorisations parentales'
    step = 4

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST or None)

        if form.is_valid():
            family = Family.objects.get(user=request.user.id)
            child = Child.create_child(family, request.session['child'])
            lg1 = Adult.create_lg(request.session['lg1'])
            lg2 = Adult.create_lg(request.session['lg2'])
            child.legal_guardian_1 = lg1
            child.legal_guardian_2 = lg2
            child.go_alone = form.cleaned_data.get('go_alone')
            child.activity = form.cleaned_data.get('activity')
            child.image_rights = form.cleaned_data.get('image_rights')
            child.save()
            return redirect('registration:myaccount')

        context = {
            'form': form,
            'h2': self.title,
            'step': self.step
        }

        return render(request, self.template_name, context)


class RegPerson(View):
    """ A view to register new person with the ability
        to pick-up the children """

    form_class = AuthorizedPersonForm
    template_name = 'registration/regperson.html'

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST or None)

        if form.is_valid():
            family = Family.objects.get(user=request.user.id)
            person = Adult.create_person(form)
            family.authorized_person.add(person)

            return redirect('registration:myaccount')

        context = {'form': form}

        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class DeleteThis(View):
    """ A view allowing the removing of a child or an authorized person
        from family"""

    def post(self, request, *args, **kwargs):

        response = {}
        family = Family.objects.get(user=request.user.id)
        this_kind = request.POST.get('this_kind')
        this_id = request.POST.get('this_id')

        if this_kind == 'child':
            try:
                child = Child.objects.get(id=this_id)
                child.family = None
                child.save()
                response['status'] = 'OK'

            except Child.DoesNotExist:
                raise Http404()

        elif this_kind == 'adult':
            try:
                person = Adult.objects.get(id=this_id)
                family.authorized_person.remove(person)
                response['status'] = 'OK'

            except Adult.DoesNotExist:
                raise Http404()

        return JsonResponse(response)
