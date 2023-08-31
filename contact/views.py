import asyncio

from django.shortcuts import render
from .models import Contact
from .forms import ContactForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

NULL = asyncio.AbstractEventLoop()

@login_required
def index(request, letter = NULL):
    if letter != NULL:
        contacts = request.user.contact_set.all().filter(name__istartswith=letter)

    else:
        contacts = request.user.contact_set.all().filter(name__contains=request.GET.get('search',''))

    context = {
        'contacts': contacts,
    }
    return render(request, 'contact/index.html', context)

@login_required
def view(request, id):
    contact = Contact.objects.get(id=id)
    context = {
        'contact': contact
    }
    return render(request, 'contact/detail.html', context)

@login_required
def edit(request, id):
    contact = Contact.objects.get(id=id)
    if request.method == 'GET':
        form = ContactForm(instance=contact)
        context = {
            'form': form,
            'id': id
        }      
        return render(request, 'contact/edit.html', context)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, instance = contact)
        if form.is_valid():
            form.save()
            context = {
            'form': form,
            'id': id
        }  
        messages.success(request, 'Contacto actualizado')
        return render(request, 'contact/edit.html', context)
    

@login_required
def create(request):
        if request.method == 'GET':
            form = ContactForm()
            context = {
                'form': form
            }
            return render(request, 'contact/create.html', context)
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                contact = form.save(commit=False)
                contact.user = request.user
                contact.save()
                
            return redirect('contact')

@login_required
def delete(request, id):
    contact = Contact.objects.get(id=id)
    contact.delete()
    return redirect('contact')