load("@pip_deps//:requirements.bzl", "requirement")

py_library(
    name="formatters",
    srcs=[
        "formatter.py",
    ],
    deps=[
        "@rules_python//python/runfiles",
    ],
    visibility=["//visibility:public"],
)


py_library(
    name="file",
    srcs=[
        "file.py",
    ],
    visibility=["//visibility:public"],
)

py_library(
    name="print",
    srcs=[
        "print.py",
    ],
    deps=[
        requirement("termcolor"),
    ],
    visibility=["//visibility:public"],
)
