from rest_framework import serializers

from apps.authentication.models import User


class UserCreationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """

    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name",
            "phone", "email", "password", "password2"
        )

    def create(self, validated_data: dict) -> User:
        """
        Method creates validate passwords and creates user if passwords match
        :param validated_data: dict
        :return: User
        """

        if validated_data["password"] == validated_data["password2"]:
            user = User.objects.create(
                username=validated_data["username"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                phone=validated_data["phone"],
                email=validated_data["email"],
            )
            user.set_password(validated_data["password"])
            user.save()
            return user


class UserActivitySerializer(serializers.ModelSerializer):
    """
    Serialize user activity data
    """

    user_id = serializers.CharField(source="id")

    class Meta:
        model = User
        fields = ("user_id", "last_login", "last_activity")
