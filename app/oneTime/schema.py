import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphene import relay, ObjectType, String
from graphene_django.filter import DjangoFilterConnectionField
from django.conf import settings
from oneTime.models import LoggedInUser
from oneTime.utils import generate_jti


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        filter_fields = ['id', 'username']
        interfaces = (relay.Node,)


class LoggedInType(DjangoObjectType):
    class Meta:
        model = LoggedInUser
        filter_fields = ['id']
        interfaces = (relay.Node,)


class CreateUser(graphene.Mutation):
    id = graphene.ID()

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    @classmethod
    def mutate(cls, root, info, username, password):
        User = get_user_model()
        user = User.objects.create_user(username)
        user.set_password(password)
        user.save()
        return cls(id=user.id)


class LogoutUser(graphene.Mutation):
    id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        user.logged_in_user.jti = generate_jti()
        user.logged_in_user.logged_in_before = False
        user.save()
        return cls(id=user.id)


class BayatMutation(graphene.ObjectType):
    logout_user = LogoutUser.Field()
    create_user = CreateUser.Field()


class BayatQuery(graphene.ObjectType):
    user = relay.Node.Field(UserType)
    user_list = DjangoFilterConnectionField(UserType)

    logged_in = relay.Node.Field(UserType)
    logged_in_list = DjangoFilterConnectionField(UserType)
