from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Post, Community, Blocked


class PostCreationView(UserPassesTestMixin, CreateView):
    model = Post
    template_name = 'conetnts/create-post.html'
    fields = ['title', 'image', 'body']

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.author = self.request.user
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        self.obj.community = self.community
        self.obj.save()
        return HttpResponseRedirect(reverse('contents:post_list',
                                    args=[self.community.slug]))

    def test_func(self):
        try:
            obj = Blocked.objects.get(user=self.request.user,
                                      community=self.community)
        except Blocked.DoesNotExist:
            return True
        return False
