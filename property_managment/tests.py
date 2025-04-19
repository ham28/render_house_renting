# import json
# from django.test import TestCase
# from graphene_django.utils.testing import GraphQLTestCase
# from django.contrib.auth.models import User
# from decimal import Decimal
# from django.core.files.uploadedfile import SimpleUploadedFile
# from graphene.test import Client
# from graphql_jwt.testcases import JSONWebTokenTestCase
#
# from .schema import schema
# from .models import (
#     Address, Owner, Tenant, Property,
#     PropertyImage, Payment, LeaseContract
# )
#
#
# class GraphQLSchemaTestCase(GraphQLTestCase, JSONWebTokenTestCase):
#     GRAPHQL_URL = "/graphql/"
#     GRAPHQL_SCHEMA = schema
#
#     def setUp(self):
#         # Create test user
#         self.user = User.objects.create_user(
#             username="testuser",
#             email="test@example.com",
#             password="testpassword123"
#         )
#
#         # Create test address
#         self.address = Address.objects.create(
#             region="Test Region",
#             district="Test District",
#             commune="Test Commune",
#             quartier="Test Quartier",
#             address="123 Test Street"
#         )
#
#         # Create test owner
#         self.owner = Owner.objects.create(
#             f_name="Test",
#             l_name="Owner",
#             type="Individual",
#             phone="1234567890",
#             email="owner@example.com",
#             address=self.address,
#             user=self.user
#         )
#
#         # Create test property
#         self.property = Property.objects.create(
#             name="Test Property",
#             type="Apartment",
#             surface=Decimal("100.00"),
#             room_nbr=2,
#             bath_room_nbr=1,
#             construction_year="2020-01-01",
#             selling_price=Decimal("200000.00"),
#             renting_price=Decimal("1000.00"),
#             status=True,
#             renting_date="2023-01-01",
#             description="A test property",
#             property_condition="Good",
#             owner=self.owner,
#             address=self.address
#         )
#
#         # Create test tenant
#         self.tenant = Tenant.objects.create(
#             f_name="Test",
#             l_name="Tenant",
#             phone="0987654321",
#             email="tenant@example.com",
#             rent_amount=Decimal("1000.00"),
#             payment_method="Cash",
#             payment_deposit=Decimal("1000.00"),
#             guarantor="Test Guarantor"
#         )
#
#         # Create test property image
#         self.test_image = SimpleUploadedFile(
#             name="test_image.jpg",
#             content=b"file_content",
#             content_type="image/jpeg"
#         )
#         self.property_image = PropertyImage.objects.create(
#             description="Test Image",
#             image=self.test_image,
#             property=self.property
#         )
#
#         # Create test payment
#         self.payment = Payment.objects.create(
#             amount=Decimal("1000.00"),
#             payment_date="2023-02-01",
#             payment_type="Rent",
#             payment_method="Cash",
#             status="Paid",
#             tenant=self.tenant,
#             property=self.property
#         )
#
#         # Create test lease contract
#         self.lease_contract = LeaseContract.objects.create(
#             name="Test Lease",
#             lease_start_date="2023-01-01",
#             lease_end_date="2024-01-01",
#             rent_amount=Decimal("1000.00"),
#             contract_status=True,
#             rules="Test rules",
#             tenant=self.tenant,
#             property=self.property
#         )
#
#         # Authenticate user
#         self.client.authenticate(self.user)
#
#     # Query Tests
#     def test_query_all_tenants(self):
#         response = self.query(
#             '''
#             query {
#                 tenants {
#                     id
#                     fName
#                     lName
#                     email
#                 }
#             }
#             '''
#         )
#
#         content = json.loads(response.content)
#         self.assertResponseNoErrors(response)
#         self.assertEqual(len(content['data']['tenants']), 1)
#         self.assertEqual(content['data']['tenants'][0]['fName'], 'Test')
#         self.assertEqual(content['data']['tenants'][0]['lName'], 'Tenant')
#
#     def test_query_tenant_by_id(self):
#         response = self.query(
#             '''
#             query($id: Int!) {
#                 tenant(id: $id) {
#                     id
#                     fName
#                     lName
#                     email
#                 }
#             }
#             ''',
#             variables={'id': self.tenant.id}
#         )
#
#         content = json.loads(response.content)
#         self.assertResponseNoErrors(response)
#         self.assertEqual(content['data']['tenant']['fName'], 'Test')
#         self.assertEqual(content['data']['tenant']['lName'], 'Tenant')
#
#     def test_query_all_properties(self):
#         response = self.query(
#             '''
#             query {
#                 properties {
#                     id
#                     name
#                     type
#                     surface
#                 }
#             }
#             '''
#         )
#
#         content = json.loads(response.content)
#         self.assertResponseNoErrors(response)
#         self.assertEqual(len(content['data']['properties']), 1)
#         self.assertEqual(content['data']['properties'][0]['name'], 'Test Property')
#
#     def test_query_property_by_id(self):
#         response = self.query(
#             '''
#             query($id: Int!) {
#                 property(id: $id) {
#                     id
#                     name
#                     type
#                     surface
#                 }
#             }
#             ''',
#             variables={'id': self.property.id}
#         )
#
#         content = json.loads(response.content)
#         self.assertResponseNoErrors(response)
#         self.assertEqual(content['data']['property']['name'], 'Test Property')
#
#     def test_query_all_owners(self):
#         response = self.query(
#             '''
#             query {
#                 owners {
#                     id
#                     fName
#                     lName
#                     email
#                 }
#             }
#             '''
#         )
#
#         content = json.loads(response.content)
#         self.assertResponseNoErrors(response)
#         self.assertEqual(len(content['data']['owners']), 1)
#         self.assertEqual(content['data']['owners'][0]['fName'], 'Test')
#         self.assertEqual(content['data']['owners'][0]['lName'], 'Owner')
#
#     def test_query_owner_by_id(self):
#         response = self.query(
#             '''
#             query($id: Int!) {
#                 owner(id: $id) {
#                     id
#                     fName
#                     lName
#                     email
#                 }
#             }
#             ''',
#             variables={'id': self.owner.id}
#         )
#
#         content = json.loads(response.content)
#         self.assertResponseNoErrors(response)
#         self.assertEqual(content['data']['owner']['fName'], 'Test')
#         self.assertEqual(content['data']['owner']['lName'], 'Owner')
#
#     def test_query_all_lease_contracts(self):
#         response = self.query(
#             '''
#             query {
#                 leaseContracts {
#                     id
#                     name
#                     rentAmount
#                     contractStatus
#                 }
#             }
#             '''
#         )
#
#         content = json.loads(response.content)
#         self.assertResponseNoErrors(response)
#         self.assertEqual(len(content['data']['leaseContracts']), 1)
#         self.assertEqual(content['data']['leaseContracts'][0]['name'], 'Test Lease')
#
#     # Mutation Tests
#     def test_add_tenant_mutation(self):
#         response = self.query(
#             '''
#             mutation AddTenant(
#                 $fName: String!,
#                 $lName: String!,
#                 $phone: String!,
#                 $email: String!,
#                 $rentAmount: Decimal!,
#                 $paymentMethod: String!,
#                 $paymentDeposit: Decimal!,
#                 $guarantor: String!,
#                 $region: String!,
#                 $district: String!,
#                 $commune: String!,
#                 $quartier: String!,
#                 $address: String!
#             ) {
#                 addTenant(
#                     fName: $fName,
#                     lName: $lName,
#                     phone: $phone,
#                     email: $email,
#                     rentAmount: $rentAmount,
#                     paymentMethod: $paymentMethod,
#                     paymentDeposit: $paymentDeposit,
#                     guarantor: $guarantor,
#                     region: $region,
#                     district: $district,
#                     commune: $commune,
#                     quartier: $quartier,
#                     address: $address
#                 ) {
#                     tenant {
#                         id
#                         fName
#                         lName
#                         email
#                     }
#                     success
#                     message
#                 }
#             }
#             ''',
#             variables={
#                 'fName': 'New',
#                 'lName': 'Tenant',
#                 'phone': '1122334455',
#                 'email': 'new.tenant@example.com',
#                 'rentAmount': '1200.00',
#                 'paymentMethod': 'Bank Transfer',
#                 'paymentDeposit': '1200.00',
#                 'guarantor': 'New Guarantor',
#                 'region': 'New Region',
#                 'district': 'New District',
#                 'commune': 'New Commune',
#                 'quartier': 'New Quartier',
#                 'address': '456 New Street'
#             }
#         )
#
#         content = json.loads(response.content)
#         self.assertResponseNoErrors(response)
#         self.assertTrue(content['data']['addTenant']['success'])
#         self.assertEqual(content['data']['addTenant']['tenant']['fName'], 'New')
#         self.assertEqual(content['data']['addTenant']['tenant']['lName'], 'Tenant')
#
#     def test_add_property_mutation(self):
#         # Create a SimpleUploadedFile for the image
#         test_image = SimpleUploadedFile(
#             name="property_image.jpg",
#             content=b"file_content",
#             content_type="image/jpeg"
#         )
#
#         response = self.query(
#             '''
#             mutation AddProperty(
#                 $name: String!,
#                 $type: String!,
#                 $surface: Decimal!,
#                 $roomNbr: Int!,
#                 $bathRoomNbr: Int!,
#                 $constructionYear: Date,
#                 $sellingPrice: Decimal!,
#                 $rentingPrice: Decimal!,
#                 $status: Boolean!,
#                 $rentingDate: Date!,
#                 $description: String!,
#                 $propertyCondition: String!,
#                 $region: String!,
#                 $district: String!,
#                 $commune: String!,
#                 $quartier: String!,
#                 $address: String!,
#                 $ownerId: Int!,
#                 $propertyImages: [PropertyImageInput!]!
#             ) {
#                 addProperty(
#                     name: $name,
#                     type: $type,
#                     surface: $surface,
#                     roomNbr: $roomNbr,
#                     bathRoomNbr: $bathRoomNbr,
#                     constructionYear: $constructionYear,
#                     sellingPrice: $sellingPrice,
#                     rentingPrice: $rentingPrice,
#                     status: $status,
#                     rentingDate: $rentingDate,
#                     description: $description,
#                     propertyCondition: $propertyCondition,
#                     region: $region,
#                     district: $district,
#                     commune: $commune,
#                     quartier: $quartier,
#                     address: $address,
#                     ownerId: $ownerId,
#                     propertyImages: $propertyImages
#                 ) {
#                     property {
#                         id
#                         name
#                         type
#                     }
#                     success
#                     message
#                 }
#             }
#             ''',
#             variables={
#                 'name': 'New Property',
#                 'type': 'House',
#                 'surface': '150.00',
#                 'roomNbr': 3,
#                 'bathRoomNbr': 2,
#                 'constructionYear': '2018-01-01',
#                 'sellingPrice': '250000.00',
#                 'rentingPrice': '1500.00',
#                 'status': True,
#                 'rentingDate': '2023-03-01',
#                 'description': 'A new test property',
#                 'propertyCondition': 'Excellent',
#                 'region': 'New Region',
#                 'district': 'New District',
#                 'commune': 'New Commune',
#                 'quartier': 'New Quartier',
#                 'address': '789 New Street',
#                 'ownerId': self.owner.id,
#                 'propertyImages': [
#                     {
#                         'description': 'Front view',
#                         'image': test_image
#                     }
#                 ]
#             },
#             # For file uploads, we need to use the multipart_data parameter
#             multipart_data={
#                 'variables.propertyImages.0.image': test_image
#             }
#         )
#
#         content = json.loads(response.content)
#         self.assertResponseNoErrors(response)
#         self.assertTrue(content['data']['addProperty']['success'])
#         self.assertEqual(content['data']['addProperty']['property']['name'], 'New Property')
#
#     def test_add_owner_mutation(self):
#         response = self.query(
#             '''
#             mutation AddOwner(
#                 $fName: String!,
#                 $lName: String!,
#                 $type: String!,
#                 $phone: String!,
#                 $email: String!,
#                 $addressId: Int!,
#                 $userId: Int!
#             ) {
#                 addOwner(
#                     fName: $fName,
#                     lName: $lName,
#                     type: $type,
#                     phone: $phone,
#                     email: $email,
#                     addressId: $addressId,
#                     userId: $userId
#                 ) {
#                     owner {
#                         id
#                         fName
#                         lName
#                         email
#                     }
#                     success
#                     message
#                 }
#             }
#             ''',
#             variables={
#                 'fName': 'New',
#                 'lName': 'Owner',
#                 'type': 'Company',
#                 'phone': '5566778899',
#                 'email': 'new.owner@example.com',
#                 'addressId': self.address.id,
#                 'userId': self.user.id
#             }
#         )
#
#         content = json.loads(response.content)
#         self.assertResponseNoErrors(response)
#         self.assertTrue(content['data']['addOwner']['success'])
#         self.assertEqual(content['data']['addOwner']['owner']['fName'], 'New')
#         self.assertEqual(content['data']['addOwner']['owner']['lName'], 'Owner')
#
#     def test_add_payment_mutation(self):
#         response = self.query(
#             '''
#             mutation AddPayment(
#                 $amount: Decimal!,
#                 $paymentDate: Date!,
#                 $paymentType: String,
#                 $paymentMethod: String,
#                 $status: String,
#                 $tenantId: Int!,
#                 $propertyId: Int!
#             ) {
#                 addPayment(
#                     amount: $amount,
#                     paymentDate: $paymentDate,
#                     paymentType: $paymentType,
#                     paymentMethod: $paymentMethod,
#                     status: $status,
#                     tenantId: $tenantId,
#                     propertyId: $propertyId
#                 ) {
#                     payment {
#                         id
#                         amount
#                         status
#                     }
#                     success
#                     message
#                 }
#             }
#             ''',
#             variables={
#                 'amount': '1200.00',
#                 'paymentDate': '2023-03-01',
#                 'paymentType': 'Rent',
#                 'paymentMethod': 'Bank Transfer',
#                 'status': 'Paid',
#                 'tenantId': self.tenant.id,
#                 'propertyId': self.property.id
#             }
#         )
#
#         content = json.loads(response.content)
#         self.assertResponseNoErrors(response)
#         self.assertTrue(content['data']['addPayment']['success'])
#         self.assertEqual(content['data']['addPayment']['payment']['amount'], '1200.00')
#
#     def test_add_lease_contract_mutation(self):
#         # First, deactivate existing lease to avoid conflicts
#         self.lease_contract.contract_status = False
#         self.lease_contract.save()
#
#         response = self.query(
#             '''
#             mutation AddLeaseContract(
#                 $name: String,
#                 $leaseStartDate: Date!,
#                 $leaseEndDate: Date!,
#                 $rentAmount: Decimal!,
#                 $contractStatus: Boolean,
#                 $rules: String!,
#                 $tenantId: Int!,
#                 $propertyId: Int!
#             ) {
#                 addLeaseContract(
#                     name: $name,
#                     leaseStartDate: $leaseStartDate,
#                     leaseEndDate: $leaseEndDate,
#                     rentAmount: $rentAmount,
#                     contractStatus: $contractStatus,
#                     rules: $rules,
#                     tenantId: $tenantId,
#                     propertyId: $propertyId
#                 ) {
#                     leaseContract {
#                         id
#                         name
#                         rentAmount
#                     }
#                     success
#                     message
#                 }
#             }
#             ''',
#             variables={
#                 'name': 'New Lease Contract',
#                 'leaseStartDate': '2023-04-01',
#                 'leaseEndDate': '2024-04-01',
#                 'rentAmount': '1200.00',
#                 'contractStatus': True,
#                 'rules': 'New contract rules',
#                 'tenantId': self.tenant.id,
#                 'propertyId': self.property.id
#             }
#         )
#
#         content = json.loads(response.content)
#         self.assertResponseNoErrors(response)
#         self.assertTrue(content['data']['addLeaseContract']['success'])
#         self.assertEqual(content['data']['addLeaseContract']['leaseContract']['name'], 'New Lease Contract')
#
#     def test_add_property_images_mutation(self):
#         # Create a SimpleUploadedFile for the image
#         test_image = SimpleUploadedFile(
#             name="property_image2.jpg",
#             content=b"file_content",
#             content_type="image/jpeg"
#         )
#
#         response = self.query(
#             '''
#             mutation AddPropertyImages(
#                 $propertyId: Int!,
#                 $images: [PropertyImageInput!]!
#             ) {
#                 addPropertyImages(
#                     propertyId: $propertyId,
#                     images: $images
#                 ) {
#                     propertyImages {
#                         id
#                         description
#                     }
#                     success
#                     message
#                 }
#             }
#             ''',
#             variables={
#                 'propertyId': self.property.id,
#                 'images': [
#                     {
#                         'description': 'Back view',
#                         'image': test_image
#                     }
#                 ]
#             },
#             # For file uploads, we need to use the multipart_data parameter
#             multipart_data={
#                 'variables.images.0.image': test_image
#             }
#         )
#
#         content = json.loads(response.content)
#         self.assertResponseNoErrors(response)
#         self.assertTrue(content['data']['addPropertyImages']['success'])
#         self.assertEqual(content['data']['addPropertyImages']['propertyImages'][0]['description'], 'Back view')
#
#     def tearDown(self):
#         # Clean up uploaded files
#         self.property_image.image.delete()
#         # Clean up test data
#         self.lease_contract.delete()
#         self.payment.delete()
#         self.property_image.delete()
#         self.tenant.delete()
#         self.property.delete()
#         self.owner.delete()
#         self.address.delete()
#         self.user.delete()