import sys
import os
from django.shortcuts import render
from django.core.mail import EmailMessage
from .forms import OrderForm
from django.utils import timezone
from datetime import datetime
from docxtpl import DocxTemplate
from docx import Document
from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Schools
from django.contrib.sites.shortcuts import get_current_site
from .tokens import email_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
import comtypes.client


def homepage(request):
    return render(request, 'order/main.html', {})


# def new_order(request):
#     email_autofill = request.user.email
#     form = OrderForm(initial={'email': email_autofill})
#     if request.method == "POST":
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             editable = form.save(commit=False)
#             doc = DocxTemplate("D:/Desktop/D_school_papers/school_papers/school_papers/doc_template/d.docx")
#             context = {'number': editable.id, 'surname': editable.surname, 'name': editable.name,
#                        'father': editable.father, 'class': editable.class_letter}
#             doc.render(context)
#             msg = EmailMessage('Справка', 'Справка с места учёбы', 'tol063115@gmail.com', [editable.email])
#             msg.content_subtype = "html"
#             name = settings.MEDIA_ROOT + "\generated_docx\generated_doc_.docx"
#             doc.save(name)
#             msg.attach_file(name)
#             msg.send()
#             form.save()
#     return render(request, 'order/new_order.html', {'form': form})


@login_required
def new_order(request):
    email_autofill = request.user.email
    form = OrderForm(initial={'email': email_autofill})
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            editable = form.save(commit=False)
            editable.date = datetime.now()
            editable.save()

            # Send an email to the user with the token:
            surname_headline = form.cleaned_data.get('surname')
            name_headline = surname_headline + ' ' + form.cleaned_data.get('name')
            father_headline = name_headline + ' ' + form.cleaned_data.get('father')
            mail_subject = 'Подтверждение справки для ' + father_headline
            current_site = get_current_site(request)
            token = email_token.make_token(request.user)
            message = render_to_string('order/confirm_order.html', {
                'surname': form.cleaned_data.get('surname'),
                'name': form.cleaned_data.get('name'),
                'father': form.cleaned_data.get('father'),
                'class_letter': form.cleaned_data.get('class_letter'),
                'domain': current_site,
                'token': token,
                'user_email': form.cleaned_data.get('email'),
            })

            # getting school email by its name from ChoiceField

            to_email_queryset = Schools.objects.filter(name=form.cleaned_data.get('schools')).values('email').get()
            to_email_queryset_string = str(to_email_queryset)
            to_email_string = to_email_queryset_string[
                              to_email_queryset_string.find(':') + 3:to_email_queryset_string.rfind('}') - 1]

            # sending confirmation eцвmail to school secretary

            email = EmailMessage(mail_subject, message, to=[to_email_string])
            email.content_subtype = "html"
            email.send()

            # creating document for current request and saving it locally

            template_path = settings.MEDIA_ROOT + '\doc_template\d.docx'
            doc = DocxTemplate(template_path)
            number_of_document = str(editable.pk).zfill(7)
            context = {'number': number_of_document, 'surname': form.cleaned_data.get('surname'),
                       'name': form.cleaned_data.get('name'),
                       'father': form.cleaned_data.get('father'), 'class': form.cleaned_data.get('class_letter'),
                       'date': datetime.today().strftime("%d.%m.%Y")}
            doc.render(context)
            name = settings.MEDIA_ROOT + '\generated_docx\generated_doc_' + str(token) + '.docx'
            doc.save(name)

            # convert docx to pdf

            # in_file = settings.MEDIA_ROOT + '\generated_docx\generated_doc_' + str(token)
            # out_file = settings.MEDIA_ROOT + '\generated_docx\generated_doc_' + str(token) + '1'
            #
            # word = comtypes.client.CreateObject('Word.Application')
            # docx = word.Documents.Open(in_file)
            # docx.SaveAs(out_file, FileFormat=17)
            # docx.Close()
            # word.Quit()

            form.save()
            return redirect('homepage')
    return render(request, 'order/new_order.html', {'form': form})


def confirm(request, token, user_email):
    name = settings.MEDIA_ROOT + '\generated_docx\generated_doc_' + str(token) + '.docx'
    email = EmailMessage('Поздравляем! Ваша справка одобрена!', 'Справка с мета учёбы одобрена секретарём',
                         to=[user_email])
    email.content_subtype = "html"
    email.attach_file(name)
    email.send()
    return redirect("homepage")
