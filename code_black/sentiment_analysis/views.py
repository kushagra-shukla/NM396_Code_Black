from django.shortcuts import render

# Create your views here.

def uploadView(request):
    if request.method  == 'POST':
        return render(request, 'result.html', {})
    return render(request, 'home.html', {})
