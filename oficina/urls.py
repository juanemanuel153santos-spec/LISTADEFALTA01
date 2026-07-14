from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('cadastro/', views.cadastro, name='cadastro'),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('pecas/', views.lista_pecas, name='lista_pecas'),
    path('pecas/nova/', views.cadastrar_peca, name='cadastrar_peca'),

    path('maodeobra/', views.lista_maodeobra, name='lista_maodeobra'),
    path('maodeobra/nova/', views.cadastrar_maodeobra, name='cadastrar_maodeobra'),

    path('falta/', views.lista_falta, name='lista_falta'),
    path('falta/nova/', views.cadastrar_falta, name='cadastrar_falta'),
    path('falta/<int:item_id>/comprado/', views.marcar_comprado, name='marcar_comprado'),
]
