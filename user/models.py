from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.shortcuts import resolve_url


class UserManager(BaseUserManager):
    # 일반 사용자
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수 항목입니다.")
        if not username:
            raise ValueError("이름은 필수 함옥입니다.")
        if not password:
            raise ValueError("비밀번호는 필수 항목입니다.")

        user = self.model(
            email=UserManager.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)

        return user

    # 관리자
    def create_superuser(self, email, username, password, **extra_fields):
        user = self.model(
            email=email,
            username=username,
        )

        user.set_password(password)
        user.full_clean()

        user.is_admin = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    class GenderChoices(models.TextChoices):
        MALE = 'M', '남성'
        FEMALE = 'F', '여성'

    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True
    )

    username = models.CharField(
        verbose_name='UserName',
        max_length=50,
        unique=True
    )

    gender = models.CharField(
        'Gender',
        max_length=2,
        blank=True,
        choices=GenderChoices.choices
    )

    profile_img = models.ImageField(
        '프로필 이미지',
        blank=True,
        upload_to='user/profile_img/%Y/%m/%d',
        help_text='gif, png, jpg 이미지 파일을 업로드 해주세요.'
    )

    reg_date = models.DateTimeField(
        '생성 날짜',
        auto_now_add=True
    )

    update_date = models.DateTimeField(
        '수정 날짜',
        auto_now=True
    )

    last_login = models.DateTimeField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        '활성화 상태',
        default=True
    )

    is_admin = models.BooleanField(
        '관리자 권한',
        default=False
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    class Meta:
        db_table = 'user'
        ordering = ['-id']
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'

    def __str__(self):
        return f'{self.email} :: {self.username}'

    def get_full_name(self):
        return self.username

    def get_shrot_name(self):
        return self.username

    @property
    def profile_img_url(self) -> str:
        if self.profile_img:
            return self.profile_img.url
        return resolve_url('user/profile_img/default_img.jpg', data=self.username)
