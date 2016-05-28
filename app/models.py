# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django.conf import settings
import datetime
from django.contrib.auth.models import User

#Enumarator
TIPO_PESSOA = (('1',u'Pessoa Física'), ('2',u'Pessoa Juridica'))
ESTADOS =  (('AC', u'Acre'), ('AL', u'Alagoas'), ('AP',u'Amapa'), ('AM',u'Amazonas'),('BA',u'Bahia'),('CE',u'Ceara'), ('DF',u'Distrito Federal'), ('ES',u'Espirito Santo'),('GO',u'Goias'),('MA',u'Maranhao'),('MS',u'Mato Grosso do Sul'),('MT',u'Mato Grosso'),('MG',u'Minas Gerais'), ('PA',u'Para'),('PB',u'Paraiba'),('PR',u'Parana'),('PE',u'Pernambuco'),('PI',u'Piaui'),('RJ',u'Rio de Janeiro'),('RN',u'Rio Grande do Norte'),('RS',u'Rio Grande do Sul'),('RO',u'Rondonia'),('RR',u'Roraima'),('SC',u'Santa Catarina'),('SP',u'Sao Paulo'),('SE',u'Sergipe'),('TO',u'Tocantins'))

TIPO_SERVICO = (('1',u'Remunerada'), ('2',u'Voluntaria'))

#Classes
class Perfil(models.Model):
    IdPerfil = models.AutoField(primary_key = True)
    DescricaoPerfil = models.CharField(max_length = 50, null = False)
    DataHoraInclusao = models.DateTimeField(auto_now_add=True)
    DataHoraExclusao = models.DateTimeField(null = True)
    @classmethod
    def create(self,IdPerfil, DescricaoPerfil,DataHoraInclusao,DataHoraExclusao):
        objPerfil = Perfil(IdPerfil = IdPerfil, DescricaoPerfil = DescricaoPerfil,DataHoraInclusao = datetime.datetime.now(),DataHoraExclusao = null)
        return objPerfil

class Endereco(models.Model):
    IdEndereco = models.AutoField(primary_key = True)
    CEP = models.CharField(max_length = 8, null = False)
    Estado = models.CharField(choices=ESTADOS, max_length = 2, null = False)
    Cidade = models.CharField(max_length = 100, null = False)
    Bairro = models.CharField(max_length = 100, null = False)
    Logradouro = models.CharField(max_length = 100, null = False)
    Numero = models.IntegerField(verbose_name=u'Número')
    Complemento = models.CharField(max_length = 100, null = True)
    Latitude = models.CharField(max_length = 50, null = True)
    Longitude = models.CharField(max_length = 50, null = True)

    @classmethod
    def create(self,CEP,Estado, Cidade, Bairro, Logradouro, Numero, Complemento ):
        objEndereco = Endereco(CEP = CEP, Estado = Estado, Cidade = Cidade, Bairro = Bairro, Logradouro = Logradouro, Numero = Numero, Complemento = Complemento, Latitude = None, Longitude=None)
        return objEndereco
    
class Usuario(models.Model):
    #extende os atributos da tabela usuario com relacao 1 para 1
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    IdUsuario = models.AutoField(primary_key = True)  
    IdPerfil = models.ForeignKey(Perfil)
    IdEndereco = models.ForeignKey(Endereco, null = True)
    IndicadorTipoPessoa = models.IntegerField(choices=TIPO_PESSOA, verbose_name='Tipo de Pessoa')
    CpfCnpj = models.CharField(max_length = 20, null = False, unique = True, verbose_name='CPF ou CNPJ')
    Nome = models.CharField(max_length = 100, null = False)
    Telefone1 = models.CharField(max_length = 16, null = True,verbose_name='Telefone Principal')
    Telefone2 = models.CharField(max_length = 16, null = True,verbose_name='Telefone Opcional')
    Email = models.CharField(max_length = 70, unique = True,verbose_name='Email/Login')
    Senha = models.CharField(max_length = 70, unique = False,verbose_name='Senha')
    DataHoraAprovacao = models.DateTimeField(null = True)
    DataHoraInclusao = models.DateTimeField(auto_now_add=True)
    DataHoraExclusao = models.DateTimeField(null = True)
    
    @classmethod
    def create(self,IdEndereco, IdPerfil, IndicadorTipoPessoa,CpfCnpj,Nome,Telefone1,Telefone2,Email,Senha):
        user = User.objects.create_user(username = Email,
                                        first_name = Nome.split(' ')[0],
                                        password = Senha
                                        ) 
        user.is_active = False
        user.save()

        objUsuario = Usuario(user_id = user.id ,IdEndereco = IdEndereco, IdPerfil = IdPerfil ,IndicadorTipoPessoa = IndicadorTipoPessoa,CpfCnpj = CpfCnpj,Nome= Nome,Telefone1 = Telefone1,Telefone2 = Telefone2, Email = Email, Senha = Senha, DataHoraAprovacao = None, DataHoraInclusao = datetime.datetime.now(), DataHoraExclusao = None)
        return objUsuario

class TipoDiferencial(models.Model):
    IdTipoDiferencial = models.AutoField(primary_key = True)
    DescricaoTipoDiferencial = models.CharField(max_length = 100, verbose_name='Descrição')
    
    def __unicode__(self):
        return self.DescricaoTipoDiferencial

class Diferencial(models.Model):
    IdDiferencial = models.AutoField(primary_key = True)
    IdUsuario = models.ForeignKey(Usuario)
    IdTipoDiferencial = models.ForeignKey(TipoDiferencial)
    Ano = models.IntegerField(verbose_name='Ano de realização')
    TituloDiferencial = models.CharField(max_length = 50, verbose_name='Título')
    DescricaoDiferencial = models.CharField(max_length = 300, verbose_name='Descrição')
    DataHoraInclusao = models.DateTimeField(auto_now_add=True)
    DataHoraExclusao = models.DateTimeField(null = True)

    @classmethod
    def create(self,Usuario,TipoDiferencial, Ano, TituloDiferencial, DescricaoDiferencial):
        objDiferencial = Diferencial(IdUsuario = Usuario , IdTipoDiferencial= TipoDiferencial, Ano = Ano, TituloDiferencial = TituloDiferencial,DescricaoDiferencial = DescricaoDiferencial, DataHoraInclusao = datetime.datetime.now(), DataHoraExclusao = None)
        return objDiferencial

#CLASSES DE DISPONIBILIDADE DO PRESTADOR
class DiaSemana(models.Model):
    IdDiaSemana = models.AutoField(primary_key = True)
    nomeDia = models.CharField(max_length = 30)

    def __unicode__(self):
        return self.nomeDia

class HorariosDisponibilidadeInicio(models.Model):
    IdHorariosDisponibilidadeInicio = models.AutoField(primary_key = True)
    HoraInicio = models.CharField(max_length = 7)
    def __unicode__(self):
        return self.HoraInicio
         
class HorariosDisponibilidadeFim(models.Model):
    IdHorariosDisponibilidadeFim = models.AutoField(primary_key = True)
    idHoraFim =  models.ForeignKey(HorariosDisponibilidadeInicio)

class DisponibilidadeUsuario(models.Model):
    idDisponibilidade =  models.AutoField(primary_key = True)
    idUsuario =  models.ForeignKey(Usuario)
    idDiaSemana =  models.ForeignKey(DiaSemana)
    idHorarioInicio =  models.ForeignKey(HorariosDisponibilidadeInicio)
    idHorarioFim =  models.ForeignKey(HorariosDisponibilidadeFim)
    DataHoraInclusao = models.DateTimeField(auto_now_add=True)
    DataHoraExclusao = models.DateTimeField(null = True)

    @classmethod
    def create(self,IdUsuario,IdDiaSemana, IdHorarioInicio,IdHorarioFim):
        objDisponibilidadeUsuario = DisponibilidadeUsuario(idUsuario = IdUsuario, idDiaSemana = IdDiaSemana,idHorarioInicio = IdHorarioInicio,idHorarioFim = IdHorarioFim,DataHoraInclusao = datetime.datetime.now(), DataHoraExclusao = None)
        return objDisponibilidadeUsuario
    
#CLASSES DOS SERVICOS EXECUTADOS. 
class Categoria(models.Model):
    IdCategoria = models.AutoField(primary_key = True)
    DescricaoCategoria = models.CharField(max_length = 250)
    
    def __unicode__(self):
     return self.DescricaoCategoria

    @classmethod
    def create(self, DescricaoCategoria):
        objCategoria = Categoria(DescricaoCategoria = DescricaoCategoria)
        return objCategoria
   
class SubCategoria(models.Model):
    IdSubCategoria = models.AutoField(primary_key = True)
    DescricaoSubCategoria = models.CharField(max_length = 150)
    IdCategoria = models.ForeignKey(Categoria)
    
    def __unicode__(self):
     return self.DescricaoSubCategoria

    @classmethod
    def create(self, DescricaoCategoria):
        objSubCategoria = SubCategoria(DescricaoCategoria = DescricaoCategoria)
        return objSubCategoria

class Servico(models.Model):
    IdServico = models.AutoField(primary_key = True)
    IdCategoria = models.ForeignKey(Categoria)
    IdSubCategoria = models.ForeignKey(SubCategoria)
    IdUsuario = models.ForeignKey(Usuario)
    IndicadorTipoServico = models.IntegerField(choices=TIPO_SERVICO, verbose_name='Categoria do Serviço')
    DescricaoServico = models.CharField(max_length = 100, verbose_name='Descrição do Serviço')
    ValorHora = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor/Hora')
    DataHoraInclusao = models.DateTimeField(auto_now_add=True)
    DataHoraExclusao = models.DateTimeField(null = True)

    @classmethod
    def create(self, IdCategoria,IdSubCategoria, IdUsuario, IndicadorTipoServico, DescricaoServico, ValorHora):
        objServico = Servico(IdCategoria = IdCategoria,IdSubCategoria = IdSubCategoria, IdUsuario = IdUsuario, IndicadorTipoServico = IndicadorTipoServico, DescricaoServico = DescricaoServico, ValorHora = ValorHora, DataHoraInclusao = datetime.datetime.now(), DataHoraExclusao = None )
        return objServico

class SituacaoServico(models.Model):
    IdSituacaoServico = models.CharField(max_length=2,primary_key = True)
    Descricao = models.CharField(max_length = 150)
    
    def __unicode__(self):
     return self.Descricao

class ClienteServico(models.Model):
    IdClienteServico = models.AutoField(primary_key = True)
    IdUsuario = models.ForeignKey(Usuario)
    IdServico = models.ForeignKey(Servico)
    DataServico = models.DateTimeField(null = False)
    QtHoras = models.IntegerField()
    ValorHora = models.DecimalField(max_digits=10, decimal_places=2)
    ValorTotal = models.DecimalField(max_digits=10, decimal_places=2)
    Descricao = models.CharField(max_length = 350)
    DataHoraConfirmacao = models.DateTimeField(null = True)
    IdSituacao = models.ForeignKey(SituacaoServico)
    Avaliacao = models.IntegerField(null = True)
    DataHoraSituacao = models.DateTimeField(null = True)
    DataHoraInclusao = models.DateTimeField(auto_now_add=True)
    DataHoraExclusao = models.DateTimeField(null = True)
    
    @classmethod
    def create(self, objUsuario, objServico, DataServico, QtHoras, ValorHora, ValorTotal, Descricao, Situacao):
        objClienteServico = ClienteServico(IdUsuario = objUsuario, IdServico = objServico, DataServico = DataServico, QtHoras = QtHoras,ValorHora = ValorHora, ValorTotal = ValorTotal, Descricao = Descricao,  DataHoraConfirmacao = None, IdSituacao = Situacao, DataHoraSituacao = datetime.datetime.now(), Avaliacao = None, DataHoraInclusao = datetime.datetime.now(), DataHoraExclusao = None)
        return objClienteServico
