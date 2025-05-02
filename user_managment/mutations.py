# from graphql_jwt.decorators import login_required
# from graphql_jwt.shortcuts import get_token
# from django.core.mail import send_mail
# from django.conf import settings
# from django.utils import timezone
# from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
# import uuid
# import logging
# import requests
# import graphql_jwt


from django.db import IntegrityError
from graphql import GraphQLError
from django.contrib.auth import get_user_model, authenticate

import graphene
from .djangoObjectType import UserType
User = get_user_model()


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)


    # Return fields
    user = graphene.Field(UserType, description="The newly created User")
    success = graphene.Boolean(description="Whether the mutation was successful")
    message = graphene.String(description="Success or error message")
    def mutate(self, info, username, password, email,):
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
        except IntegrityError as e :
            if 'UNIQUE constraint failed' in str(e):
                raise GraphQLError(f" Integrity Error {e} Username {username} ")
            else:
                raise GraphQLError("An error occurred while creating the User.")

        return CreateUser( user=user, success=True, message="User created successfully" )


class LoginMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    access = graphene.String()
    refresh = graphene.String()
    user = graphene.Field(UserType)
    message = graphene.String()

    def mutate(self, info, email, password):
        try:
            user_ = User.objects.get(email=email)
        except User.DoesNotExist:
            raise GraphQLError(f"User with email {email} does not exist")

        user = authenticate(username=user_.username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
        
            refresh['userId'] = str(user.id) 
        
            if hasattr(user, 'user_type'):
                refresh['userType'] = user.user_type
            else:
                refresh['userType'] = user.user_type
            
            return LoginMutation(
                access=str(refresh.access_token), 
                refresh=str(refresh), 
                user=user, 
                message="Authenticated successfully"
            )

        raise GraphQLError('Invalid credentials')

