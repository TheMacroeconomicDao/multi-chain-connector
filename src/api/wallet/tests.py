from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api.wallet.models import Wallet
from api.wallet.serializers import WalletSerializer


class WalletTests(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.user_test1 = User.objects.create_user(username="TestUser1", password="1q2w3e")
        self.user_test1.save()

        wallets = [
            Wallet(
                user_id=self.user_test1.id,
                address=f"TestAddress{i}",
                private_key="I-am-the-private-test-key!",
                public_key="I-am-the-public-test-key!",
            ) for i in range(10)
        ]

        Wallet.objects.bulk_create(wallets)

    def test_list(self) -> None:
        """
        Testcase LIST wallets
        """
        response = self.client.get("/api/v1/wallets/")
        serializer = WalletSerializer(
            Wallet.objects.filter(user_id=self.user_test1.id),
            many=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.json())

    def test_detail(self) -> None:
        """
        Testcase DETAIL wallet
        """
        response = self.client.get("/api/v1/wallets/1/")
        serializer = WalletSerializer(
            Wallet.objects.get(id=1)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.json())

    def test_post(self) -> None:
        """
        Testcase POST wallet
        """
        data = {
            "user_id": 1,
            "address": "TestAddress",
            "private_key": "I-am-the-private-test-key!",
            "public_key": "I-am-the-public-test-key!",
        }
        old_len_wallet = Wallet.objects.all().count()
        response = self.client.post("/api/v1/wallets/", data)

        self.assertEqual(Wallet.objects.all().count(), old_len_wallet + 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'status': 'success',
                'message': 'Wallet saved successfully.'
            }
        )

    def test_delete(self) -> None:
        """
        Testcase DELETE wallet
        """
        old_len_wallet = Wallet.objects.all().count()
        response = self.client.delete("/api/v1/wallets/2/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wallet.objects.all().count(), old_len_wallet - 1)
        self.assertEqual(Wallet.objects.filter(id=2).first(), None)

        response = self.client.get("/api/v1/wallets/2/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put(self) -> None:
        """
        Testcase PUT wallet
        """
        response = self.client.put("/api/v1/wallets/3/", {
            "user_id": 1,
            "address": "ChangedAdress",
            "private_key": "I-am-the-private-test-key-modifying!",
            "public_key": "I-am-the-public-test-key-modifying!",
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wallet.objects.get(id=3).address, "ChangedAdress")

    def test_patch(self) -> None:
        """
        Testcase PATCH wallet
        """
        response = self.client.patch(
            "/api/v1/wallets/5/",
            {
                "address": "Patched"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Wallet.objects.get(id=5).address, "Patched")
        self.assertEqual(Wallet.objects.get(id=5).id, 5)
