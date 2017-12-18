from django.shortcuts import render
from bug.models import *
from bug.forms import TicketForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render


def ticket_crear(request):   
    form = TicketForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.propietario = request.user 
        instance.save()
        return HttpResponseRedirect('/')
    context = {
        "form": form
    }
    return render(request, "ticket.html", context)


def ver_incidencias(request):   
    misticket = Ticket.objects.filter(propietario=request.user).order_by("-creado_el")
    context = {
        "misticket":misticket,
    }
    return render(request, "misticket.html", context)
