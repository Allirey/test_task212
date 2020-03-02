from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Article, Comment
from .forms import CommentForm
from .tasks import send_notification_email


def home(request):
    return render(request, 'articles/home.html')


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles/article_list.html'
    login_url = 'login'
    queryset = Article.objects.filter(status=Article.Status.PUBLISHED)


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.all()
        return context

    def post(self, request, **kwargs):
        article = get_object_or_404(Article, id=kwargs.get('pk'), status=Article.Status.PUBLISHED)

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user
            new_comment.save()

            send_notification_email.delay(article.author.id, new_comment.id)
        return redirect(reverse('article_detail', args=[kwargs.get('pk')]))


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'body',)
    template_name = 'articles/article_edit.html'
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'articles/article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'articles/article_new.html'
    fields = ('title', 'body')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user

        if form.instance.author.has_perm('articles.publish_without_moderation'):
            form.instance.status = Article.Status.PUBLISHED
        return super().form_valid(form)
