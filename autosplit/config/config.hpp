#pragma once

#include <string>
#include <vector>

namespace config {

void initialize(int argc, char **argv);

std::vector<std::string> getIgnoredWindows();

}  // namespace config
