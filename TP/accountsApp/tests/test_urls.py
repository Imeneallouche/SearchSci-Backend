from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accountsApp.views import AfficherModerateurs, SupprimerUser

# Class to test urls
class TestUrls(SimpleTestCase):
    def test_afficher_moderateurs_url_is_resolved(self):
        url = reverse('afficher_moderateurs')
        self.assertEqual(resolve(url).func, AfficherModerateurs)

    def test_supprimer_user_url_is_resolved(self):
        url = reverse('supprimer_user')
        self.assertEqual(resolve(url).func, SupprimerUser)


