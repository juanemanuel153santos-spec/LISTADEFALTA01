from django.contrib import admin
from .models import PerfilUsuario, Peca, MaoDeObra, PecaEmFalta


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    # list_editable permite marcar "aprovado" direto na listagem, sem abrir cada usuário
    list_display = ('usuario', 'tipo', 'aprovado')
    list_editable = ('aprovado',)
    list_filter = ('tipo', 'aprovado')


@admin.register(Peca)
class PecaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade', 'preco', 'cadastrado_por', 'data_cadastro')
    list_filter = ('cadastrado_por',)


@admin.register(MaoDeObra)
class MaoDeObraAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'cadastrado_por', 'data_cadastro')


@admin.register(PecaEmFalta)
class PecaEmFaltaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade_desejada', 'comprado', 'solicitado_por')
    list_editable = ('comprado',)
