from django.shortcuts import render
from .dl_model.predict import predict
from django.http import HttpResponse
from .models import Result, IndividualResult
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import urllib, base64
from .task import bulk_sentiment_analyser

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
            return render(request, 'upload_successful.html', {'result_id':result_obj.id})
        except:
            return HttpResponse("file format not supported")
        return HttpResponse("file not uploaded")
    return render(request, 'bulk_review_upload.html', {})

def BulkAnalyserResultView(request):
    if 'result_id' in request.GET:
        result_obj = Result.objects.get(id=request.GET.get('result_id'))
        if(result_obj.is_ready):
            individual_results = IndividualResult.objects.filter(overall_result=result_obj)
            analyser_results = list(individual_results.values_list('analyser_result', flat=True))
            average_results = list(individual_results.values_list('average_result', flat=True))
            analyser_graph = BarPlot(analyser_results)
            average_gaph = BarPlot(average_results)
            result_dic = {
                'overall_average_rating': result_obj.overall_average_result,
                'overall_user_rating': result_obj.overall_user_rating,
                'overall_analyser_rating': result_obj.overall_analyser_result,
                'individual_result': individual_results,
                'analyser_graph': analyser_graph,
                'average_graph': average_gaph
            }
            return render(request, 'bulk_result.html', result_dic)
        return render(request, 'please_wait.html', {'result_id':result_obj.id})
    return render(request,  'get_bulk_result.html', {})


def BarPlot(X:list)->None:
    for i in range(len(X)):
        X[i]=round(X[i])
    df = pd.DataFrame({'Rating':X})
    sns.catplot(x='Rating', kind='count', data=df)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    prg_url = urllib.parse.quote(string)
    plt.close()
    return prg_url

