# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
import sqlite3
from app import models
from app.models import Usuario
from app.models import Endereco
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpRequest
from datetime import datetime
from Colmeia import p_perfil
from Colmeia import p_endereco
from django.db import connection
from app.forms import UsuarioForm, UserForm, EnderecoForm
from django.shortcuts import redirect
from datetime import datetime


def incluirUsuario(request):
    objEndereco = Endereco.create(request.POST['CEP'],request.POST['Estado'],request.POST['Cidade'], request.POST['Bairro'],request.POST['Logradouro'],request.POST['Numero'],request.POST['Complemento'] )
    objEndereco.save()
    objEndereco = p_endereco.recuperaUltimoEndereco()
    tipo = request.GET['tipo']
    if tipo == 'p':
        objPerfil = p_perfil.recuperaPerfil('2') #perfil 2 = Prestador
    else:
        objPerfil = p_perfil.recuperaPerfil('3') #perfil 3 = Contratante
    
    objUsuario = Usuario.create(objEndereco, objPerfil, request.POST['IndicadorTipoPessoa'],request.POST['CpfCnpj'],request.POST['Nome'],request.POST['Telefone1'],request.POST['Telefone2'],request.POST['Email'],request.POST['Senha'])
    objUsuario.save()
    return objUsuario.Nome.split(' ')[0]

def incluirPrestador(request):
    nome = incluirUsuario(request)
    form = UsuarioForm()
    userfrm = UserForm()
    end = EnderecoForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/site/confirmaCadastro.html',
        context_instance = RequestContext(request,
        {
            'title':'Colmeia | Inicio',
            'tipo': 'Prestador',
            'nome': nome,
            'year': datetime.now().year,
        })
    )

def incluirContratante(request):
    nome = incluirUsuario(request)
    form = UsuarioForm()
    userfrm = UserForm()
    end = EnderecoForm()
    assert isinstance(request, HttpRequest)
    return render(
       request,
        'app/site/confirmaCadastro.html',
        {'form': form, 'userfrm': userfrm,'endereco':end},
        context_instance = RequestContext(request,
        {
            'title':'Colmeia | Inicio',
            'tipo': 'Contratante',
            'nome': nome,
            'year': datetime.now().year,
        })
    )

#recupera todos os objetos
def recuperaUsuario():
    objUsuario = models.Usuario.objects.all()
    return objUsuario

#recupera todos um objeto especifico pelo id
def recuperaUsuario(idObj):
	objUsuario = models.Usuario.objects.get(id=idObj)
	return objUsuario

def aprovaUsuarioP(request):
    idObj = request.GET['id']
    objUser = models.User.objects.get(id=idObj)
    objUsuario = models.Usuario.objects.get(user_id = idObj)
    #Registra data e hora da aprovacao do cadastro
    objUsuario.DataHoraAprovacao = datetime.now()
    objUsuario.save()
    #Ativa o cadastro de usuarios para fazer plugIn
    objUser.is_active = True
    objUser.save()


    
    return redirect('prestadores')

def aprovaUsuarioC(request):
    idObj = request.GET['id']
    objUser = models.User.objects.get(id=idObj)
    objUsuario = models.Usuario.objects.get(user_id = idObj)
    #Registra data e hora da aprovacao do cadastro
    objUsuario.DataHoraAprovacao = datetime.now()
    objUsuario.save()
    #Ativa o cadastro de usuarios para fazer plugIn
    objUser.is_active = True
    objUser.save()
    
    return redirect('contratantes')

def recuperaQtdPrestPendentes():
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(A.user_id) FROM app_usuario AS A JOIN auth_user AS B ON (A.user_id = B.id) WHERE (B.is_active = 0 AND A.IdPerfil_id = 2)')
    rows = cursor.fetchall()
    return rows

def recuperaQtdContPendentes():
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(A.user_id) FROM app_usuario AS A JOIN auth_user AS B ON (A.user_id = B.id) WHERE (B.is_active = 0 AND A.IdPerfil_id = 1)')
    rows = cursor.fetchall()
    return rows

def recuperaQtdContPendentes():
    return  models.User.filter(IdPerfil = '2').count()
#recupera todos um objeto especifico pelo id
def recuperaPrestadoresPendentesAprovacao():
    cursor = connection.cursor()
    cursor.execute('SELECT A.Nome, B.username, A.Telefone1, A.CpfCnpj, P.DescricaoPerfil, B.id FROM app_usuario AS A JOIN auth_user AS B ON (A.user_id = B.id) JOIN app_perfil AS P ON (A.IdPerfil_id = P.IdPerfil) WHERE (B.is_active = 0 AND A.IdPerfil_id = 2)')
    rows = cursor.fetchall()
    return rows

#recupera todos um objeto especifico pelo id
def recuperaContratantesPendentesAprovacao():
    cursor = connection.cursor()
    
    cursor.execute('SELECT A.Nome, B.username, A.Telefone1, A.CpfCnpj, P.DescricaoPerfil, B.id FROM app_usuario AS A JOIN auth_user AS B ON (A.user_id = B.id) JOIN app_perfil AS P ON (A.IdPerfil_id = P.IdPerfil) WHERE (B.is_active = 0 AND A.IdPerfil_id = 3)')
    rows = cursor.fetchall()
    return rows