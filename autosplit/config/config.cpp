#include "autosplit/config/config.hpp"

#include <tools/cpp/runfiles/runfiles.h>
#include <yaml-cpp/yaml.h>

#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

using bazel::tools::cpp::runfiles::Runfiles;

namespace config {

static constexpr auto SETTINGS_YAML_PATH = "_main/config/settings.yaml";

static std::string mainProgram = "";

void initialize(int argc, char **argv) { mainProgram = argv[0]; }

std::vector<std::string> getIgnoredWindows() {
  std::string error;
  auto runfiles = std::unique_ptr<Runfiles>(
      Runfiles::Create(mainProgram, BAZEL_CURRENT_REPOSITORY, &error));
  if (runfiles == nullptr) {
    throw std::runtime_error(error);
  }

  std::vector<std::string> ignoredWindows;

  std::string path = runfiles->Rlocation(SETTINGS_YAML_PATH);
  YAML::Node config = YAML::LoadFile(path);
  const auto &ignoredFilesNode = config["IGNORED_WINDOWS"];
  for (std::size_t i = 0; i < ignoredFilesNode.size(); i++) {
    ignoredWindows.push_back(ignoredFilesNode[i].as<std::string>());
  }

  return ignoredWindows;
}

}  // namespace config
