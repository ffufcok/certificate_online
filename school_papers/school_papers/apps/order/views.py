from datetime import datetime
from docxtpl import DocxTemplate
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Schools
from django.contrib.sites.shortcuts import get_current_site
from .tokens import email_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def homepage(request):
    return render(request, 'order/main.html', {})


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

            # getting school email and name in English by its name from ChoiceField
            current_school = form.cleaned_data.get('schools')

            to_email_queryset = Schools.objects.filter(name=current_school).values('email').get()
            to_email_queryset_string = str(to_email_queryset)
            to_email_string = to_email_queryset_string[
                              to_email_queryset_string.find(':') + 3:to_email_queryset_string.rfind('}') - 1]

            english_name_queryset = Schools.objects.filter(name=current_school).values('name_in_english').get()
            english_name_queryset_string = str(english_name_queryset)
            english_name_string = english_name_queryset_string[
                                  english_name_queryset_string.find(':') + 3:english_name_queryset_string.rfind(
                                      '}') - 1]

            # sending confirmation email to school secretary

            email = EmailMessage(mail_subject, message, to=[to_email_string])
            email.content_subtype = "html"
            email.send()

            # creating document for current request and saving it locally

            template_path = settings.MEDIA_ROOT + '\doc_template\school_' + english_name_string + '.docx'
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
            messages.success(request, 'Заявка отправлена на рассмотрение секртарю!')
            return redirect('homepage')
    return render(request, 'order/new_order.html', {'form': form})


def confirm(request, token, user_email):
    try:
        name = settings.MEDIA_ROOT + '\generated_docx\generated_doc_' + str(token) + '.docx'
        message = render_to_string('order/confirmed_document.html')
        email = EmailMessage('Заявка на справку одобрена!', message,
                             to=[user_email])
        email.content_subtype = "html"
        email.attach_file(name)
        email.send()
        messages.success(request, 'Справка успешно одобрена!')
        return redirect("homepage")
    except FileNotFoundError:
        return HttpResponse('Ссылка недействительна!')


def decline(request, token, user_email):
    current_site = get_current_site(request)
    message = 'Заявка на получение справки на ' + str(
        current_site) + ' отклонена. Проверте правильность введённых данных' \
                        ' и попробуте снова'
    email = EmailMessage('Заявка на справку отклонена', message,
                         to=[user_email])
    email.content_subtype = "html"
    email.send()
    messages.success(request, 'Справка успешно отклонена!')
    return redirect("homepage")
