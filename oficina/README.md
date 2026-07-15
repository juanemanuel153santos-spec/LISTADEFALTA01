# Sistema Motopeças — app "oficina"

Este pacote é um **app Django** pronto pra ser encaixado dentro do seu projeto. Ele cobre as Etapas 0 a 4 do roteiro: login com aprovação manual, cadastro de peças e mão de obra (mecânico), e visão geral + lista de falta (vendedor).

## 1. Criar o projeto (se ainda não tiver feito)

```bash
pip install django
django-admin startproject motopecas
cd motopecas
```

## 2. Colocar a pasta `oficina` dentro do projeto

Copie a pasta `oficina/` (que veio junto com este ZIP) para dentro da pasta `motopecas/` — ao lado da pasta `motopecas/motopecas/` que o Django cria automaticamente. A estrutura deve ficar assim:

```
motopecas/
├── manage.py
├── motopecas/          <- criado pelo django-admin
│   ├── settings.py
│   └── urls.py
└── oficina/             <- a pasta que eu criei
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── admin.py
    └── templates/
```

## 3. Editar `motopecas/settings.py`

Adicione `'oficina'` em `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'django.contrib.staticfiles',
    'oficina',
]
```

E no final do arquivo, adicione:

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
```

## 4. Editar `motopecas/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('oficina.urls')),
]
```

## 5. Rodar as migrações e criar um superusuário

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 6. Rodar o servidor

```bash
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/` para o sistema e `http://127.0.0.1:8000/admin/` para aprovar usuários (marque a caixa "aprovado" na tela de `Perfil usuario`).

## Como funciona o fluxo de aprovação

1. Usuário se cadastra em `/cadastro/` escolhendo se é mecânico ou vendedor
2. Fica com `aprovado = False` e vê a tela "Aguardando aprovação" ao logar
3. Você (admin) entra em `/admin/`, abre "Perfil usuario" e marca `aprovado` = sim
4. A partir daí o usuário tem acesso normal ao sistema

## O que já foi feito (Etapa 6 concluída)

- Filtro de busca em tempo real nas listas de peças, mão de obra e peças em falta (sem recarregar a página)
- Confirmação (`confirm()`) antes de marcar um item como comprado
- Validação simples no navegador nos formulários de cadastro (bloqueia valores numéricos ≤ 0 antes de enviar)
- Arquivo `oficina/static/oficina/js/main.js` com todo o JavaScript — o Django encontra ele sozinho porque o app já está em `INSTALLED_APPS` (não precisa configurar nada extra em desenvolvimento)

## O que ainda falta (próxima etapa do roteiro)

- Etapa 7: refinar layout com CSS e revisar permissões

## Sobre os erros que você quer corrigir/deixar mais flexível

Fica à vontade pra mexer — alguns pontos que provavelmente vão precisar de ajuste conforme o projeto cresce:

- Hoje o tipo de usuário é fixo (mecânico/vendedor) — se quiser mais tipos, é só adicionar em `PerfilUsuario.TIPO_CHOICES`
- A aprovação é manual via admin — dá pra criar uma tela própria pra isso depois
- Não tem paginação nas listas — se crescer muito, vale usar `Paginator` do Django
