from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from .views import *
from backend.views import *
from .models import User

factory = APIRequestFactory()
# user = User.objects.get(username="test")
view_cart = CartViewSet.as_view({'get': 'list', 'post': 'create'})
view_prd = ProductViewSet.as_view({'get': 'list', 'post': 'create'})
class Test(TestCase):

    def testConfirmCart(self):
        # Criar usuário para o teste
        request = factory.post('/staff', {'username': 'test', 'password': 'test', 'email': 'test@dummy.com', 'full_name': 'Test Dummy', 'birth_date': '2000-01-01', 'cpf': '12345678901'})
        response = user_register(request)
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='test')
        # Criar endereço do usuário para o teste
        request = factory.post('/address/', {'cep': '12345678', 'state': 'SP', 'city': 'São Paulo', 'street': 'Rua Teste', 'number': '123'})
        request.user = user
        response = user_add_address(request)
        self.assertEqual(response.status_code, 201)
        # Criar itens no carrinho
        request = factory.post('/cart_item/', {'product_id': 1, 'quantity': 5})
        request.user = user
        response = view_cart(request)
        self.assertEqual(response.status_code, 201)
        # Confirmando carrinho
        request = factory.post('/confirm/', {'payment_method': 'credit', 'user_address': 1})
        request.user = user
        response = confirmCart(request)
        self.assertEqual(response.status_code, 200)

    def testCartDevolution(self):
        # Criar usuário para o teste
        request = factory.post('/staff', {'username': 'test', 'password': 'test', 'email': 'test@dummy.com', 'full_name': 'Test Dummy', 'birth_date': '2000-01-01', 'cpf': '12345678901'})
        response = user_register(request)
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='test')
        # Criar endereço do usuário para o teste
        request = factory.post('/address/', {'cep': '12345678', 'state': 'SP', 'city': 'São Paulo', 'street': 'Rua Teste', 'number': '123'})
        request.user = user
        response = user_add_address(request)
        self.assertEqual(response.status_code, 201)
        # Criar itens no carrinho
        request = factory.post('/cart_item/', {'product_id': 1, 'quantity': 5})
        request.user = user
        response = view_cart(request)
        self.assertEqual(response.status_code, 201)
        # Confirmando carrinho
        request = factory.post('/confirm/', {'payment_method': 'credit', 'user_address': 1})
        request.user = user
        response = confirmCart(request)
        self.assertEqual(response.status_code, 200)
        # Devolução do carrinho
        request = factory.post('/devolution/', {'order_id': 1})
        request.user = user
        request = orderDevolution(request)
        self.assertEqual(response.status_code, 200)