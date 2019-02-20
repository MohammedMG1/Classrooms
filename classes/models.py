from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Classroom(models.Model):
	name = models.CharField(max_length=120)
	subject = models.CharField(max_length=120)
	year = models.IntegerField()
	teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classroom')

	def get_absolute_url(self):
		return reverse('classroom-detail', kwargs={'classroom_id':self.id})


	
gender_options =(
		('Male', 'Male'),
		('Female', 'female')
	)
class Student(models.Model):
	name = models.CharField(max_length=120)
	date_of_birth = models.DateField()
	gender = models.CharField(max_length=6, choices=gender_options)
	exam_grade = models.FloatField()
	classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='students')




