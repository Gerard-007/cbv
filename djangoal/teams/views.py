from django.shortcuts import render, get_object_or_404
from django.views.generic import (
	ListView, DetailView, 
	CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from . import mixins
from . import models


#def team_list(request):
#    teams = models.Team.objects.all()
#    return render(request, 'teams/team_list.html', {'teams': teams})


#def team_detail(request, pk):
#    team = get_object_or_404(models.Team, pk=pk)
#    return render(request, 'teams/team_detail.html', {'team': team})


class TeamListView(CreateView, ListView):
	context_object_name = 'teams'
	fields = ('name', 'practice_location', 'coach')
	model = models.Team
	template_name = 'teams/team_list.html'
	
	
#class TeamDetailView(DetailView):
#	model = models.Team

class TeamDetailView(DetailView, UpdateView):
	context_object_name = 'team'
	fields = ('name', 'practice_location', 'coach')
	model = models.Team
	template_name = 'teams/team_detail.html'
	
	
class TeamCreateView(LoginRequiredMixin, mixins.PageTitleMixin, CreateView):
	fields = ('name', 'practice_location', 'coach')
	model = models.Team
	#Creating page title as attribute from mixins.PageTitleMixin
	page_title = "Create a new team" 
	
	def get_initial(self):
		
#		This function retains the name of
#		current user that is creating the team (coach)

		initial = super().get_initial()
		initial['coach'] = self.request.user.pk
		return initial
	
	
class TeamUpdateView(LoginRequiredMixin, mixins.PageTitleMixin, UpdateView):
	fields = ('name', 'practice_location', 'coach')
	model = models.Team
	
	#Creating page title as function from mixins.PageTitleMixin
	def get_page_title(self):
		obj = self.get_object()
		return "Update {}".format(obj.name)
	
	
class TeamDeleteView(LoginRequiredMixin, DeleteView):
	model = models.Team
	success_url = reverse_lazy('teams:list')
	
	def get_queryset(self):
		
#		This method ensures that no user deletes 
#		any form except if couch or super_user()

		if not self.request.user.is_super:
			return self.model.objects.filter(coach=self.request.user)
		return self.model.objects.all()
	
	
	
	