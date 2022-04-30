from django.db import models


class Question(models.Model):
    #django automaticamente nos crea un id por eso no lo generamos nosotros
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField("date published")



class Choise(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choise_text = models.CharField(max_length=100)
    votes = models.IntegerField(default = 0)



