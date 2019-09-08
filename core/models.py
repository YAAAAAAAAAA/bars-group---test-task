from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_init


class Planet(models.Model):
    name = models.CharField(max_length=255, primary_key=True)


class Recruit(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField()
    email = models.EmailField(primary_key=True)
    planet_habitat = models.ForeignKey(Planet, on_delete=models.CASCADE)


class Sith(models.Model):
    name = models.CharField(max_length=255)
    planet_of_learning = models.ForeignKey(Planet, on_delete=models.CASCADE)


class TestTrials(models.Model):
    orden_code = models.CharField(max_length=255, primary_key=True)


class Questions(models.Model):
    question = models.TextField()
    test_trial = models.ForeignKey(TestTrials, on_delete=models.CASCADE)


class Answers(models.Model):
    recruit = models.ManyToManyField(Recruit, related_name='answers')
    quest = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='answers')
    answer = models.BooleanField(default=False)


class DiscipleTeacher(models.Model):
    disciple = models.OneToOneField(Recruit, on_delete=models.CASCADE, related_name='teacher')
    teacher = models.ForeignKey(Sith, on_delete=models.CASCADE, related_name='disciples')