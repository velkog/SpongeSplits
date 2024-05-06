load("@aspect_rules_lint//format:defs.bzl", "format_multirun", "format_test")

format_multirun(
    name = "format",
    cc = "@llvm_toolchain_llvm//:bin/clang-format",
    python = "//tools/lint:ruff",
    visibility = ["//visibility:public"],
)

format_test(
    name = "format_test",
    no_sandbox = True,
    workspace = "//:WORKSPACE",
    # TODO: not hermetic, requires libncurses installed on the machine even when non-interactive
    cc = "@llvm_toolchain_llvm//:bin/clang-format",
    python = "//tools/lint:ruff",
)

FORMAT_PATHS = [
    ".",
]
