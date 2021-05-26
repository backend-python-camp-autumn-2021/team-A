from rest_framework import serializers

from users.models import User, Customer,Supplier


class ChangePassswordSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
        )
    password = serializers.CharField(write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate_password2(self, value):
        if self.initial_data['password'] == value:
            return value
        raise serializers.ValidationError('Not Equal')

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class UpdateSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['username', 'first_name', 'last_name', 'profile_picture', 'bank_account']


class UpdateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'profile_picture', 'phone', 'gender']


class RegisterSupplierSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    password = serializers.CharField(write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model = Supplier
        fields = ['username', 'password', 'password2',
        'email', 'first_name', 'last_name', 'bank_account',
        'profile_picture']

    def validate_password2(self, value):
        if self.initial_data['password'] == value:
            return value
        raise serializers.ValidationError('Not Equal Password')

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        supplier = Supplier.objects.create(**validated_data)
        supplier.set_password(password)
        supplier.save()
        return supplier


class RegisterCustomerSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    password = serializers.CharField(write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model = Customer
        fields = ['username', 'password', 'password2',
        'email', 'first_name', 'last_name', 'gender',
        'profile_picture', 'phone']

    def validate_password2(self, value):
        if self.initial_data['password'] == value:
            return value
        raise serializers.ValidationError('Not Equal Password')

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        customer = Customer.objects.create(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    password2 = serializers.CharField(write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def validate(self, attrs):
        if attrs['password1'] == attrs['password2']:
            return attrs
        else:
            raise serializers.ValidationError('Not equal')


    