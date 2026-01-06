from django.db import models

class Wine(models.Model):
    WINE_TYPES = (('red', 'Red'), ('white', 'White'))
    
    type = models.CharField(max_length=5, choices=WINE_TYPES)
    fixed_acidity = models.FloatField()
    volatile_acidity = models.FloatField()
    citric_acid = models.FloatField()
    residual_sugar = models.FloatField()
    chlorides = models.FloatField()
    free_sulfur_dioxide = models.FloatField()
    total_sulfur_dioxide = models.FloatField()
    density = models.FloatField()
    pH = models.FloatField()
    sulphates = models.FloatField()
    alcohol = models.FloatField()
    quality = models.IntegerField()

    def __str__(self):
        return f"{self.type.capitalize()} Wine - Quality {self.quality}"