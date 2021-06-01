from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DeleteView
										
from .models import Problem, ProblemSubmission, Comment
from .forms import WriteSolution, WriteComment
#List of problems by section
class ProblemsList(ListView):
	template_name = 'problems/problems-list.html'
	context_object_name = 'problems_list'
	model = Problem
	def get_context_data(self, **kwargs):
			context = super().get_context_data(**kwargs)
			topic = self.kwargs.get('slug')
			problems = self.request.user.progress.opened_problems(topic = topic).filter(publish = True)
			problems_by_levels = []
			for k in range(1,6):
					problems_by_levels.append(problems.filter(level = k))
			context['problems_list'] = problems_by_levels
			context['solved_problems'] = self.request.user.progress.solved_problems.filter(chapter__topic=topic)
			context['wrong_problems'] = [
					sub.problem for sub in self.request.user.problemsubmission_set.filter(correct = False)
					]
			return context


def comment(request, sub):
	form = WriteComment(request.POST)
	if form.is_valid():
			cmnt = Comment(user = request.user,
											content = form.cleaned_data['content'],
											submission_id = sub
											)
			cmnt.save()

def problem_sub(request, **kwargs):
	template   = 'problems/problem-submit.html'
	qs  = Problem.objects.filter(
			chapter__in = request.user.progress.completed_chapters.filter(topic = kwargs['slug']),
			publish = True           )
	problem = get_object_or_404(qs, id = kwargs['pk'])
	problem_url = reverse('problems:submit', kwargs = {'pk': kwargs['pk'], 'slug':kwargs['slug']})
	context = {
			'problem': problem
	}
	sub = request.GET.get('sub')

	if request.user.progress.last_submissions.filter(problem = problem):
		for x in request.user.progress.last_submissions.filter(problem=problem):
				request.user.progress.last_submissions.remove(x)

	if problem in request.user.progress.solved_problems.all():
			#the student can see the solutions
			if not sub:
					sub = request.user.problemsubmission_set.filter(problem = problem).filter(correct = True).first().pk
					return redirect(problem_url + f'?sub={sub}')
			subs     = ProblemSubmission.objects.filter(problem = problem)
			all_sols = subs.filter(correct = True)
			# submissions of this user
			this_user_subs = subs.filter(student = request.user)
			#or from this_user_subs
			this_sub = this_user_subs.filter(id = int(sub)).first()
			if not this_sub:
					this_sub = get_object_or_404(all_sols, id  = int(sub))
			comments = Comment.objects.filter(submission_id = int(sub))
			context['all_sols'] = all_sols
			context['user_subs'] = this_user_subs
			context['this_sub'] = this_sub
			context['comments'] = comments
			if this_sub.student == request.user:
					context['cmnt'] = WriteComment()
			if request.method == 'POST':
					comment(request, sub)
					return redirect(problem_url + f'?sub={sub}')

	else:
		old_subs  = ProblemSubmission.objects.filter(student = request.user).filter(problem_id = kwargs['pk'])
		old_draft = old_subs.filter(status = 'draft')
		#?sub = 0 draft , ?sub != comment to the wrong or see a submission not corrected yet
			
		if sub == None:
					#not good
					context['user_subs'] = request.user.problemsubmission_set.filter(problem = problem).exclude(status = 'draft')
					context['show_btn'] = True
					if not old_draft:
							context['btn']     = 'إجابة جديدة'
					else:
							context['btn']     = 'إكمال المحاولة السابقة'
		elif sub == '0':
					context['show_btn'] = False
					if not old_draft:
							#create new sub
							if request.method == 'POST':
									form = WriteSolution(request.POST, request.FILES)
									if form.is_valid():
											submission = ProblemSubmission(
																			solution = form.cleaned_data['content'],
																			student = request.user,
																			problem = problem,
																			status = request.POST.get('sub'),
																			file = request.FILES.get('file'),
																			submited_on = timezone.now(),
																			ltr_dir = (request.POST.get('dir') == 'left')
																			)
											submission.save()
											if submission.status == 'draft':
													return redirect(problem_url)
											return redirect(problem_url + f'?sub={submission.id}')
							form = WriteSolution()
							context['form'] = form
							
					else:
							#there is a draft
							old_draft = old_draft[0]
							if request.method == 'POST':                   
									form = WriteSolution(request.POST, request.FILES)
									if form.is_valid():
											old_draft.solution = form.cleaned_data['content']
											old_draft.ltr_dir = (form.cleaned_data['dir'] == 'left')
											old_draft.submited_on = timezone.now()
											old_draft.status = request.POST.get('sub')
											if request.FILES.get('file'):
													old_draft.file = request.FILES.get('file')
											old_draft.save()
											if old_draft.status == 'draft':
													return redirect(problem_url)
											return redirect(problem_url+ f'?sub={old_draft.id}')
							form = WriteSolution(initial={'content':old_draft.solution})
							context['form'] = form
							context['ltr_dir'] = old_draft.ltr_dir
							context['show_del'] = True
							
		else:
					#show a submission of his 
					old_subs = old_subs.filter(status__in = ['submit','wrong','comment'])
					this_sub = get_object_or_404(old_subs, pk = int(sub))
					context['all_subs'] = old_subs
					context['this_sub'] = this_sub
					if this_sub.status in ['wrong', 'comment']:
							context['comments'] = Comment.objects.filter(submission_id = sub)
							context['cmnt'] = WriteComment()
					if request.method == 'POST':
							comment(request, sub)
							this_sub.status = 'comment'
							this_sub.save()
							return redirect(problem_url + f'?sub={sub}')
	return render(request, template, context)

class DeleteDraft(DeleteView):
	template_name       = 'problems/delete-draft.html'
	
	def get_object(self, **kwargs):
		problem = Problem.objects.get(pk = self.kwargs['pk'])
		return get_object_or_404(self.request.user.problemsubmission_set.filter(status = 'draft'), problem = problem)

	def get_success_url(self, **kwargs):
		problem = Problem.objects.get(pk = self.kwargs['pk'])
		return reverse_lazy('problems:submit', kwargs={
																		'slug': problem.chapter.topic,
																		'pk': problem.pk,
																									}
													)

class LastCorrectedSubs(ListView):
	template_name       = 'problems/last-subs.html'
	context_object_name = 'user_subs'
	def queryset(self, **kwargs):
		return self.request.user.progress.last_submissions.all() 

class LastSolvedProblems(ListView):
	template_name       = 'problems/last-solved.html'
	context_object_name = 'last_solved_problems'
	queryset = ProblemSubmission.objects.filter(
							correct = True).filter(
							submited_on__gte = timezone.now()-timedelta(days=7)).order_by(
							'-submited_on')
