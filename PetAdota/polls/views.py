
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, DetailView, DeleteView, UpdateView, FormView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from . import models
from .forms import AnimalForm, UsuarioForm, OfertaDoacaoForm, PedidoDoacaoForm, CadastroForm, AtualizarPedidoForm


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


class CriarAnimal(LoginRequiredMixin, CreateView):
    model = models.Animal
    form_class = AnimalForm
    template_name = "animais/cadastro_animal.html"
    success_url = reverse_lazy("polls:listar_animais")

    def form_valid(self, form):
        form.instance.responsavel = get_object_or_404(
            models.Usuario, conta=self.request.user
        )
        return super().form_valid(form)


class DetalhesAnimal(DetailView):
    model = models.Animal
    context_object_name = "animal"
    template_name = "animais/detalhes_animal.html"


class AtualizarAnimal(LoginRequiredMixin, UpdateView):
    model = models.Animal
    form_class = AnimalForm
    template_name = "animais/atualizar_animal.html"
    success_url = reverse_lazy("polls:listar_animais")

    def get_queryset(self):
        return models.Animal.objects.filter(
            responsavel__conta=self.request.user
        )


class DeletarAnimal(LoginRequiredMixin, DeleteView):
    model = models.Animal
    template_name = "animais/deletar_animal.html"
    success_url = reverse_lazy("polls:listar_animais")

    def get_queryset(self):
        return models.Animal.objects.filter(
            responsavel__conta=self.request.user
        ).exclude(ofertadoacao__isnull=False)


class CadastrarUsuario(TemplateView):

    def get(self, request):
        return redirect("polls:cadastro")

    def post(self, request):
        return redirect("polls:cadastro")


class AtualizarUsuario(LoginRequiredMixin, UpdateView):
    model = models.Usuario
    form_class = UsuarioForm
    template_name = "usuarios/atualizar_usuario.html"
    success_url = reverse_lazy("polls:listar_ofertas")

    def get_queryset(self):
        return models.Usuario.objects.filter(
            conta=self.request.user
        )


class ListarOfertas(ListView):
    model = models.OfertaDoacao
    template_name = "ofertas/listar_ofertas.html"
    context_object_name = "ofertas"

    def get_queryset(self):
        status = self.request.GET.get("status")
        if status:
            return self.model.objects.filter(status=status)
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Titulo"] = "OFERTAS DE DOAÇÃO"
        return context


class CriarOferta(LoginRequiredMixin, CreateView):
    model = models.OfertaDoacao
    form_class = OfertaDoacaoForm
    template_name = "ofertas/cadastro_oferta.html"
    success_url = reverse_lazy("polls:criar_oferta")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["animal"].queryset = models.Animal.objects.filter(
            responsavel__conta=self.request.user,
            adotado=False
        ).exclude(ofertadoacao__isnull=False)
        return form

    def form_valid(self, form):
        form.instance.doador = get_object_or_404(
            models.Usuario, conta=self.request.user
        )
        return super().form_valid(form)


class DetalhesOferta(DetailView):
    model = models.OfertaDoacao
    context_object_name = "oferta"
    template_name = "ofertas/detalhes_oferta.html"


class AtualizarOferta(LoginRequiredMixin, UpdateView):
    model = models.OfertaDoacao
    form_class = OfertaDoacaoForm
    template_name = "ofertas/atualizar_oferta.html"
    success_url = reverse_lazy("polls:listar_ofertas")

    def get_queryset(self):
        return models.OfertaDoacao.objects.filter(
            doador__conta=self.request.user
        )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["animal"].disabled = True
        return form


class ListarPedidos(LoginRequiredMixin, ListView):
    model = models.PedidoDoacao
    template_name = "pedidos/listar_pedido.html"
    context_object_name = "pedidos"

    def get_queryset(self):
        queryset = models.PedidoDoacao.objects.filter(
            Q(id_usuario__conta=self.request.user) |
            Q(id_ofertaDoacao__doador__conta=self.request.user)
        )

        usuario_id = self.kwargs.get("usuario_id")

        if usuario_id:
            queryset = queryset.filter(
                id_ofertaDoacao__doador__id_usuario=usuario_id
            )

        return queryset


class CriarPedido(LoginRequiredMixin, CreateView):
    model = models.PedidoDoacao
    form_class = PedidoDoacaoForm
    template_name = "pedidos/criar_pedido.html"
    success_url = reverse_lazy("polls:listar_pedidos")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["id_ofertaDoacao"].queryset = (
            models.OfertaDoacao.objects.filter(
                status="DIS",
                animal__adotado=False
            ).exclude(doador__conta=self.request.user)
        )
        return form

    def form_valid(self, form):
        usuario = get_object_or_404(
            models.Usuario, conta=self.request.user
        )

        oferta = form.cleaned_data["id_ofertaDoacao"]

        if models.PedidoDoacao.objects.filter(
            id_usuario=usuario,
            id_ofertaDoacao=oferta
        ).exists():
            form.add_error("id_ofertaDoacao", "Você já solicitou esta adoção.")
            return self.form_invalid(form)

        form.instance.id_usuario = usuario
        return super().form_valid(form)


class DetalhesPedido(LoginRequiredMixin, DetailView):
    model = models.PedidoDoacao
    context_object_name = "pedido"
    template_name = "pedidos/detalhes_peidido.html"

    def get_queryset(self):
        return models.PedidoDoacao.objects.filter(
            Q(id_usuario__conta=self.request.user) |
            Q(id_ofertaDoacao__doador__conta=self.request.user)
        )


class AtualizarPedido(LoginRequiredMixin, UpdateView):
    model = models.PedidoDoacao
    form_class = AtualizarPedidoForm
    template_name = "pedidos/atualizar_pedido.html"
    success_url = reverse_lazy("polls:listar_pedidos")

    def get_queryset(self):
        return models.PedidoDoacao.objects.filter(
            id_ofertaDoacao__doador__conta=self.request.user
        )


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

    animais = models.Animal.objects.filter(
        especie=codigo, adotado=False
    )
    contexto = {
        "lista_itens": animais,
        "categoria": nome_categoria
    }
    return render(request, "animais/lista_categoria.html", contexto)


def cadastrar_conta(request):
    if request.user.is_authenticated:
        return redirect("polls:listar_ofertas")

    if request.method == "POST":
        conta_form = CadastroForm(request.POST)
        usuario_form = UsuarioForm(request.POST)

        conta_valida = conta_form.is_valid()
        usuario_valido = usuario_form.is_valid()

        if conta_valida and usuario_valido:
            with transaction.atomic():
                conta = conta_form.save()
                usuario = usuario_form.save(commit=False)
                usuario.conta = conta
                usuario.save()

            login(request, conta)
            return redirect("polls:listar_ofertas")

    else:
        conta_form = CadastroForm()
        usuario_form = UsuarioForm()

    contexto = {
        "conta_form": conta_form,
        "usuario_form": usuario_form
    }

    return render(request, "usuarios/cadastro_conta.html", contexto)
