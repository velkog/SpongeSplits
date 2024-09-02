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
