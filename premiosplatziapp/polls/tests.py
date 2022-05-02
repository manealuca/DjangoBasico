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



def create_question(question_text,days):
    """
    Create a question with the given "question_text" and published the given 
    number of days offset to now (negative for published in the past, positive
    for questions that have yet to be published)
    """
    time = timezone.now() +datetime.timedelta(days = days)
    return Question.objects.create(question_text = question_text,pub_date = time)


class QuestionsIndexViewTests(TestCase):
    def test_no_questions(self):
        """if no question exist, an appropiate message is desplayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_future_question(self):
        """Questions with a pub_date in the future anren  t displayed on the index page"""
        create_question("Future question",days = 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response,"No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_past_question(self):
        """Question with a pub_date in the past are displayed in the index page"""
        question = create_question("past question",days =-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question])

    def test_future_question_and_past_question(self,):
        """Even if both past and future question exist, only past question are displayed"""
        past_question = create_question(question_text = "Past question",days =-30)
        future_question = create_question(question_text = "future question",days =30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],[past_question]
        )

    def test_two_past_question(self):
        """The questions index page may display multiple questions"""
        past_question1 = create_question(question_text = "Past question1",days =-1)
        past_question2 = create_question(question_text = "past question2",days =-20)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[past_question1,past_question2])

    def test_two_future_questions(self):
        """The questions with a pub date in  the future arent displayed on the index page"""
        future_question1 = create_question(question_text = "future question1",days =30)
        future_question2 = create_question(question_text = "future question2",days =20)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response,"No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],
        []
        )



    class QuestionDetailViewTests(TestCase):
        def test_future_question(self):
            """The detail view of  a question with a public i the futyre returns a 404 error not found"""
            future_question = create_question(question_text = "future question",days =30)
            url = reverse("polls;detail",args=(future_question.pk,))
            response = self.client.get(url)
            self.assertEqual(response.status_code,404)
                        
        def test_past_question(self):
            """The detail view of a question with a pub_date in the past displays the questions text"""
            past_question = create_question(question_text = "past question",days =30)
            url = reverse("polls:detail",args=(past_question.pk,))
            response = self.client.get(url)
            self.assertContains(response,past_question.question_text)

        def test_question_has_answers(self):
            question  = Question(qeustion_text = "test",pub_date = timezone.now()) 
            with self.assertRaises(Exception):
                    question.save() 



