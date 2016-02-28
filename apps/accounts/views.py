from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from apps.accounts.forms import *
from apps.accounts.models import *
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone


def register_user(request, seller=False):
    args = {}
    args.update(csrf(request))

    args['seller'] = seller

    if request.method == 'POST':

        if seller:
            form = SellerRegistrationForm(request.POST)
        else:
            form = CustomerRegistrationForm(request.POST)

        args['form'] = form
        if form.is_valid():
            form.save(seller)  # save user to database if form is valid

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            if seller:
                company_name = form.cleaned_data['company_name']
            else:
                company_name = None

            salt = hashlib.sha1((str(random.random())).encode('utf-8')).hexdigest()[:5]
            activation_key = hashlib.sha1((salt+email).encode('utf-8')).hexdigest()

            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            # Get user by username
            user = User.objects.get(username=username)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key, key_expire=key_expires,
                                      company_name=company_name)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Подтверждение регистрации'
            email_body = "Добрый день, %s! Спасибо за регистрацию на нашем сайте. Для подтверждения учетной записи, \
             пожалуйста, перейдите по ссылке: http://127.0.0.1:8000/accounts/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'alexdolgov88@gmail.com', [email], fail_silently=False)

            return HttpResponseRedirect('/')
    else:
        if seller:
            args['form'] = SellerRegistrationForm()
        else:
            args['form'] = CustomerRegistrationForm()

    return render_to_response('register.html', args, context_instance=RequestContext(request))


def register_confirm(request, activation_key):

    if request.user.is_authenticated():
        HttpResponseRedirect('/')

    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    if user_profile.key_expire < timezone.now().date():
        return render_to_response('confirm_expired.html')

    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('confirm.html')
