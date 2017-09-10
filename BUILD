load("@io_bazel_rules_pex//pex:pex_rules.bzl", "pex_binary")
load("//:requirements.bzl", "requirements")


pex_binary(
    name = "streque",
    main = "manage.py",
    srcs = [
        "manage.py",
    ],
    deps=[':bare'],
    reqs=requirements,
    # zip_safe=False unzips the pex file before running. This enables more
    # flexibility when using a resource file (e.g. executing it with bash).
    # This is the reason why we choose pex over subpar.
    zip_safe=False,
    # default_python_version = "PY3",
)


py_library(
    name='src',
    deps=[':bare', '@requirements//:libraries'],
    srcs_version = "PY2AND3",
)


py_library(
    name='bare',
    srcs=glob([
        'manage.py',
        'alge/*.py',
        'api/*.py',
        'EmailUser/**/*.py',
        'password_reset_email/**/*.py',
        'ProtectedServe/**/*.py',
        'strecklista/**/*.py',
    ]),
    srcs_version = "PY2AND3",
    data=glob(['resources/*']),
)
