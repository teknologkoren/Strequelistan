from django.http import Http404
from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from EmailUser.models import MyUser
from strecklista.models import Group, Transaction, PriceGroup, Product, ProductCategory, PriceLimit, Quote
from django.contrib.auth.decorators import login_required
from rest_framework import authentication, permissions
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from datetime import datetime, timedelta

class IsAdminOrReadOnly(permissions.BasePermission):

  def has_permission(self, request, view):
    # Can view
    if request.user.is_authenticated and request.method in permissions.SAFE_METHODS:
      return True

    # Can edit
    if request.user.is_admin:
      return True

    return False

  def has_object_permission(self, request, view, obj):

    #Can view
    if request.user.is_authenticated and request.method in permissions.SAFE_METHODS:

      return True

    #Can edit
    if request.user.is_admin:
      return True

    return False

class GroupSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  name = serializers.CharField(max_length=50, required=True)
  description = serializers.CharField(max_length=500, allow_blank=True, default="")
  sortingWeight = serializers.IntegerField(default=0)

  def create(self, validated_data):
    g = Group()
    g.name = validated_data.get('name', g.name)
    g.description = validated_data.get('description', g.description)
    g.sortingWeight = validated_data.get('sortingWeight', g.sortingWeight)
    g.save()
    return g

  def update(self, instance, validated_data): #TODO: check if the if statements are neede
    if validated_data.get('name', instance.description):
      instance.name = validated_data.get('name', instance.name)
    if validated_data.get('description', instance.description):
      instance.description = validated_data.get('description', instance.description)
    if validated_data.get('sortingWeight', instance.sortingWeight):
      instance.description = validated_data.get('description', instance.description)
    instance.save()

    return instance

class GroupViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAdminOrReadOnly,)
  queryset = Group.objects.all()
  serializer_class = GroupSerializer


class ProductCategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = ProductCategory
    fields = ('name', 'description', 'sortingWeight',)

class ProductCategoryViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAdminOrReadOnly,)
  queryset = ProductCategory.objects.all()
  serializer_class = ProductCategorySerializer


class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = ('name', 'description', 'sortingWeight', 'priceGroup', 'productCategory',)

class ProductAdminSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = ProductSerializer.Meta.fields + ('is_active',)


class ProductViewSet(viewsets.ViewSet):
  permission_classes = (IsAdminOrReadOnly,)
  queryset = Product.objects.all().filter(is_active=True)
  serializer_class = ProductSerializer

  def list(self, request, *args, **kwargs):
    if request.user.is_admin:
      self.queryset = Product.objects.all()
      self.serializer_class = ProductAdminSerializer(self.queryset, context={'request': request}, many=True)

    else:
      self.serializer_class = ProductSerializer(self.queryset, context={'request': request}, many=True)

    return Response(self.serializer_class.data)


    return

class PriceGroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = PriceGroup
    fields = ('name',  'sortingWeight', 'defaultPrice', 'priceLimits',)

class PriceGroupViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAdminOrReadOnly,)
  queryset = PriceGroup.objects.all()
  serializer_class = PriceGroupSerializer


class PriceLimitSerializer(serializers.ModelSerializer):
  class Meta:
    model = PriceLimit
    fields = ('name', 'limit', 'multiplier',)

class PriceLimitViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAdminOrReadOnly,)
  queryset = PriceLimit.objects.all()
  serializer_class = PriceLimitSerializer


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = (
            'text',
            'who',
            'timestamp',
            'submittedBy',
        )


class RandomQuoteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Quote.objects.all().order_by('?')[:1]
    serializer_class = QuoteSerializer


class QuoteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


class TransactionSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  user = serializers.PrimaryKeyRelatedField(queryset=MyUser.objects.all())
  amount = serializers.IntegerField()
  timestamp = serializers.DateTimeField()


class TransactionAdminSerializer(TransactionSerializer):

  id = serializers.IntegerField(read_only=True)
  user = serializers.PrimaryKeyRelatedField(queryset=MyUser.objects.all())
  amount = serializers.IntegerField()
  timestamp = serializers.DateTimeField()
  returned = serializers.BooleanField()


class TransactionViewSet(viewsets.ViewSet):
  permission_classes = (IsAdminOrReadOnly,)
  serializer_class = TransactionSerializer
  queryset = Transaction.objects.all()


  def list(self, request):

    if request.user.is_admin:
      queryset = Transaction.objects.all()
    else:

      time_threshold = datetime.now() - timedelta(minutes=30)

      queryset = Transaction.objects.all().filter(returned=False, admintransaction=False, timestamp__gte=time_threshold)
      queryset = queryset[:10] #Limit to the first 10 for non admins

    if request.user.is_admin:
      serializer = TransactionAdminSerializer(queryset, context={'request': request}, many=True)
    else:
      serializer = TransactionSerializer(queryset, context={'request': request}, many=True)

    return Response(serializer.data)




# Create your views here.
class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = MyUser
    fields = ('id', 'first_name', 'last_name', 'nickname', 'email', 'phone_number', 'avatar', 'group')


# Create your views here.
class UserSerializerAdmin(serializers.ModelSerializer):
  class Meta:
    model = MyUser
    fields = UserSerializer.Meta.fields + ('weight', 'balance')



class UserViewSet(viewsets.ViewSet):


  permission_classes = (IsAdminOrReadOnly,)

  def list(self, request):

    queryset = MyUser.objects.all()

    if(request.user.is_admin):
      serializer = UserSerializerAdmin(queryset, context={'request':request}, many=True)

    else:
      serializer = UserSerializer(queryset, context={'request':request}, many=True)

    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    print("retrieve")
    print("pk: %i", pk)
    queryset = MyUser.objects.all()
    user = get_object_or_404(queryset, pk=pk)

    print(request.user.id)

    if request.user.id is int(pk) or request.user.is_admin:
      print("yay")
      serializer = UserSerializerAdmin(user, context={'request':request})

    else:
      print("nay")
      serializer = UserSerializer(user, context={'request':request})
    return Response(serializer.data)

  queryset = MyUser.objects.all()
