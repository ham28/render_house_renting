import graphene
from .mutations import CreateUser, LoginMutation


class Mutation(graphene.ObjectType):
    add_user = CreateUser.Field()
    login_mutaion = LoginMutation.Field()


# from .models import UserDevice
#
#
# logger = logging.getLogger("django")

#
#
# class LoginResponse(graphene.ObjectType):
#     access = graphene.String()
#     refresh = graphene.String()
#     user = graphene.Field(UserType)
#
#
# class AuthResponse(graphene.ObjectType):
#     status = graphene.String()
#     message = graphene.String()
#
#
# class LoginResponse(graphene.ObjectType):
#     access = graphene.String()
#     refresh = graphene.String()
#     user = graphene.Field(UserType)
#
#
# class TokenValidationResponse(graphene.ObjectType):
#     message = graphene.String()
#
#
# class CredentialsVerificationResponse(graphene.ObjectType):
#     status = graphene.String()
#
#

#
#
# class VerifyCredentialsMutation(graphene.Mutation):
#     class Arguments:
#         username = graphene.String(required=True)
#         password = graphene.String(required=True)
#
#     Output = CredentialsVerificationResponse
#
#     def mutate(cls, root, info, username, password):
#         user = authenticate(username=username, password=password)
#         if user:
#             return CredentialsVerificationResponse(status="valid")
#         logger.warning(f'Invalid verification attempt for username: {username}')
#         return CredentialsVerificationResponse(status="invalid")
#
#
# class ValidateTokenQuery(graphene.ObjectType):
#     validate_token = graphene.Field(TokenValidationResponse)
#
#     def resolve_validate_token(root, info):
#         # Add logic to validate the token here
#         return TokenValidationResponse(message="Token is valid.")
#
#
# class SMSUserRegisterMutation(graphene.Mutation):
#     class Arguments:
#         username = graphene.String(required=True)
#         password = graphene.String(required=True)
#
#     Output = AuthResponse
#
#     def mutate(self, info, username, password):
#         try:
#             user = User.objects.create_user(username=username, password=password)
#             user.save()
#             return AuthResponse(
#                 status='success',
#                 message='User created successfully'
#             )
#         except Exception as e:
#             logger.error(f"Error creating SMS user: {str(e)}")
#             raise graphene.GraphQLError('Error creating user')
#
#
# class Query(graphene.ObjectType):
#     users = graphene.List(UserType)
#     me = graphene.Field(UserType)
#     check_device_status = graphene.Field(
#         graphene.Boolean,
#         username=graphene.String(required=True),
#         device_name=graphene.String(required=True)
#     )
#     check_admin_status = graphene.Field(UserType)
#     validate_token = graphene.Field(AuthResponse)
#     user = graphene.Field(UserType, id=graphene.String(required=True))
#
#     @login_required
#     def resolve_users(self, info):
#         return User.objects.all()
#
#     @login_required
#     def resolve_me(self, info):
#         user = info.context.user
#         if user.is_authenticated:
#             return user
#         return None
#
#     @login_required
#     def resolve_user(self, info, id):
#         return User.objects.get(id=id)
#
#
#     def resolve_check_device_status(self, info, username, device_name):
#         try:
#             user = User.objects.get(username=username)
#             device = UserDevice.objects.get(user=user, device_name=device_name)
#             return device.is_verified
#         except (User.DoesNotExist, UserDevice.DoesNotExist):
#             return False
#
#     def resolve_check_admin_status(self, info):
#         user = info.context.user
#         if not user.is_authenticated:
#             raise graphene.GraphQLError('Not authenticated')
#         return user
#
#     def resolve_validate_token(self, info):
#         if info.context.user.is_authenticated:
#             return AuthResponse(status='valid', message='Token is valid')
#         raise graphene.GraphQLError('Invalid token')
#
#
# class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
#     user = graphene.Field(UserType)
#     device_verified = graphene.Boolean()
#     token = graphene.String()
#
#     @classmethod
#     def Field(cls, *args, **kwargs):
#         cls._meta.arguments.update({
#             'deviceName': graphene.String(required=True)
#         })
#         return super().Field(*args, **kwargs)
#
#     @classmethod
#     def resolve(cls, root, info, **kwargs):
#         return cls(user=info.context.user, device_verified=False, token=None)
#
#     @classmethod
#     def mutate(cls, root, info, **kwargs):
#         username = kwargs.get(User.USERNAME_FIELD)
#         password = kwargs.get('password')
#         device_name = kwargs.get('deviceName', '')
#
#         user = User.objects.filter(username=username).first()
#
#         if user is None or not user.check_password(password):
#             raise Exception('Invalid username or password')
#
#         ip_address = info.context.META.get('REMOTE_ADDR')
#         location = get_location_from_ip(ip_address)
#
#         device, created = UserDevice.objects.get_or_create(
#             user=user,
#             device_name=device_name,
#             defaults={'ip_address': ip_address, 'location': location, 'is_verified': False}
#         )
#
#         if not device.is_verified:
#             verification_token = str(uuid.uuid4())
#             device.verification_token = verification_token
#             device.verification_expiry = timezone.now() + timedelta(seconds=settings.DEVICE_VERIFICATION_EXPIRY)
#             device.save()
#             send_verification_email(user, device, verification_token)
#             return cls(user=user, device_verified=False, token="verification_pending")
#
#         context = info.context
#         context.user = user
#         token = graphql_jwt.shortcuts.get_token(user)
#         return cls(token=token, user=user, device_verified=True)
#
#
# class VerifyDeviceMutation(graphene.Mutation):
#     class Arguments:
#         verification_token = graphene.String(required=True)
#
#     success = graphene.Boolean()
#     message = graphene.String()
#     token = graphene.String()
#
#     def mutate(self, info, verification_token):
#         try:
#             device = UserDevice.objects.get(
#                 verification_token=verification_token,
#                 is_verified=False
#             )
#
#             if device.verification_expiry and device.verification_expiry < timezone.now():
#                 return VerifyDeviceMutation(
#                     success=False,
#                     message="Le lien de vérification a expiré",
#                     token=None
#                 )
#
#             device.is_verified = True
#             device.verification_token = None
#             device.verification_expiry = None
#             device.save()
#
#             # Générer un nouveau token pour l'utilisateur
#             token = get_token(device.user)
#
#             return VerifyDeviceMutation(
#                 success=True,
#                 message="Appareil vérifié avec succès",
#                 token=token
#             )
#         except UserDevice.DoesNotExist:
#             return VerifyDeviceMutation(
#                 success=False,
#                 message="Token de vérification invalide",
#                 token=None
#             )
#         except Exception as e:
#             return VerifyDeviceMutation(
#                 success=False,
#                 message=f"Une erreur s'est produite : {str(e)}",
#                 token=None
#             )
#
#
# class RequestDeviceVerificationMutation(graphene.Mutation):
#     class Arguments:
#         device_id = graphene.ID(required=True)
#
#     success = graphene.Boolean()
#
#     @login_required
#     def mutate(self, info, device_id):
#         user = info.context.user
#         try:
#             device = UserDevice.objects.get(id=device_id, user=user, is_verified=False)
#             verification_token = str(uuid.uuid4())
#             device.verification_token = verification_token
#             device.verification_expiry = timezone.now() + timedelta(seconds=settings.DEVICE_VERIFICATION_EXPIRY)
#             device.save()
#             send_verification_email(user, device, verification_token)
#             return RequestDeviceVerificationMutation(success=True)
#         except UserDevice.DoesNotExist:
#             return RequestDeviceVerificationMutation(success=False)
#
#
# """
#     Mutation Class for Creating new User
# """

#
# """
#     Mutation Device Verification
# """
# class CompleteDeviceVerificationMutation(graphene.Mutation):
#     class Arguments:
#         username = graphene.String(required=True)
#         device_name = graphene.String(required=True)
#
#     success = graphene.Boolean()
#     token = graphene.String()
#     message = graphene.String()
#
#     def mutate(self, info, username, device_name):
#         try:
#             user = User.objects.get(username=username)
#             device = UserDevice.objects.get(user=user, device_name=device_name, is_verified=True)
#
#             # Utiliser la méthode correcte pour générer le token
#             token = get_token(user)
#
#             return CompleteDeviceVerificationMutation(
#                 success=True,
#                 token=token,
#                 message="Vérification complétée avec succès"
#             )
#         except (User.DoesNotExist, UserDevice.DoesNotExist):
#             return CompleteDeviceVerificationMutation(
#                 success=False,
#                 token=None,
#                 message="Appareil non trouvé ou non vérifié"
#             )
#
#

#     token_auth = ObtainJSONWebToken.Field()
#     verify_token = graphql_jwt.Verify.Field()
#     refresh_token = graphql_jwt.Refresh.Field()
#     verify_device = VerifyDeviceMutation.Field()
#     complete_device_verification = CompleteDeviceVerificationMutation.Field()
#     request_device_verification = RequestDeviceVerificationMutation.Field()
#     login = LoginMutation.Field()
#     verify_credentials = VerifyCredentialsMutation.Field()
#     register_sms_user = SMSUserRegisterMutation.Field()
#
#
# schema = graphene.Schema(query=Query, mutation=Mutation)
#
#
# """
#     Retrieving IP Location
#     Use ipapi.co API
#
#     # input:
#         - ip_address
# """
# def get_location_from_ip(ip_address):
#     response = requests.get(f'https://ipapi.co/{ip_address}/json/')
#     if response.status_code == 200:
#         data = response.json()
#         return f"{data.get('city', '')}, {data.get('country_name', '')}"
#     return ''
#
#
# """
#     Send email verification to admin
#     # input:
#         - user { username}
#         - device { name, ip_address, location }
#         - verification_token
# """
# def send_verification_email(user, device, verification_token):
#     subject = 'New Device Login Verification'
#     verification_url = f"{settings.FRONTEND_URL}/verify-device/{verification_token}"
#
#     message = f"""
#     User {user.username} has logged in from a new device:
#     Device Name: {device.device_name}
#     IP Address: {device.ip_address}
#     Location: {device.location}
#
#     To verify this device, click on the following link:
#     {verification_url}
#
#     This link will expire in 24 hours.
#     """
#
#     try:
#         for admin_name, admin_email in settings.ADMINS:
#             send_mail(
#                 subject,
#                 message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [admin_email],
#                 fail_silently=False
#             )
#     except Exception as e:
#         logger.info(f"Error sending email: {str(e)}")
#         raise
