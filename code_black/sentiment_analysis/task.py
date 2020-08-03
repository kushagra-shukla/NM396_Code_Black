from celery import shared_task
from .models import Result, IndividualResult
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .dl_model.predict import predict

@shared_task(name="bulk_sentiment_analyser")
def bulk_sentiment_analyser(result_id):
    result_obj = Result.objects.get(id=result_id) 
    reviews, user_ratings = bulk_analyser_reader(result_obj.csv_file)
    analyser_result = predict(reviews)
    total_analyser_rating = 0
    total_review_rating = 0
    reviews_count = len(reviews)

    for i in range(reviews_count):
        total_analyser_rating += analyser_result[i]
        total_review_rating += user_ratings[i]
        average_result = (analyser_result[i] + user_ratings[i])/2
        IndividualResult.objects.create( review=reviews[i],
                                          user_rating=user_ratings[i],
                                          analyser_result=analyser_result[i],
                                          average_result=average_result,
                                          overall_result=result_obj
                                          )
        result_obj.overall_analyser_result = total_analyser_rating/reviews_count
        result_obj.overall_user_rating = total_review_rating/reviews_count
        result_obj.overall_average_result = (result_obj.overall_analyser_result + result_obj.overall_user_rating)/2
        result_obj.is_ready = True
        result_obj.save()


def bulk_analyser_reader(file):
    dfx= pd.read_csv(file)
    file_values = dfx.values
    reviews = []
    user_ratings = []
    for review in file_values:
        reviews.append(str(review[0]))
        user_ratings.append(int(review[1]))
    # print(reviews)
    # print(user_ratings)
    return reviews, user_ratings
