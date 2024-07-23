from django.db import models

class AlgorithmParameters(models.Model):
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    area_size = models.FloatField()
    number_of_vehicles = models.IntegerField()
    number_of_points = models.IntegerField()
    # Adicione mais parâmetros conforme necessário
