from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .models import ContactMessage

SERVICES = [
    "Fuel delivery & bulk fuel supply", "Oil & gas services", "Logistics & freight",
    "Car hire & transportation", "Building materials", "General construction",
    "Computers, ICT & networking", "Electrical supplies", "Furniture",
    "Agro trading & food supplies", "Safety equipment", "Other enquiry",
]

def home(request):
    return render(request, "home.html", {"services": SERVICES[:6]})

def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, "services.html", {"services": SERVICES})

@require_http_methods(["GET", "POST"])
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        service = request.POST.get("service", "").strip()
        subject = request.POST.get("subject", "").strip()
        body = request.POST.get("message", "").strip()

        if not all([name, email, subject, body]):
            messages.error(request, "Please complete all required fields and try again.")
        else:
            enquiry = ContactMessage.objects.create(
                name=name, email=email, phone=phone, service=service,
                subject=subject, message=body
            )
            # Database storage always happens; email notification is optional.
            if settings.EMAIL_HOST and settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                try:
                    send_mail(
                        subject=f"Website enquiry: {enquiry.subject}",
                        message=(
                            f"From: {enquiry.name}\nEmail: {enquiry.email}\nPhone: {enquiry.phone}\n"
                            f"Service: {enquiry.service}\n\n{enquiry.message}"
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
                        fail_silently=True,
                    )
                except Exception:
                    pass
            messages.success(request, "Thank you. Your enquiry has been received. Our team will contact you.")
            return redirect("contact")
    return render(request, "contact.html", {"services": SERVICES})
