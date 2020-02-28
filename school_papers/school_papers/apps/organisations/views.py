from django.shortcuts import redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send an email to the user with the token:
            mail_subject = 'Активируйте свой аккаунт'
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            message = render_to_string('order/acc_active_email.html', {
                'user': user.username,
                'domain': current_site,
                'uid': uid,
                'token': token,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = "html"
            email.send()
            messages.success(request, 'Письмо в подтверждением отправлено на электронную почту!')
            return redirect('login')

    else:
        form = UserRegistrationForm()
    return render(request, 'order/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'order/profile.html')


User = get_user_model()


def activate(request, uidb64=1, token=1):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        update_session_auth_hash(request, user)
        return redirect('profile')
    else:
        return HttpResponse('Activation link is invalid!')
