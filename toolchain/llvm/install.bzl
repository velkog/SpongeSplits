load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

BASE_URL = "https://github.com/llvm/llvm-project/releases/download/llvmorg-"
VERSIONS = [
    "18.1.0",
    "18.1.8",
]
PLATFORMS = [
    "x86_64-pc-windows-msvc",
]

LLVM_DISTRIBUTIONS = {
    # 18.1.0
    "clang+llvm-18.1.0-x86_64-pc-windows-msvc": "d128c0f5f7831c77d549296a910fc9972407ff028b720fb628ffa837ed7ff04e",
    
    # 18.1.8
    "clang+llvm-18.1.8-x86_64-pc-windows-msvc": "22c5907db053026cc2a8ff96d21c0f642a90d24d66c23c6d28ee7b1d572b82e8",
}

def install_llvm_tools(llvm_version, platform):
    if llvm_version not in VERSIONS:
        fail("Unsupported version '{}' provided.".format(llvm_version))
    if platform not in PLATFORMS:
        fail("Unsupported platform '{}' provided.".format(platform))

    release_name = "clang+llvm-{}-{}".format(llvm_version, platform)
    url = "{}{}/{}.tar.xz".format(BASE_URL, llvm_version, release_name)

    http_archive(
        name = "llvm_tools",
        urls = [url],
        strip_prefix = release_name,
        sha256 = LLVM_DISTRIBUTIONS[release_name],
        build_file = "@//toolchain/llvm:llvm.BUILD",
    )
