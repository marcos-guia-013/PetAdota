from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("animais/categoria/<str:nome_categoria>/", views.lista_categoria, name="lista_categoria"),
    path("animais/", views.ListarAnimais.as_view(), name="listar_animais"),
    path("animais/cadastrar/", views.CriarAnimal.as_view(), name="cadastro_animal"),
    path("animais/<int:pk>/", views.detalhes_animal_view, name="detalhes_animal"),
    path("animais/<int:pk>/atualizar/", views.AtualizarAnimal.as_view(), name="atualizar_animal"),
    path("animais/<int:pk>/excluir/", views.DeletarAnimal.as_view(), name="deletar_animal"),
    path("usuarios/cadastrar/", views.CadastrarUsuario.as_view(), name="cadastrar_usuario"),
    path("usuarios/<int:pk>/atualizar/", views.AtualizarUsuario.as_view(), name="atualizar_usuario"),
    path("ofertas/", views.ListarOfertas.as_view(), name="listar_ofertas"),
    path("ofertas/cadastrar/", views.CriarOferta.as_view(), name="criar_oferta"),
    path("ofertas/<int:pk>/", views.DetalhesOferta.as_view(), name="detalhes_oferta"),
    path("ofertas/<int:pk>/atualizar/", views.AtualizarOferta.as_view(), name="atualizar_oferta"),
    path("pedidos/", views.ListarPedidos.as_view(), name="listar_pedidos"),
    path("pedidos/cadastrar/", views.CriarPedido.as_view(), name="criar_pedido"),
    path("pedidos/<int:pk>/", views.DetalhesPedido.as_view(), name="detalhes_pedido"),
    path("pedidos/<int:pk>/atualizar/", views.AtualizarPedido.as_view(), name="atualizar_pedido"),
    path("pedidos/doador/<int:usuario_id>/", views.ListarPedidos.as_view(), name="listar_pedidos_doador"),
]