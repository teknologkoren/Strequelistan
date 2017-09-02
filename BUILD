py_binary(
    name = "streque",
    main = "manage.py",
    srcs = [
        "manage.py",
    ],
    deps = [
        ":pwa",
    ],
    imports = [
        "venv/lib/python3.5",
    ],
)

genrule(
    name = "pwa",
    srcs = [
        "foo.html",
    ],
    outs = [
        "foo.js",
    ],
    cmd = "svelte compile $< --output $@ --format iife",
)