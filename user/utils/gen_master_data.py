from user.models import User

def gen_master(apps, schema_editor):
    User.objects.create_superuser(
        email='admin@email.com',
        username='admin',
        password='admin',
        gender=User.GenderChoices.MALE
    )

    User.objects.create_user(
        email='user1@email.com',
        username='user1',
        password='user1',
        gender=User.GenderChoices.FEMALE
    )