from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from appnay.models import AccountUser

@receiver(post_save, sender=AccountUser, dispatch_uid="nim")
def check_nim(sender, instance, created, **kwargs):
    # Check if student number or email already exists
    student_number_exists = AccountUser.objects.filter(account_user_student_number=instance.account_user_student_number).exists()
    email_exists = User.objects.filter(username=instance.email).exists()

    if student_number_exists or email_exists:
        # Logging or some other form of handling can be added here
        print("Nim / email Telah digunakan!")
    else:
        if created:
            User.objects.create(username=instance.email)
            AccountUser.objects.create(
                account_user_fullname=instance.account_user_fullname,
                account_user_student_number=instance.account_user_student_number,
            )
        else:
            # Handle the scenario where the instance is updated
            print("Instance updated without duplication")
