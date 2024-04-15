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
