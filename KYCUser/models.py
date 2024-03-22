from django.db import models
from django.core.validators import RegexValidator, EmailValidator, MinValueValidator

class KYCUsers(models.Model):
    user_id = models.CharField(max_length=20, primary_key = True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    ])
    email = models.EmailField(max_length=255, validators=[EmailValidator()])
    address = models.TextField()
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10, validators=[
        RegexValidator(regex=r'^\d{5}$', message="Zip code must be 5 digits.")
    ])
    occupation = models.CharField(max_length=255)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    email_before_update = models.EmailField(max_length=255, blank=True, null=True)
    phone_number_before_update = models.CharField(max_length=15, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.pk:
            # Check if email or phone number has changed
            orig = KYCUsers.objects.get(pk=self.pk)
            if self.email != orig.email:
                self.email_before_update = orig.email
            if self.phone_number != orig.phone_number:
                self.phone_number_before_update = orig.phone_number
        super(KYCUsers, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
