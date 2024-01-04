from django.db import models

# Create your models here.

# Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

# Car Model model
class CarModel(models.Model):
    CAR_TYPES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('wagon', 'Wagon'),
        ('truck', 'Truck')
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='car_models')
    name = models.CharField(max_length=255)
    dealer_id = models.CharField(max_length=50)  # Assuming dealer_id is a string, adjust as needed
    car_type = models.CharField(max_length=10, choices=CAR_TYPES)
    year = models.DateField()

    def __str__(self):
        return f"{self.car_make} - {self.name}"

# Plain Python class CarDealer
class CarDealer:
    # Add fields/methods as needed
    pass

# Plain Python class DealerReview
class DealerReview:
    # Add fields/methods as needed
    pass
