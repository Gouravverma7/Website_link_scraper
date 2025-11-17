from django.shortcuts import render, redirect, HttpResponseRedirect
import requests
from bs4 import BeautifulSoup
from .models import Link

def scrape(request):
    if request.method == "POST":
        site = request.POST.get('site','')

        if site in ["", "http://", "https://"]:
            return HttpResponseRedirect("/")
        
        if not site.startswith("http://") and not site.startswith("http://"):
            site = "https://" + site 

        page = requests.get(site)
        soup = BeautifulSoup(page.text,'html.parser')

        for link in soup.find_all('a'):
            link_address = link.get('href')
            link_text = link.string
            Link.objects.create(address=link_address, name=link_text)
        return HttpResponseRedirect('/')
    else:
        data = Link.objects.all()
    
    return render(request, "scrape/result.html", {'data':data})


def delete(request):
    # data = get_object_or_404(Link)
    # data.delete()
    Link.objects.all().delete()
    return render(request, 'scrape/result.html')