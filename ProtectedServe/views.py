from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.static import serve
from alge.settings import MEDIA_ROOT
# Create your views here.

# More info on how to set up with Nginx here:
# http://stackoverflow.com/questions/39744587/serve-protected-media-files-with-django

@login_required(login_url='/login/')
def protectedFileServe(request, file):

    path = "/protected/%s" %(file)

    return serve(request, path, document_root = MEDIA_ROOT, show_indexes=False)