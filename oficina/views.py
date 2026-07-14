from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden

from .forms import CadastroForm, PecaForm, MaoDeObraForm, PecaEmFaltaForm
from .models import Peca, MaoDeObra, PecaEmFalta


def cadastro(request):
    """Tela de cadastro de novo usuário (fica pendente de aprovação)."""
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Cadastro realizado! Aguarde a aprovação de um administrador para poder entrar.'
            )
            return redirect('login')
    else:
        form = CadastroForm()
    return render(request, 'oficina/cadastro.html', {'form': form})


def _usuario_aprovado(user):
    """Confere se o usuário logado tem perfil e está aprovado."""
    return hasattr(user, 'perfil') and user.perfil.aprovado


@login_required
def dashboard(request):
    """
    Página inicial após o login.
    Bloqueia quem ainda não foi aprovado e manda cada tipo de usuário
    pra sua respectiva área.
    """
    if not _usuario_aprovado(request.user):
        return render(request, 'oficina/aguardando_aprovacao.html')

    return render(request, 'oficina/dashboard.html', {
        'tipo': request.user.perfil.tipo,
    })


@login_required
def cadastrar_peca(request):
    if not _usuario_aprovado(request.user):
        return HttpResponseForbidden("Sua conta ainda não foi aprovada.")

    if request.method == 'POST':
        form = PecaForm(request.POST)
        if form.is_valid():
            peca = form.save(commit=False)
            peca.cadastrado_por = request.user
            peca.save()
            messages.success(request, 'Peça cadastrada com sucesso!')
            return redirect('lista_pecas')
    else:
        form = PecaForm()
    return render(request, 'oficina/peca_form.html', {'form': form})


@login_required
def lista_pecas(request):
    if not _usuario_aprovado(request.user):
        return HttpResponseForbidden("Sua conta ainda não foi aprovada.")

    # Vendedor vê tudo; mecânico vê só o que ele mesmo cadastrou
    if request.user.perfil.tipo == 'vendedor':
        pecas = Peca.objects.all()
    else:
        pecas = Peca.objects.filter(cadastrado_por=request.user)

    return render(request, 'oficina/lista_pecas.html', {'pecas': pecas})


@login_required
def cadastrar_maodeobra(request):
    if not _usuario_aprovado(request.user):
        return HttpResponseForbidden("Sua conta ainda não foi aprovada.")

    if request.method == 'POST':
        form = MaoDeObraForm(request.POST)
        if form.is_valid():
            mao_de_obra = form.save(commit=False)
            mao_de_obra.cadastrado_por = request.user
            mao_de_obra.save()
            messages.success(request, 'Mão de obra cadastrada com sucesso!')
            return redirect('lista_maodeobra')
    else:
        form = MaoDeObraForm()
    return render(request, 'oficina/maodeobra_form.html', {'form': form})


@login_required
def lista_maodeobra(request):
    if not _usuario_aprovado(request.user):
        return HttpResponseForbidden("Sua conta ainda não foi aprovada.")

    if request.user.perfil.tipo == 'vendedor':
        itens = MaoDeObra.objects.all()
    else:
        itens = MaoDeObra.objects.filter(cadastrado_por=request.user)

    return render(request, 'oficina/lista_maodeobra.html', {'itens': itens})


@login_required
def cadastrar_falta(request):
    if not _usuario_aprovado(request.user):
        return HttpResponseForbidden("Sua conta ainda não foi aprovada.")

    if request.method == 'POST':
        form = PecaEmFaltaForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.solicitado_por = request.user
            item.save()
            messages.success(request, 'Item adicionado à lista de peças em falta.')
            return redirect('lista_falta')
    else:
        form = PecaEmFaltaForm()
    return render(request, 'oficina/falta_form.html', {'form': form})


@login_required
def lista_falta(request):
    if not _usuario_aprovado(request.user):
        return HttpResponseForbidden("Sua conta ainda não foi aprovada.")

    itens = PecaEmFalta.objects.all()
    return render(request, 'oficina/lista_falta.html', {'itens': itens})


@login_required
def marcar_comprado(request, item_id):
    """Marca um item da lista de falta como comprado (só vendedor)."""
    if request.user.perfil.tipo != 'vendedor':
        return HttpResponseForbidden("Só o vendedor pode marcar itens como comprados.")

    item = get_object_or_404(PecaEmFalta, id=item_id)
    item.comprado = True
    item.save()
    return redirect('lista_falta')
