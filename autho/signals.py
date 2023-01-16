from autho.models import OTPToken
from django.db.models import signals
from django.dispatch import receiver


@receiver(signals.post_save, sender=OTPToken)
def invalidate_previous_tokens(sender, instance, created, **kwargs):
    """
    Invalidates all previously issued tokens of that type when a new one is created, used, or anything like that.
    """
    print("I am running....")
    if isinstance(instance, OTPToken):
        OTPToken.objects.active().filter(user=instance.user).exclude(
            id=instance.id
        ).update(is_active=False)
