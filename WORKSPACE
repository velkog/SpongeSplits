load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("//toolchain/llvm:install.bzl", "install_llvm_tools")
load("//toolchain/ruff:install.bzl", "install_ruff")

register_execution_platforms(
    "//toolchain:x64_windows-clang-cl"
)

register_toolchains(
    "@local_config_cc//:cc-toolchain-x64_windows-clang-cl",
)

install_llvm_tools("18.1.8", "x86_64-pc-windows-msvc")
install_ruff("0.6.3", "x86_64-pc-windows-msvc")

http_archive(
    name = "yaml-cpp",
    urls = ["https://github.com/jbeder/yaml-cpp/archive/refs/tags/0.8.0.zip"],
    strip_prefix = "yaml-cpp-0.8.0",
    sha256="334e80ab7b52e14c23f94e041c74bab0742f2281aad55f66be2f19f4b7747071",
)
