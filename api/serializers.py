from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import WithComment,Room,Profile

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        # activeなユーザモデルを取得
        model = get_user_model()
        fields = ('id', 'email', 'password')
        # クライアントから読み込むことはできない様にしている
        extra_kwargs = {
            'email': {'wirte_only': True},
            'password': {'write_only': True}}

    # createメソッドをオーバーライドしている
    def create(self, validated_data):
        # models.pyのUserクラスのcreate_userメソッドを呼び出す。
        user = get_user_model().objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):

    created_on = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model=Profile
        fields = ('id', 'nickName', 'userProfile', 'created_on', 'img')
        # userProfileはリードオンリーにする。
        # userProfileはUserモデルと外部参照の形をとるため、変更してはいけない。
        extra_kwargs = {'userProfile': {'read_only': True}}

class RoomSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'createUser', 'joinUser', 'created_on')
        extra_kwargs = {
                        'createUser': {'read_only': True},
                        'joinUser': {'read_only': True}
        }

class WithCommentSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = WithComment
        fields = ('id', 'userId', 'roomId', 'comment', 'created_on')
        extra_kwargs = {
                        'userId': {'read_only': True},
                        'roomId': {'read_only': True}
        }