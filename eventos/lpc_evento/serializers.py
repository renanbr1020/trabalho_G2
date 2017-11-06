from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
from lpc_evento.models import Pessoa, Evento, Ticket, Inscricao

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class PessoaSerializer(serializers.HyperlinkedModelSerializer):
    usuario = UserSerializer(many = False)

    class Meta:
        model = models.Pessoa
        fields = ('nome', 'email', 'sexo', 'idade', 'usuario')

    def create(self,dados):
        dados_user = dados.pop('usuario')
        u =  User.objects.create(**dados_user)
        p = models.Pessoa.objects.create(usuario=u,**dados)
        return p 

class EventoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Evento
        fields = ('nome', 'dataEHoraDeInicio','endereco','logotipo','sigla','eventoPrincipal')

    def create(self,dados):
        return models.Evento.objects.create(**dados)


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    idEvento = EventoSerializer(many = False)
    class Meta:
        model = models.Ticket
        fields = ('nome', 'descricao','valor','idEvento')

    def create(self,dados):
        dados_evento = dados.pop ('idEvento')
        e =  models.Evento.objects.create(**dados_evento)
        t = models.Ticket.objects.create(evento=e,**dados)
        return t 

'''
class TicketSerializer(serializers.HyperlinkedModelSerializer):
    #evento = EventoSerializer(many=False)
    class Meta:
        model = models.Ticket
        fields = "__all__"
    def create(self,dados):
        evento_data = dados.pop("evento")
        evento = models.Evento.objects.get(nome=evento_data)
        return models.Ticket.objects.create(evento = evento,**dados)
'''


class InscricaoSerializer(serializers.HyperlinkedModelSerializer):
    Evento = EventoSerializer(many = False)
    Participante = PessoaSerializer(many = False)
    Ticket = TicketSerializer(many = False)
    class Meta:
        model = Inscricao
        fields = ('Evento', 'Participante','Ticket','validacao')

'''
class UserSerializar (serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username','email','profile')
    
    def create (self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user,**profile_data)
        return user
'''