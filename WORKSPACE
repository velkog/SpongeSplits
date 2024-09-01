# This file marks the root of the Bazel workspace.
# See MODULE.bazel for external dependencies setup.

# load("@aspect_rules_lint//lint:ruff.bzl", "fetch_ruff")
# # https://github.com/astral-sh/ruff/pull/8631#issuecomment-2022746290
# fetch_ruff("v0.3.2")

register_execution_platforms(
    "//toolchain:x64_windows-clang-cl"
)

register_toolchains(
    "@local_config_cc//:cc-toolchain-x64_windows-clang-cl",
)
