from django.test import TestCase
from .models import Player
from django.contrib.auth import get_user_model


class PlayerModelTestCase(TestCase):
    def test_create_player(self):
        """Test player creation"""
        player = Player.objects.create_user(username="newplayer", password="pass123")
        self.assertEqual(player.username, "newplayer")
        self.assertEqual(player.games_played, 0)
        self.assertEqual(player.games_won, 0)
        self.assertEqual(player.games_drawn, 0)

    def test_player_str(self):
        """Test player string representation"""
        player = Player.objects.create_user(username="testplayer", password="pass123")
        self.assertEqual(str(player), "testplayer")


class PlayerManagerTestCase(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="normal_user", password="foo")
        self.assertEqual(user.username, "normal_user")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            self.assertIsNone(user.email)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(username="")
        with self.assertRaises(ValueError):
            User.objects.create_user(username="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser("admin", "foo")
        self.assertEqual(user.username, "admin")
        self.assertTrue(user.is_active, True)
        self.assertTrue(user.is_staff, True)
        self.assertTrue(user.is_superuser, True)

        try:
            self.assertIsNone(user.email)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_superuser()
        with self.assertRaises(TypeError):
            User.objects.create_superuser(username="")
        with self.assertRaises(ValueError):
            User.objects.create_superuser(username="", password="foo")
