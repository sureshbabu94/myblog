from django.contrib.auth.models import Group


class RoleMiddleware:  
    def __init__(self, get_response):  
        self.get_response = get_response  
      
    def __call__(self, request):  
        response = self.get_response(request)  
        return response 

    def process_view(self, request, view_func, *view_args, **view_kargs):

        if request.user.is_authenticated:
            request.role=None
            groups=request.user.groups.all()
            if groups:
                request.role = str(groups[0].name)


        else:
            request.role=None
