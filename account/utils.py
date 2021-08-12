from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect

def get_next_redirect(request):
    next = request.GET.get('next')
    if next:
        # Verify the next data if it belongs to our domain
        if next.find('.') == -1:
            return redirect(next)
    return



def send_email(email, subject, message, fail=True):
    print(message)
    val = send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email], fail_silently=fail)
    return bool(val)