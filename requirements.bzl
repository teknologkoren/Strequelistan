requirements = [
    "django>=1.9",
    "django-livereload-server==0.2.3",
    "django-widget-tweaks==1.4.1",

    # Image processing
    "Pillow==4.0.0",
    "django-appconf==1.0.2",
    "django-imagekit==4.0.1",
    "pilkit==2.0",

    # Api stuff
    "djangorestframework==3.6.2",
    "django-cors-headers==2.1.0", # Using multiple servers in parallel.
    "markdown==2.6.8",
    "django-filter==1.0.2",

    # Gives access to a nicer shell with models already imported (shell_plus)
    "django-extensions==1.7.8",
    "django-progressive-web-app==0.1",
]