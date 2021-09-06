from rest_framework import generics
from rest_framework import viewsets
#　新規ユーザ作成時のjwt認証の対応のために必須
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Room, WithComment


