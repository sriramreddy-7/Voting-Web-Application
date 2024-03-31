from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
    name = models.CharField(max_length=100)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    id_number = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    id_proof = models.ImageField(upload_to='id_proofs/', blank=True, null=True)

    def __str__(self):
        return self.name

class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    aadhar_number = models.CharField(max_length=16, unique=True, null=True)
    role = models.CharField(max_length=100)
    id_number = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    id_proof = models.ImageField(upload_to='voter_id_proofs/', blank=True, null=True)

    def __str__(self):
        return self.user.username
