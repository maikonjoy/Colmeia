# -*- coding: utf-8 -*-
"""
Definition of forms.
"""

from django import forms	
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import *
from Colmeia import p_categoria


class BootstrapAuthenticationForm(AuthenticationForm):
    #Authentication form which uses boostrap CSS.
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['IndicadorTipoPessoa', 'CpfCnpj', 'Nome', 'Telefone1', 'Telefone2']
        
        widgets = {
            'IndicadorTipoPessoa': forms.Select(attrs={'class': 'form-control',
                                                    'placeholder': 'Tipo pessoa',
                                                    'required': 'true',                    
                                                   'style': 'margin-bottom: 10px; width: 200px;'
                                                    }),
            'CpfCnpj': forms.TextInput(attrs={'class': 'form-control',
                                             'style': 'margin-bottom: 10px; width: 200px;',
                                            'placeholder': 'CPF /  CNPJ',
                                            #'pattern': '(\d{3}\d{3}\d{3}\d{2}|\d{2}\d{3}\d{3}\d{4}\d{2})',
                                            'required': 'true'}),

            'Nome': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Nome',
                                            'style': 'margin-bottom: 10px;',
                                            'required': 'true'}),

            'Telefone1': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Telefone',
                                                'style': 'margin-bottom: 10px; width: 200px;',
                                                'type' : 'tel',
                                                #'pattern': '^\(\d{2}\) 9?\d{4}-\d{4}$',
                                                'required': 'true'}),

            'Telefone2': forms.TextInput(attrs={'class': 'form-control',
                                                'type' : 'tel',
                                               'style': 'margin-bottom: 10px; width: 200px;',
                                                'placeholder': 'Telefone',
                                                
                                                #'pattern': '^\(\d{2}\) 9?\d{4}-\d{4}$'
                                                }),
       
        }
      
class UserForm(forms.Form):
    Email = forms.CharField(max_length=100, label= u'* E-mail',  widget=forms.TextInput({
                                   'class': 'form-control',
                                   'style': 'margin-bottom: 10px;',
                                   'type:' : 'email',
                                   'required' : 'required',
                                   'placeholder': 'E-mail'}))
    Senha = forms.CharField(label= u'* Senha',max_length=100,  widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'required' : 'required',
                                   'placeholder':'Password'}))
    
class EnderecoForm(ModelForm):
    class Meta: 
        model = Endereco
     
        fields = ['CEP', 'Estado', 'Cidade', 'Bairro', 'Logradouro','Numero','Complemento']
        
        widgets = {
            'CEP': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'CEP',
                                                    'required': 'true',                    
                                                    'style': 'margin-bottom: 10px; width: 200px;'
                                                    }),
            'Estado': forms.Select(attrs={'class': 'form-control',
                                                    'placeholder': 'Estado',
                                                    'required': 'true',                    
                                                    'style': 'margin-bottom: 10px; width: 200px;'
                                                    }),
            'Cidade': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Cidade',
                                                    'required': 'true',                    
                                                    'style': 'margin-bottom: 10px;'
                                                    }),
            'Bairro': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Bairro',
                                                    'required': 'true',                    
                                                    'style': 'margin-bottom: 10px;'
                                                    }),
            'Logradouro': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Rua Exemplo ou Avenida Exemplo',
                                                    'required': 'true',                    
                                                    'style': 'margin-bottom: 10px;'
                                                    }),
            'Numero': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Numero',
                                                    'required': 'true',                    
                                                    'style': 'margin-bottom: 10px; width: 200px;'
                                                    }),
            'Complemento': forms.TextInput(attrs={'class': 'form-control',
                                                    'placeholder': 'Complemento',
                                                    'style': 'margin-bottom: 10px;'
                                                    })
            }

class DiferencialForm(forms.Form):
      IdTipoDiferencial = forms.ModelChoiceField(queryset= TipoDiferencial.objects.all().order_by('DescricaoTipoDiferencial'),label= u'Tipo Diferencial',  widget=forms.Select({
                                   'class': 'form-control',
                                   'style': 'margin-bottom: 10px;',
                                   'required' : 'true'
                                   }))
      Ano = forms.CharField(widget = forms.TextInput({'class': 'span7',
                                                    'required': 'true', 
                                                    'placeholder': 'Ano de Conclusão',                    
                                                    'style': 'margin-bottom: 10px; width: 200px;'
                                                    }))
      TituloDiferencial = forms.CharField(label = u'Título',widget = forms.TextInput({'class': 'span9',
                                                    'required': 'true', 
                                                    'style': 'margin-bottom: 10px; width: 300px;'
                                                    }))
      DescricaoDiferencial = forms.CharField(label=u'Descrição',widget = forms.Textarea({'class': 'span9',
                                                    'required': 'true', 
                                                    'cols':'10',
                                                    'placeholder': 'Descreva em poucas palavras seu diferencial',             
                                                    'style': 'margin-bottom: 10px; width: 300px;'
                                                    }))

class DisponibilidadeUsuarioForm(forms.Form):
      IdDiaSemana = forms.ModelChoiceField(queryset= DiaSemana.objects.all().order_by('nomeDia'),label= u'Dia da semana',  widget=forms.Select({
                                   'class': 'form-control',
                                   'style': 'margin-bottom: 10px;',
                                   'required' : 'true'  
                                   }))

      idHoraInicio = forms.ModelChoiceField(queryset= HorariosDisponibilidadeInicio.objects.all().order_by('HoraInicio'),label= u'Hora início',  widget=forms.Select({
                                   'class': 'form-control',
                                   'style': 'margin-bottom: 10px;',
                                   'required' : 'true'  
                                   }))
      idHoraFim = forms.ModelChoiceField(queryset= HorariosDisponibilidadeFim.objects.all().order_by('HoraFim'),label= u'Hora Fim',  widget=forms.Select({
                                   'class': 'form-control',
                                   'style': 'margin-bottom: 10px;',
                                   'required' : 'true'  
                                   }))
          
TIPO_SERVICO = (('1',u'Remunerada'), ('2',u'Voluntaria'))
class ServicoForm(forms.Form):
    IdCategoria = forms.ModelChoiceField(queryset= Categoria.objects.all().order_by('DescricaoCategoria'),label= u'Categoria de Serviço',  widget=forms.Select({
                                   'class': 'form-control',
                                   'style': 'margin-bottom: 10px;',
                                   'required' : 'required'
                                   }))
    IdSubCategoria = forms.ModelChoiceField(queryset= SubCategoria.objects.all().order_by('DescricaoSubCategoria'),label= u'Subcategoria de Serviço',  widget=forms.Select({
                                   'class': 'form-control',
                                   'style': 'margin-bottom: 10px;',
                                   'required' : 'required',
                                   'enabled' : 'false',
                                   'placeholder': 'E-mail'}))

    IndicadorTipoServico =  forms.ChoiceField(choices = TIPO_SERVICO, widget=forms.Select({'class': 'span7',
                                                    'required': 'true',                     
                                                    'style': 'margin-bottom: 10px; width: 200px;'
                                                    }))
    ValorHora = forms.CharField(widget = forms.TextInput({'class': 'span7',
                                                    'required': 'true',                     
                                                    'style': 'margin-bottom: 10px; width: 200px;'
                                                    }))
    DescricaoServico = forms.CharField(widget=forms.Textarea({'class': 'span9',
                                                    'required': 'true',  
                                                    'style': 'margin-bottom: 10px; width: 300px;'
                                                    }))
    
class DisponibilidadeForm(forms.Form):
    IdDiaSemana = forms.ModelChoiceField(queryset= DiaSemana.objects.all().order_by('IdDiaSemana'),label= u'Dia da semana',  widget=forms.Select({
                                   'class': 'form-control',
                                   'style': 'margin-bottom: 10px;',
                                   'required' : 'required'
                                   }))
    IdHorariosDisponibilidadeInicio = forms.ModelChoiceField(queryset= HorariosDisponibilidadeInicio.objects.all().order_by('IdHorariosDisponibilidadeInicio'),label= u'Hora Inicio',  widget=forms.Select({
                                   'class': 'form-control',
                                   'style': 'margin-bottom: 10px;',
                                   'required' : 'required'
                                   }))

    IdHorariosDisponibilidadeFim = forms.ModelChoiceField(queryset= HorariosDisponibilidadeInicio.objects.all().order_by('IdHorariosDisponibilidadeInicio'),label= u'Hora Fim',  widget=forms.Select({
                                   'class': 'form-control',
                                   'style': 'margin-bottom: 10px;display:inline-block;',
                                   'required' : 'required'
                                   }))

class PesquisaForm(forms.Form):
     IdCategoria = forms.ModelChoiceField(queryset= Categoria.objects.all().order_by('DescricaoCategoria'),label= u'',  widget=forms.Select({
                                   'class': 'form-control',
                                   'style': 'float:left;margin-left: 20px;',
                                   'required' : 'required'
                                   }))
     IdSubCategoria = forms.ModelChoiceField(queryset= SubCategoria.objects.all().order_by('DescricaoSubCategoria'),label= u'',  widget=forms.Select({
                                   'class': 'form-control',
                                   'style': 'float:left;margin-left: 20px;',
                                   'required' : 'required',
                                   'enabled' : 'false'
                                   }))

     PalavraChave = forms.CharField(label= u'',  widget=forms.TextInput({
                                   'class': 'form-control',
                                   'style': 'float:left;margin-left: 20px;height: auto',
                                   'placeholder' : 'Palavra chave: Carteira B, Domicílio, etc.'
                                   }))

class PesquisaFormSite(forms.Form):
     IdCategoria = forms.ModelChoiceField(queryset= Categoria.objects.all().order_by('DescricaoCategoria'),label= u'',  widget=forms.Select({
                                   'class': 'form-control',
                                   'style': 'float:left;margin-left: 20px;',
                                   'required' : 'required'
                                   }))
     IdSubCategoria = forms.ModelChoiceField(queryset= SubCategoria.objects.all().order_by('DescricaoSubCategoria'),label= u'',  widget=forms.Select({
                                   'class': 'form-control',
                                   'style': 'float:left;margin-left: 20px;',
                                   'required' : 'required',
                                   'enabled' : 'false'
                                   }))

     PalavraChave = forms.CharField(label= u'',  widget=forms.TextInput({
                                   'class': 'form-control',
                                   'style': 'float:left;margin-left: 20px;height: auto',
                                   'placeholder' : 'Palavra chave: Carteira B, Domicílio, etc.'
                                   }))

SITUACAO = (('AP',u'Aprovação Pendente'), ('AG',u'Aceito e Agendado'), ('CP',u'Cancelado pelo prestador'),('CC',u'Cancelado pelo Cliente'),('EX',u'Executado'),('AV',u'Avaliado'))
class ContrataServicoForm(forms.Form):
    DataServico = forms.DateTimeField(label=u'',widget=forms.DateTimeInput({
            'type' : 'date',
           'class':'form-control',
           'required':'true'}))
    QtHoras = forms.IntegerField(widget = forms.TextInput({
            'class':'form-control',
            'required':'true',
            'type':'number' }))
    ValorHora = forms.DecimalField(decimal_places = 2,widget = forms.TextInput({
            'class':'form-control',
            'required':'true',
            'enabled':'False' }))
    ValorTotal = forms.DecimalField(decimal_places = 2,widget = forms.TextInput({
            'required':'true' }))
    Descricao = forms.CharField(widget=forms.Textarea({
            'class':'form-control',
            'class': 'span9',
            'required': 'true',
            'rows':'5',  
            'style': 'margin-bottom: 10px; width: 250px;'
        }))
