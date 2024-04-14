LINT_PATHS = [
    ".",
]

py_binary(
    name = "clang_format",
    srcs = [
        "lint.py"
    ],
    main = "lint.py",
    args = [
        "--lint-executable='clang-format'",
        "--language='cpp'"
    ] + LINT_PATHS,
    deps = [
        "//tools:print",
    ],
)
