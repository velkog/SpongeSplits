load("@aspect_rules_lint//format:defs.bzl", "format_multirun")

format_multirun(
    name = "format",
    cc = "@llvm_toolchain_llvm//:bin/clang-format",
    python = "//tools/lint:ruff",
    visibility = ["//visibility:public"],
)

FORMAT_PATHS = [
    ".",
]

py_binary(
    name = "clang_format",
    srcs = [
        "format.py"
    ],
    main = "format.py",
    args = [
        "--format-executable='clang-format'",
        "--language='cpp'",
    ] + FORMAT_PATHS,
    deps = [
        "//tools:print",
    ],
)
