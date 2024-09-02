FORMAT_PATHS = [
    "autosplit/",
    "toolchain/",
    "tools/",
]

py_binary(
    name="format",
    srcs=["format.py"],
    data=[
        "@llvm_tools//:clang_format",
        "@ruff//:ruff",
    ],
    deps=[
        "@rules_python//python/runfiles",
        "//tools/format/system:formatters",
        "//tools/format/system:file",
        "//tools/format/system:print",
    ],
    visibility=["//visibility:public"],
    args=FORMAT_PATHS,
)
