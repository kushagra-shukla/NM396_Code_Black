from django.shortcuts import render
from .dl_model.predict import predict
from django.http import HttpResponse
from .models import Result, IndividualResult
import pandas as pd
import numpy as np
<<<<<<< HEAD
import matplotlib.pyplot as plt
from .task import bulk_sentiment_analyser
=======
#import matplotlib.pyplot as plt
>>>>>>> f4d6940a708093a663010d26b9513dab96ac4b5d

# Create your views here.

def sentimentAnalyserView(request):
    if request.method  == 'POST':
        sentences = []
        sentences.append(request.POST.get('sentence'))
        rating = predict(sentences)
        results = [
            ["I really like the Bhuvan portal.", "User rating 5", "Average rating 4"],
            ["Detailing of India's 2D map are great but its Zoom feature can be improved.", "User rating 3.5", "Average rating 3"],
            ["I am unable to login my account on bhuvan", "User rating 1", "Average rating 1"],
            ["Another great portal by goverment of India and ISRO", "User rating 3.5", "Average rating 4"]
        ]
        return render(request, 'result.html', {'sentence': sentences[0], 'rating': rating, 'results': results})
    return render(request, 'home.html', {})


def BulkAnalyserView(request):
    if request.method == 'POST':
        print("got request")
        try:
            file = request.FILES['file']
            result_obj = Result.objects.create(csv_file=file)
            bulk_sentiment_analyser.delay(result_obj.id)           
            return render(request, 'upload_success.html', {'result_id':result_obj.id})
        except:
            return HttpResponse("file format not supported")
        return HttpResponse("file not uploaded")
    return render(request, 'bulk_review_upload.html', {})

def BulkAnalyserResultView(request):
    if 'result_id' in request.GET:
        result_obj = Result.objects.get(id=request.GET.get('result_id'))
        if(result_obj.is_ready):
            return render(request, 'bulk_result.html', {})
        return render(request, 'please_wait.html', {'result_id':result_obj.id})
    return render(request,  'get_bulk_result.html', {})



