"""
Definition of urls for Colmeia.
"""
from django.http import HttpResponse
from django.shortcuts import render
import sqlite3
from app import models
from app.models import Perfil
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect

from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm
import p_usuario, p_servico, p_categoria, p_diferencial, p_disponibilidade, p_clienteServico
from django.http import HttpRequest


# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscreques
urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.index', name='index'),
    url(r'^inicio', 'app.views.inicio', name='inicio'),
    url(r'^search', 'app.views.search', name='search'),
    url(r'^quemSomos', 'app.views.quemSomos', name='quemSomos'),
    
    url(r'^admin', 'app.views.admin', name='admin'),    
    url(r'^prestadores', 'app.views.prestadores', name='prestadores'),
    url(r'^contratantes', 'app.views.contratantes', name='contratantes'),
    url(r'^relatorioAdm', 'app.views.relatorioAdm', name='relatorioAdm'),
    
    #Menu Prestador
    url(r'^diferenciais', 'app.views.diferenciais', name='diferenciais'),    
    url(r'^disponibilidade', 'app.views.disponibilidade', name='disponibilidade'),    
    url(r'^servicosOferecidos', 'app.views.servicosOferecidos', name='servicosOferecidos'),
    url(r'^gerServicos', 'app.views.gerServicos', name='gerServicos'),
    url(r'^colmeiaPontos', 'app.views.colmeiaPontos', name='colmeiaPontos'),
    url(r'^relPrestador', 'app.views.relPrestador', name='relPrestador'),
    
    #Menu Contratante
    url(r'^pesquisaServicos', 'app.views.pesquisaServicos', name='pesquisaServicos'),    
    url(r'^servContratados', 'app.views.servContratados', name='servContratados'),
    url(r'^relContratante', 'app.views.relContratante', name='relContratante'),

    #Urls persistencia
    url(r'^i_prestador', p_usuario.incluirPrestador, name='i_prestador'),
    url(r'^i_contratante', p_usuario.incluirContratante, name='i_contratante'),
    url(r'^aprova_usuariosP', p_usuario.aprovaUsuarioP, name='aprova_usuariosP'),
    url(r'^aprova_usuariosC', p_usuario.aprovaUsuarioC, name='aprova_usuariosC'),
    #url(r'^sucesso', p_usuario.incluirContratante, name='i_contratante'),
    #url(r'^c_usuario', c_usuario.incluir, name='c_usuario'),
    
    #URLS para Persistencia dos Servicos
    url(r'^i_servico', p_servico.incluir, name='i_servico'),
    url(r'^a_servico', p_servico.alterar, name='a_servico'),
    url(r'^e_servico', p_servico.excluir, name='e_servico'),
    url(r'^subCategorias',p_categoria.recuperaSubCategoriasPorCategoria, name='subCategorias'),
    

    #URLS para Persistencia dos Servicos
    url(r'^i_diferencial', p_diferencial.incluir, name='i_diferencial'),
    url(r'^a_diferencial', p_diferencial.alterar, name='a_diferencial'),
    url(r'^e_diferencial', p_diferencial.excluir, name='e_diferencial'),

    #URLS para Persistencia da Disponibilidade
    url(r'^i_disponibilidade', p_disponibilidade.incluir, name='i_disponibilidade'),
    url(r'^a_disponibilidade', p_disponibilidade.alterar, name='a_disponibilidade'),
    url(r'^e_disponibilidade', p_disponibilidade.excluir, name='e_disponibilidade'),

    url(r'^contrataServico', p_clienteServico.contrataServico, name='contrataServico'),
    
    #Site Principal
    url(r'^s_contato', 'app.views.s_contato', name='s_contato'),
    url(r'^s_quemSomos', 'app.views.s_quemSomos', name='s_quemSomos'),

    url(r'^sair', 'app.views.sair', name='sair'),
    url(r'^fazLogin', 'app.views.fazLogin', name='fazLogin'),
    
    url(r'^loginpage',
        'django.contrib.auth.views.login',
        {
            'template_name': 'app/geral/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Colmeia Login',
                'year':datetime.now().year,
            }
        },
        name='login'),
    
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
