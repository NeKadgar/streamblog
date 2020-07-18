from django.conf import settings


class SessionProfile(object):
    def __init__(self, request):
        self.session = request.session
        profile = self.session.get(settings.PROFILE_SESSION_ID)
        if not profile:
            profile = self.session[settings.PROFILE_SESSION_ID] = {"posts": [], "profiles": []}
        self.profile = profile

    def add_post(self, post_id):
        if post_id not in self.profile:
            posts = self.profile["posts"]
            posts.append({"post_id": post_id})
            self.profile["posts"] = posts

    def show(self):
        return self.profile

    def clear(self):
        del self.session[settings.PROFILE_SESSION_ID]