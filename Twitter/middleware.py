from django.contrib.auth import logout
from django.http import HttpResponse

from Twitter.models import RequestData, LoggedInUser


class RequestMonitorMiddleware(object):
    def __init__(self, get_response):
        self.n = 2000
        self.h = 20
        self.d = 10
        self.blocked_ips = []
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
        if ip:
            ip = ip.split(", ")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "")

        browser = request.user_agent.browser.family + request.user_agent.browser.version_string
        data = RequestData.objects.create(ip=ip, browser=browser)

        if ip in self.blocked_ips:
            return HttpResponse("Error: Blocked IP (" + ip + ")")

        auth_requests = RequestData.objects.filter(ip=ip, authorized=True).order_by('-time')
        unauth_requests = RequestData.objects.filter(ip=ip, authorized=False).order_by('-time')

        if auth_requests.count() > self.n:
            block = self.check_distance(auth_requests[:self.n + 1], self.h)
            if block:
                self.blocked_ips.append(ip)
                return HttpResponse("Error: Blocked IP (" + ip + ")")

        if unauth_requests and unauth_requests.count() > self.n:
            block = self.check_distance(auth_requests[:self.n + 1], self.d)
            if block:
                self.blocked_ips.append(ip)
                return HttpResponse("Error: Blocked IP (" + ip + ")")

        request.data_object = data
        return self.get_response(request)

    def check_distance(self, requests, distance):
        timestamps = list(requests.values_list("time", flat=True))
        block = True
        for i in range(1, len(timestamps)):
            diff = timestamps[i - 1] - timestamps[i]
            if diff.total_seconds() * 1000 > distance:
                block = False
                break
        return block


class OneSessionPerUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                logged_in = LoggedInUser.objects.get(user=request.user)
            except:
                logged_in = LoggedInUser.objects.create(user=request.user)

            stored_session_key = logged_in.session_key
            if stored_session_key and stored_session_key != request.session.session_key:
                logout(request)

            logged_in.session_key = request.session.session_key
            logged_in.save()

        response = self.get_response(request)
        return response
