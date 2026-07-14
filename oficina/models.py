from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    """
    Extensão do usuário padrão do Django.
    Guarda o tipo (mecânico ou vendedor) e se já foi aprovado
    pra poder acessar o sistema.
    """
    TIPO_CHOICES = [
        ('mecanico', 'Mecânico'),
        ('vendedor', 'Vendedor'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    aprovado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} ({self.get_tipo_display()})"


class Peca(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    quantidade = models.PositiveIntegerField(default=1)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    cadastrado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pecas')
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['-data_cadastro']


class MaoDeObra(models.Model):
    descricao = models.CharField(max_length=300)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    cadastrado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maodeobras')
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ['-data_cadastro']
        verbose_name_plural = "Mão de obra"


class PecaEmFalta(models.Model):
    nome = models.CharField(max_length=200)
    quantidade_desejada = models.PositiveIntegerField(default=1)
    comprado = models.BooleanField(default=False)
    solicitado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='falta_pecas')
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.quantidade_desejada})"

    class Meta:
        ordering = ['comprado', '-data_solicitacao']
        verbose_name_plural = "Peças em falta"
