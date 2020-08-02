from django.db import models


class Result(models.Model):
    overall_analyser_result = models.FloatField(blank=True, null=True)
    overall_user_rating = models.FloatField(blank=True, null=True)
    overall_average_result = models.FloatField(blank=True, null=True)
    csv_file = models.FileField(upload_to='uploads/')
    is_ready = models.BooleanField(default=False)


class IndividualResult(models.Model):
    review = models.TextField(blank = True)
    user_rating = models.FloatField(blank=True, null=True)
    analyser_result = models.FloatField(blank=True, null=True)
    average_result = models.FloatField(blank=True, null=True)
    overall_result = models.ForeignKey(Result, on_delete=models.CASCADE, blank=True, null=True)









