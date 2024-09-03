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

http_archive(
    name = "com_github_gflags_gflags",
    sha256 = "34af2f15cf7367513b352bdcd2493ab14ce43692d2dcd9dfc499492966c64dcf",
    strip_prefix = "gflags-2.2.2",
    urls = ["https://github.com/gflags/gflags/archive/v2.2.2.tar.gz"],
)

http_archive(
    name = "com_github_google_glog",
    sha256 = "c17d85c03ad9630006ef32c7be7c65656aba2e7e2fbfc82226b7e680c771fc88",
    strip_prefix = "glog-0.7.1",
    urls = ["https://github.com/google/glog/archive/v0.7.1.zip"],
)
