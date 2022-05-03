from django.db import models
from django.utils import timezone
import datetime

class Question(models.Model):
    #django automaticamente nos crea un id por eso no lo generamos nosotros
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField("date published")

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        if(self.choise_set.all().count == 0):
            super().delete()
            raise Exeption("Question must have at least once choice")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now()-datetime.timedelta(days=1)



class Choise(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choise_text = models.CharField(max_length=100)
    votes = models.IntegerField(default = 0)

    def __str__(self):
        return self.choise_text

