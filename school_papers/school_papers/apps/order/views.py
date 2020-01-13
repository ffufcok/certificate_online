from django.shortcuts import render
from django.core.mail import EmailMessage
from .forms import OrderForm
from django.utils import timezone
from docxtpl import DocxTemplate


def homepage(request):
    return render(request, 'order/main.html', {})


def new_order(request):
    form = OrderForm()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            editable = form.save(commit=False)
            editable.date = timezone.now()
            # doc = DocxTemplate('static/docs/d.docx')
            # context = {'number': editable.id, 'surname': editable.surname, 'name': editable.name,
            #            'father': editable.father, 'class': editable.class_letter}
            # doc.render(context)
            msg = EmailMessage('Справка', 'Справка с места учёбы', 'tol063115@gmail.com', [editable.email])
            msg.content_subtype = "html"
            # msg.attach_file(doc)
            msg.send()
            form.save()
    return render(request, 'order/new_order.html', {'form': form})
