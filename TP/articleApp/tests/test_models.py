from django.test import TestCase
from articleApp.models import *

class TestModels(TestCase):
    

    def test_str_reference(self):
        reference = Reference.objects.create(
        titre = 'Reference'
        )
        self.assertEqual(str(reference), reference.titre)
    
    def test_traiter_article(self):
        article = Article.objects.create(
            titre = 'Titre',
            resume = 'Resume'
        )
        self.assertFalse(article.traiter)
    
     