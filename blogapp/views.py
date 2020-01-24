from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

def home(request):
	context = {'posts': Post.objects.all()}
	return render(request,'blogapp/home.html',context)

class PostListView(ListView): #class base view Home List View
	model = Post
	template_name = 'blogapp/home.html'#<app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5	

class UserPostListView(ListView): #class base view User List View
	model = Post
	template_name = 'blogapp/user_posts.html'#<app>/<model>_<viewtype>.html
	context_object_name = 'posts'

	paginate_by = 5	

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView): #class base view Post List View
	model = Post
	
class PostCreateView(LoginRequiredMixin,CreateView):
	model = Post
	fields = ['title','content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Post
	fields = ['title','content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post =self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Post
	success_url = '/'
	def test_func(self):
		post =self.get_object()
		if self.request.user == post.author:
			return True
		return False

def about(request):
	return render(request,'blogapp/about.html')
