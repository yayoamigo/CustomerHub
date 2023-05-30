from django.shortcuts import  reverse
from django.core.mail import send_mail
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lead, Agent, Category, FollowUp
from .forms import LeadForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm, CategoryModelForm, FollowUpModelForm
from agents.mixins import OrganisorAndLoginRequiredMixin
import datetime

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LeadListView(LoginRequiredMixin ,generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization )
            print(queryset)
            queryset = queryset.filter(agent__user=user)
            

        return queryset
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset
            })
        return context


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization )
            
            queryset = queryset.filter(agent__user=user)
            

        return queryset


class LeadCreateView(OrganisorAndLoginRequiredMixin , generic.CreateView):
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

class LeadUpdateView(OrganisorAndLoginRequiredMixin , generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadForm
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")

class LeadDeleteView(OrganisorAndLoginRequiredMixin , generic.DeleteView):
    template_name = "leads/lead_delete.html"
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    

class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
        
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organisation
            )

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset


class CategoryCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organization = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/category_update.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset


class CategoryDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/category_delete.html"

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})

    def form_valid(self, form):
        lead_before_update = self.get_object()
        instance = form.save(commit=False)
        converted_category = Category.objects.get(name="Converted")
        if form.cleaned_data["category"] == converted_category:
            # update the date at which this lead was converted
            if lead_before_update.category != converted_category:
                # this lead has now been converted
                instance.converted_date = datetime.datetime.now()
        instance.save()
        return super(LeadCategoryUpdateView, self).form_valid(form)

class FollowUpCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "leads/followup_create.html"
    form_class = FollowUpModelForm

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowUpCreateView, self).get_context_data(**kwargs)
        context.update({
            "lead": Lead.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        lead = Lead.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.lead = lead
        followup.save()
        return super(FollowUpCreateView, self).form_valid(form)


class FollowUpUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/followup_update.html"
    form_class = FollowUpModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizor:
            queryset = FollowUp.objects.filter(lead__organization=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(lead__organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(lead__agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().lead.id})


class FollowUpDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/followup_delete.html"

    def get_success_url(self):
        followup = FollowUp.objects.get(id=self.kwargs["pk"])
        return reverse("leads:lead-detail", kwargs={"pk": followup.lead.pk})

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = FollowUp.objects.filter(lead__organization=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(lead__organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(lead__agent__user=user)
        return queryset
