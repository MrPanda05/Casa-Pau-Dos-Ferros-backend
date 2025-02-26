from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from .views import *
from backend.views import *
from .models import User

factory = APIRequestFactory()
# user = User.objects.get(username="test")
view_cart = CartViewSet.as_view({'get': 'list', 'post': 'create'})
view_prd = ProductViewSet.as_view({'get': 'list', 'post': 'create'})
class TestHelloWorld(TestCase):

    def testConfirmCart(self):
        # Criar usuário para o teste
        request = factory.post('/staff', {'username': 'test', 'password': 'test', 'email': 'test@dummy.com', 'full_name': 'Test Dummy', 'birth_date': '2000-01-01', 'cpf': '12345678901'})
        response = user_register(request)
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='test')
        # Criar itens no carrinho
        request1 = factory.post('/cart_item/', {'product_id': 1, 'quantity': 5})
        request1.user = user
        response1 = view_cart(request1)
        self.assertEqual(response1.status_code, 201)
        # Confirmando carrinho
        request2 = factory.get('/cart_item/')
        request2.user = user
        response2 = getProductInCart(request2)
        self.assertEqual(response2.status_code, 200)

    def testCartDevolution(self):
        # Criar usuário para o teste
        request = factory.post('/staff', {'username': 'test', 'password': 'test', 'email': 'test@dummy.com', 'full_name': 'Test Dummy', 'birth_date': '2000-01-01', 'cpf': '12345678901'})
        response = user_register(request)
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='test')
        # Criar itens no carrinho
        request1 = factory.post('/cart_item/', {'product_id': 1, 'quantity': 5})
        request1.user = user
        response1 = view_cart(request1)
        self.assertEqual(response1.status_code, 201)
        # Confirmando carrinho
        request2 = factory.get('/cart_item/')
        request2.user = user
        response2 = getProductInCart(request2)
        self.assertEqual(response2.status_code, 200)