# [Strecklista](http://streque.se)

Website written using django and python 3.5


## Getting Started
Make sure you have `python3` and `pipenv` installed, and create the environment:
```sh
pipenv install
```
then start a new shell with the environment:
```sh
pipenv shell
```

You also need pdflatex in your path to be able to generate PDF's.
"apt install texlive-full" works, but you can probably skip a lot of the
packages and documentation and get by anyways.

## Developing

1. Create the database and apply the migrations with:
```sh
python3 manage.py migrate
```

2. You need a user to access most parts of the site. Create a new superuser with:
```sh
python3 manage.py createsuperuser
```

3. Start the webserver by running
```sh
python3 manage.py runserver
```

4. Visit http://localhost:8000 and log in.

### LiveReload
You can run a [LiveReload server](https://github.com/tjwalch/django-livereload-server)
during development, which when combined with a [LiveReload extension](https://chrome.google.com/webstore/detail/livereload/jnihajbhpnppcggbcgedagnkighmdlei?utm_source=chrome-app-launcher-info-dialog)
will refresh the current page when any file is changed. It is enabled by
default when `DEBUG = True`. Just start the server in another terminal:

```sh
python3 manage.py livereload
```

### Formatting
To keep the code formatting consistent, run this command to auto-format all
changed Python files in-place before committing them.

```sh
git diff --name-only | grep '.py' | xargs yapf -i
```

### Tests
Place your tests next to the code they're testing. Run all tests with:

```sh
python3 ./manage.py test --pattern="*_test.py"
```

## Cyclic dependency fix
You will get a error complaining about a cyclic dependency when runnig the
first migration. To fix this, comment out the reference to "strecklista.Group"
in the EmailUser.models.MyUser class, run the migration, remove the comment and
migrate again

## Email
As this project uses gmail for outgoing mail you need to enable "less secure
devices" on the google account as [described here](http://stackoverflow.com/questions/26697565/django-smtpauthenticationerror).
This should only be needed the first time the website is set up on a new server.

## Groups for new users.
When new users are registererd via the /register page they are automatically
placed in the group with the lowest sorting weight.
