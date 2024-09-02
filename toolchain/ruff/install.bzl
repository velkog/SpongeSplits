load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

_BASE_URL = "https://github.com/astral-sh/ruff/releases/download/"

_VERSIONS = [
    "0.6.3",
]

_PLATFORMS = [
    "x86_64-pc-windows-msvc",
]

_RUFF_DISTRIBUTIONS = {
    # 0.6.3
    "ruff-x86_64-pc-windows-msvc": "2a4bdca05e61b9855b7668d5377503feb69332fd1401069392212e0579533608",
}


def install_ruff(ruff_version, platform):
    if ruff_version not in _VERSIONS:
        fail("Unsupported version '{}' provided.".format(ruff_version))
    if platform not in _PLATFORMS:
        fail("Unsupported platform '{}' provided.".format(platform))

    release_name = "ruff-{}".format(platform)
    url = "{}{}/{}.zip".format(_BASE_URL, ruff_version, release_name)

    http_archive(
        name="ruff",
        urls=[url],
        # strip_prefix = release_name,
        sha256=_RUFF_DISTRIBUTIONS[release_name],
        build_file="@//toolchain/ruff:ruff.BUILD",
    )
