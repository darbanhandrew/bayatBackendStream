import graphene
import graphql_jwt
from ipware import get_client_ip

from oneTime.models import LoggedInUser
from oneTime.schema import BayatMutation, BayatQuery, UserType
from graphql_jwt.utils import jwt_payload as graphql_jwt_payload
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)
    # ip = graphene.String()
    # session = graphene.String()

    # @classmethod
    # def Field(cls, *args, **kwargs):
    #     cls._meta.arguments.update({
    #         'session': graphene.String()
    #     })
    #     return super().Field(*args, **kwargs)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        # request = info.context.request
        # client_ip, is_routable = get_client_ip(request)
        # session = kwargs['session']
        return cls(user=info.context.user)


class AuthMutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(
    BayatQuery,  # Add your Query objects here
    graphene.ObjectType
):
    pass


class Mutation(AuthMutation, BayatMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
