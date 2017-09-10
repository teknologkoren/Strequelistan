

def svelte_component(srcs):
    native.genrule(
        name = "pwa",
        srcs = [
            srcs,
        ],
        outs = [
            "{}.js".format(path.basename(srcs)),
        ],
        cmd = "svelte compile $< --output $@ --format iife",
    )