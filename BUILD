load("@io_bazel_rules_pex//pex:pex_rules.bzl", "pex_binary")
load("//:requirements.bzl", "requirements")

# The main streque binary.
pex_binary(
    name = "streque",
    main = "manage.py",
    srcs = [
        "manage.py",
    ],
    deps = [
        ":bare",
        "//EmailUser:pylib",
    ],
    data = [
        ":templates",
    ],
    reqs = requirements,
    interpreter = "python3.5",
    # zip_safe=False unzips the pex file before running. This enables more
    # flexibility when using a resource file (e.g. executing it with bash).
    # This is the reason why we choose pex over subpar.
    zip_safe = False,
    pex_use_wheels = False,
)


py_library(
    name = "bare",
    srcs = glob([
        # "manage.py",
        "alge/*.py",
        "api/**/*.py",
        "password_reset_email/**/*.py",
        "ProtectedServe/**/*.py",
        "strecklista/**/*.py",
    ]),
    srcs_version = "PY3",
)


filegroup(
    name = "templates",
    srcs = glob([
        "strecklista/**/*",
    ], exclude = ["**/*.py"]),
)
