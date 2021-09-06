from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
# Create your models here.

def upload_avater_path(instance, filename):
    #配列の最後の文字列を取得する(jpeg等)
    ext = filename.split('.')[-1]
    #"avatars/idnickname.ext"となる
    return '/'.join(['avatars', str(instance.userProfile.id) + str(instance.nickName) + str(".") + str(ext)])

def get_deleted_user():
    return User.objects.get_or_create(name="削除されたユーザ")[0]

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Email is must')

        # emailの文字列で正規化する
        user = self.model(email=self.normalize_email(email))
        # passwordの文字列をhash化する
        user.set_password(password)
        # dbに新規ユーザを作成し登録する。
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        # staff権限
        user.is_staff = True
        # superuser権限
        user.is_superuser = True
        user.save(using=self._db)

        return user

# cloneアプリを使用するユーザ
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    # アカウントの切り替えはON
    is_active = models.BooleanField(default=True)
    # スタッフ権限はいらない
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    # ユーザネームの表示、デフォルトはusername
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Profile(models.Model):
    nickName = models.CharField(max_length=20)
    #djangoのuserモデルとuserProfileをonetooneでつなぐ。onetooneで繋いでいるユーザが削除された場合、参照している側も削除する
    userProfile = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='userProfile', on_delete=models.CASCADE)

    created_on = models.DateTimeField(auto_now_add=True)

    #upload_avater_path->別で定義
    img = models.ImageField(blank=True, null=True, upload_to=upload_avater_path)

    # # 外部参照で、BikeNameテーブルを参照できる様に変更
    # bikeName = models.CharField(max_length=20, null=True)
    # # 外部参照で、Prefectureテーブルを参照できる様に変更
    # prefecture = models.CharField(max_length=10)
    # # 外部参照で、localテーブルを参照できる様に変更
    # local = models.CharField(max_length=10)
    #
    # # likeBikeはあとで作成
    #
    # incom = models.IntegerField(default=0)
    #
    # toukou = models.IntegerField(default=0)
    def __str__(self):
        return self.nickName

class Room(models.Model):
    id = models.AutoField(primary_key=True)

    createUser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='createUser', on_delete=models.DO_NOTHING)

    joinUser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="joinUser", on_delete=models.DO_NOTHING)

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class WithComment(models.Model):
    id = models.AutoField(primary_key=True)

    userId = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='userId', on_delete=models.DO_NOTHING)

    roomId = models.ForeignKey(Room, related_name="roomId", on_delete=models.CASCADE)

    comment = models.CharField(max_length=200)

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

