from django.shortcuts import render
from .models import *

# Create your views here.
def index_ges(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        college = request.POST['college']
        participant = ges_Participant.objects.create(name=name, email=email, college=college)
        participant.save()
    return render(request, 'GES/index.html')
