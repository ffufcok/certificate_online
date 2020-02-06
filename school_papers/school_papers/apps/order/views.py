from django.shortcuts import render
from django.core.mail import EmailMessage
from .forms import OrderForm
from django.utils import timezone
from docxtpl import DocxTemplate
from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from .tokens import email_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string



def homepage(request):
    return render(request, 'order/main.html', {})


def new_order(request):
    form = OrderForm()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            editable = form.save(commit=False)
            editable.date = timezone.now()
            doc = DocxTemplate("D:/Desktop/D_school_papers/school_papers/school_papers/doc_template/d.docx")
            context = {'number': editable.id, 'surname': editable.surname, 'name': editable.name,
                       'father': editable.father, 'class': editable.class_letter}
            doc.render(context)
            msg = EmailMessage('Справка', 'Справка с места учёбы', 'tol063115@gmail.com', [editable.email])
            msg.content_subtype = "html"
            name = settings.MEDIA_ROOT + "\generated_docx\generated_doc_.docx"
            doc.save(name)
            msg.attach_file(name)
            msg.send()
            form.save()
    return render(request, 'order/new_order.html', {'form': form})


# def new_order(request):
#     form = OrderForm()
#     if request.method == "POST":
#         if form.is_valid():
#             pass

def register(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            editable = form.save(commit=False)
            username = request.POST.get("username").lower()
            # Send an email to the user with the token:
            mail_subject = 'Подтверждение справки для ' + username
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(request.user.pk))
            token = email_token.make_token(request.user)
            message = render_to_string('order/acc_active_email.html', {
                'user': request.user.username,
                'domain': current_site,
                'uid': uid,
                'token': token,
            })

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[editable.schools.get])
            email.content_subtype = "html"
            email.send()
            messages.success(request, 'Письмо в подтверждением отправлено на электронную почту!')
            return redirect('homepage')

    else:
        form = OrderForm()
    return render(request, 'order/register.html', {'form': form})