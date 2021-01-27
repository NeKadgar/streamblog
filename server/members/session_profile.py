from django.conf import settings
from blog.models import Post
import random


class SessionProfile(object):
    def __init__(self, request):
        self.session = request.session
        profile = self.session.get(settings.PROFILE_SESSION_ID)
        if not profile:
            profile = self.session[settings.PROFILE_SESSION_ID] = {"posts": [], "profiles": []}
        self.profile = profile

    def add_post(self, post_id):
        if post_id not in self.profile["posts"]:
            posts = self.profile["posts"]
            posts.append(post_id)
            self.profile["posts"] = posts
            self.save()

    def add_profile(self, profile_id):
        if profile_id not in self.profile["profiles"]:
            profiles = self.profile["profiles"]
            profiles.append(profile_id)
            self.profile["profiles"] = profiles
            self.save()

    def get_tags(self):
        popular_tags = [tag.name for tag in list(Post.tags.most_common()[:4])]
        posts = list(Post.objects.filter(id__in=self.profile["posts"]))
        tags = [tag for post in posts for tag in post.get_name_tags()]
        c = len(tags)
        if len(tags) > 5:
            c = len(tags)//3
        random_tags = random.sample(tags, len(tags))
        return popular_tags+random_tags

    def get_recommendations(self):
        tags = self.get_tags()
        posts = list(Post.objects.filter(tags__name__in=tags))
        random_posts = random.sample(posts, 5)
        return {"left": random_posts[0], "middle": random_posts[1:4], "right":random_posts[4]}

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def show(self):
        return self.profile

    def clear(self):
        del self.session[settings.PROFILE_SESSION_ID]
