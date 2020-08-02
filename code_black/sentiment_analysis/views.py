from django.shortcuts import render
from .DLmodel.predict import predict

# Create your views here.

def uploadView(request):
    if request.method  == 'POST':
        sentence = request.POST.get('sentence')
        rating = predict(sentence)
        results = [
            ["I really like the Bhuvan portal.", "User rating 5", "Average rating 4"],
            ["Detailing of India's 2D map are great but its Zoom feature can be improved.", "User rating 3.5", "Average rating 3"],
            ["I am unable to login my account on bhuvan", "User rating 1", "Average rating 1"],
            ["Another great portal by goverment of India and ISRO", "User rating 3.5", "Average rating 4"]
        ]
        return render(request, 'result.html', {'sentence': sentence, 'rating': rating, 'results': results})
    return render(request, 'home.html', {})
