from django.shortcuts import  reverse
from django.core.mail import send_mail
from django.views import generic
from .models import Lead
from .forms import LeadForm, CustomUserCreationForm

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LeadListView(generic.ListView):
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"

class LeadDetailView(generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"

class LeadCreateView(generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@gmail.com",
            recipient_list=["test2@gmail.com"],
        )
        return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadForm
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")

class LeadDeleteView(generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")