from django.test import TestCase
from django.utils import timezone
from .models import Question
import datetime
from django.urls.base import reverse

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """was_published_recently return False questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question  = Question(question_text = "Quien es el mejor Course Director de Platzi",pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)


class QuestionsIndexViewTests(TestCase):
    def test_no_questions(self):
        """if no question exist, an appropiate message is desplayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])



    