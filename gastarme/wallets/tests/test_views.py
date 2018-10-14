from unittest.mock import patch

from django.urls import reverse
from rest_framework import test, status

from users.models import User
from wallets.models import Wallet


class TestUserView(test.APITransactionTestCase):
    """Test cases for the wallet view."""

    def setUp(self):
        self.user = User.objects.create(
            name='user',
            email='user@email.com',
        )

        self.superuser = User.objects.create(
            name='super',
            email='super@email.com',
            is_superuser=True
        )

    def test_user_resource_url(self):
        self.assertEqual(reverse('wallets-list'), '/v1/wallets/')
        self.assertEqual(reverse('wallets-detail', args=[1]), '/v1/wallets/1/')

    def test_superuser_resource_url(self):
        self.assertEqual(
            reverse('creditcards-list'),
            '/v1/wallets/creditcards/'
        )
        self.assertEqual(
            reverse('creditcards-detail', args=[1]),
            '/v1/wallets/creditcards/1/'
        )

    @patch('wallets.logger.info')
    def test_user_wallet_create(self, logger_mock):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse('wallets-list'),
        )
        logger_mock.assert_called()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.count(), 1)

    @patch('wallets.logger.info')
    def test_user_wallet_detail(self, logger_mock):
        wallet = Wallet.objects.create(user=self.user)
        self.client.force_authenticate(self.user)

        response = self.client.get(
            reverse('wallets-detail', args=[wallet.id]),
        )
        logger_mock.assert_called()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('wallets.logger.info')
    def test_superuser_wallet_list(self, logger_mock):
        Wallet.objects.create(user=self.user)
        self.client.force_authenticate(self.superuser)

        response = self.client.get(
            reverse('wallets-list'),
        )
        logger_mock.assert_called()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('wallets.logger.info')
    def test_superuser_wallet_delete(self, logger_mock):
        wallet = Wallet.objects.create(user=self.user)
        self.client.force_authenticate(self.superuser)

        response = self.client.delete(
            reverse('wallets-detail', args=[wallet.id]),
        )
        logger_mock.assert_called()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)