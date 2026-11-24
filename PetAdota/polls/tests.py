from django.test import TestCase
from .forms import AnimalForm, UsuarioForm


class AnimalTest(TestCase):

    def test_cadastrar_animal(self):
        form = AnimalForm(data={
            "especie": "CAC",
            "porte": "M",
            "data_nasc": "2024-01-01",
            "descricao": "Cachorro para adoção",
            "foto": "https://exemplo.com/cachorro.jpg"
        })
        self.assertTrue(form.is_valid())
        animal = form.save()
        self.assertEqual(animal.especie, "CAC")

    def test_animal_sem_foto(self):
        form = AnimalForm(data={
            "especie": "GAT",
            "porte": "P",
            "data_nasc": "2025-01-01",
            "descricao": "Gato para adoção"
        })
        self.assertTrue(form.is_valid())


class UsuarioTest(TestCase):

    def test_usuario_valido(self):
        form = UsuarioForm(data={
            "cpf": "123.456.789-00",
            "nome": "Usuario Teste",
            "numero": "82999999999",
            "email": "teste@example.com"
        })
        self.assertTrue(form.is_valid())

    def test_cpf_invalido(self):
        form = UsuarioForm(data={
            "cpf": "123",
            "nome": "Usuario Teste",
            "numero": "82999999999",
            "email": "teste@example.com"
        })
        self.assertFalse(form.is_valid())

    def test_telefone_invalido(self):
        form = UsuarioForm(data={
            "cpf": "123.456.789-00",
            "nome": "Usuario Teste",
            "numero": "123",
            "email": "teste@example.com"
        })
        self.assertFalse(form.is_valid())