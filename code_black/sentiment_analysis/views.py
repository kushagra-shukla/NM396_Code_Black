from django.shortcuts import render
from .dl_model.predict import predict
from django.http import HttpResponse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
            print(file)
            reviews, user_ratings = bulk_analyser_reader(file)
            return render(request, 'result.html', {})
        except:
            return HttpResponse("file format not supported")
        return HttpResponse("file not uploaded")
    return render(request, 'bulk_review_upload.html', {})

def bulk_analyser_reader(file):
    dfx= pd.read_csv(file)
    file_values = dfx.values
    reviews = []
    user_ratings = []
    for review in file_values:
        reviews.append(review[0])
        user_ratings.append(int(review[1]))
    # print(reviews)
    # print(user_ratings)
    return reviews, user_ratings