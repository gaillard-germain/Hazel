from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
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


class SignUp(TemplateView):

    user_form_class = SignUpForm
    family_form_class = FamilyForm
    doctor_form_class = DoctorForm
    template_name = 'registration/signup.html'

    def post(self, request):
        post_data = request.POST or None
        user_form = self.user_form_class(post_data, prefix='user')
        family_form = self.family_form_class(post_data, prefix='family')
        doctor_form = self.doctor_form_class(post_data, prefix='doctor')

        context = self.get_context_data(
            user_form=user_form,
            family_form=family_form,
            doctor_form=doctor_form
        )

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

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ManageAccount(View):

    def get(self, request):
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


class RegChild(View):

    form_class = ChildForm
    template_name = 'registration/regchild.html'
    session_key = 'child'
    title = 'Enfant'
    step = 1

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST or None)

        if form.is_valid():
            request.session[self.session_key] = form.cleaned_data
            return redirect('registration:regchild_step{}'.format(self.step+1))

        context  = {
        'form': form,
        'h2': self.title,
        'step': self.step
        }

        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class RegChildFinal(RegChild):

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
            child.go_alone = form.cleaned_data['go_alone']
            child.activity = form.cleaned_data['activity']
            child.image_rights = form.cleaned_data['image_rights']
            child.save()
            return redirect('registration:myaccount')

        context  = {
        'form': form,
        'h2': self.title,
        'step': self.step
        }

        return render(request, self.template_name, context)


class RegPerson(View):

    form_class = AuthorizedPersonForm
    template_name = 'registration/regperson.html'

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST or None)

        if form.is_valid():
            family = Family.objects.get(user=request.user.id)
            person = Adult.create_person(form)
            family.authorized_person.add(person)

            return redirect('registration:myaccount')

        context  = {'form': form}

        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
