from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, DetailView, DeleteView, UpdateView, FormView
from . import models

class ListarAnimais(ListView):
    model = models.Animal
    template_name = "animais/listar_animais.html"
    context_object_name = "animais"

    def get_queryset(self):
        queryset = self.model.objects.filter(adotado=False)
        especie = self.request.GET.get("especie")

        if especie:
            queryset = queryset.filter(especie=especie)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Titulo"] = "Animais em doação"
        return context

class CriarAnimal(CreateView):
    model = models.Animal
    fields = [
        "especie",
        "porte",
        "data_nasc",
        "descricao",
        "adotado"
    ]
    template_name = "animais/cadastro_animal.html"
    success_url = reverse_lazy("polls:listar_animais")

class DetalhesAnimal(DetailView):
    model = models.Animal
    context_object_name = "animal"
    template_name = "animais/detalhes_animal.html"

class AtualizarAnimal(UpdateView):

    model = models.Animal
    fields = [
        "especie",
        "porte",
        "data_nasc",
        "descricao",
        "adotado"
    ]
    template_name = "animais/atualizar_animal.html"
    success_url = reverse_lazy("polls:listar_animais")

class DeletarAnimal(DeleteView):
    model = models.Animal
    template_name = "animais/deletar_animal.html"
    success_url = reverse_lazy("polls:listar_animais")

class CadastrarUsuario(CreateView):
    model = models.Usuario
    fields = ["cpf", "nome", "numero", "email"]
    template_name = "usuarios/cadastro_usuario.html"
    success_url = reverse_lazy("polls:cadastrar_usuario")

class AtualizarUsuario(UpdateView):
    model = models.Usuario
    fields = ["cpf", "nome", "numero", "email"]
    template_name = "usuarios/atualizar_usuario.html"
    success_url = reverse_lazy("polls:listar_ofertas")

class ListarOfertas(ListView):
    model = models.OfertaDoacao
    template_name = "ofertas/listar_ofertas.html"
    context_object_name = "ofertas"

    def get_queryset(self):
        status= self.request.GET.get("status")
        if status:
            return self.model.objects.filter(status=status)
        
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Titulo"] = "OFERTAS DE DOAÇÃO"
        return context

class CriarOferta(CreateView):
    model = models.OfertaDoacao
    fields = [  
        "doador",
        "animal",
        "endereco",
        "descricao",
        "status",
    ]
    template_name = "ofertas/cadastro_oferta.html"
    success_url = reverse_lazy("polls:criar_oferta")

class DetalhesOferta(DetailView):
    model = models.OfertaDoacao
    context_object_name = "oferta"
    template_name = "ofertas/detalhes_oferta.html"

class AtualizarOferta(UpdateView):

    model = models.OfertaDoacao
    fields = [  
        "doador",
        "animal",
        "endereco",
        "descricao",
        "status",
    ]
    template_name = "ofertas/atualizar_oferta.html"
    success_url = reverse_lazy("polls:listar_ofertas")

class ListarPedidos(ListView):
    model = models.PedidoDoacao
    template_name = "pedidos/listar_pedido.html"
    context_object_name = "pedidos"
    def get_queryset(self):
        usuario_id = self.kwargs.get("usuario_id")

        if usuario_id:
            return self.model.objects.filter(
                id_ofertaDoacao__doador__id_usuario=usuario_id
            )

        return self.model.objects.all()

class CriarPedido(CreateView):
    model = models.PedidoDoacao

    fields = [
        "id_ofertaDoacao",
        "id_usuario",
        "status_pedido",
    ]

    template_name = "pedidos/criar_pedido.html"
    success_url = reverse_lazy("polls:criar_pedido")

class DetalhesPedido(DetailView):
    model = models.PedidoDoacao
    context_object_name = "pedido"
    template_name = "pedidos/detalhes_peidido.html"

class AtualizarPedido(UpdateView):

    model = models.PedidoDoacao
    fields = [  
        "id_ofertaDoacao",
        "id_usuario",
        "status_pedido",
    ]
    template_name = "pedidos/atualizar_pedido.html"
    success_url = reverse_lazy("polls:listar_pedidos")

def home_view(request):
    return redirect("polls:listar_ofertas")

def detalhes_animal_view(request, pk):
    animal = get_object_or_404(models.Animal, pk=pk)
    contexto = {"animal": animal}
    return render(request, "animais/detalhes_animal.html", contexto)

def lista_categoria(request, nome_categoria):
    if nome_categoria == "gato":
        codigo = "GAT"
    elif nome_categoria == "cachorro":
        codigo = "CAC"
    elif nome_categoria == "outro":
        codigo = "OUT"
    else:
        codigo = ""

    animais = models.Animal.objects.filter(especie=codigo, adotado=False)
    contexto = {"lista_itens": animais, "categoria": nome_categoria}
    return render(request, "animais/lista_categoria.html", contexto)
