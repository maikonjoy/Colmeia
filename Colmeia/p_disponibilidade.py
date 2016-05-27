#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
import sqlite3
from app import models
from app.models import Perfil
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect

def incluir(request):
    objUser = models.Usuario.objects.get(IdUsuario = request.user.id)
    objDiaSemana = models.DiaSemana.objects.get(IdDiaSemana = request.POST['IdDiaSemana'])
    objHoraInicio = models.HorariosDisponibilidadeInicio.objects.get(IdHorariosDisponibilidadeInicio = request.POST['IdHorariosDisponibilidadeInicio'])
    objHoraFim = models.HorariosDisponibilidadeFim.objects.get(IdHorariosDisponibilidadeFim = request.POST['IdHorariosDisponibilidadeFim'])
    objDisponibilidade = models.DisponibilidadeUsuario.create(objUser, objDiaSemana, objHoraInicio, objHoraFim)
    objDisponibilidade.save()
    request.session['msg'] = 'Dados inseridos com sucesso!'
    return redirect('disponibilidade')

def alterar(request):
	idObj = request.GET['id']
	objDisponibilidade = models.DisponibilidadeUsuario.objects.get(idDisponibilidade=idObj)
	objDiaSemana = models.DiaSemana.objects.get(IdDiaSemana = request.POST['IdDiaSemana'])
	objHoraInicio = models.HorariosDisponibilidadeInicio.objects.get(IdHorariosDisponibilidadeInicio = request.POST['IdHorariosDisponibilidadeInicio'])
	objHoraFim = models.HorariosDisponibilidadeFim.objects.get(IdHorariosDisponibilidadeFim = request.POST['IdHorariosDisponibilidadeFim'])
	objDisponibilidade.idDiaSemana = objDiaSemana
	objDisponibilidade.idHorarioInicio = objHoraInicio
	objDisponibilidade.idHorarioFim = objHoraFim
	objDisponibilidade.save()
	request.session['msg'] = 'Dados alterados com sucesso.'
	return redirect('disponibilidade')

#exclui um objeto especifico pelo id e o retorna para confirmar a exclusao do objeto
def excluir(request):
	idObj = request.GET['id']
	objExcluido = models.DisponibilidadeUsuario.objects.get(IdDisponibilidade=idObj)
	objExcluido.delete()
	request.session['msg'] = 'Registro excluido com sucesso'
	return redirect('disponibilidade')

#recupera todos os objetos
def recuperaDisponibilidade():
    objDisponibilidade = models.DisponibilidadeUsuario.objects.all()
    return objDisponibilidade

#recupera todos um objeto especifico pelo id
def recuperaDisponibilidade(idObj):
	objDisponibilidade = models.DisponibilidadeUsuario.objects.get(IdDisponibilidade=idObj)
	return objDisponibilidade

#subCategoria, tipoDisponibilidade, valorHora, descricao

#recupera todos os objetos
def recuperaDisponibilidadePorPrestador(id_user):
    objDisponibilidade = models.DisponibilidadeUsuario.objects.filter(idUsuario_id = id_user).order_by('idDiaSemana')
    return objDisponibilidade


