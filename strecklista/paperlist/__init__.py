from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import Context, Template
from EmailUser.models import MyUser
from subprocess import Popen, PIPE
from tempfile import TemporaryDirectory
import os.path


with open('strecklista/paperlist/paperlist.tex') as file:
    tex_template = Template(file.read())

@login_required
def render_pdf(request):
    if request.GET.get("active", False):
        userlist = MyUser.objects.filter(active_singer=True).all().order_by('first_name')
    else:
        userlist = MyUser.objects.all().order_by('first_name')

    grouplist = []

    # Filter to only get used groups
    for user in userlist:
        if user.group is not None and user.group not in grouplist:
            grouplist.append(user.group)

    grouplist.sort(key=lambda x: x.sortingWeight, reverse=True)

    context = Context({
        'user_list' : userlist,
        'group_list' : grouplist,
    })
    tex = tex_template.render(context).encode('utf-8')

    pdf = render_tex(tex)

    response = HttpResponse(content_type='application/pdf')
    response.write(pdf)
    return response


def render_tex(tex):
    with TemporaryDirectory() as tempdir:
        # Create subprocess, supress output with PIPE and
        # run latex twice to generate the TOC properly.
        # Finally read the generated pdf.
        for _ in range(2):
            process = Popen(
                ['pdflatex', '-output-directory', tempdir],
                stdin=PIPE,
                stdout=PIPE,
            )
            process.communicate(tex)

        with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
            return f.read()


urlpatterns = [
    url(r'^', render_pdf, name='paperlist')
]
