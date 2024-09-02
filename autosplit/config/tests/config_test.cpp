#include "autosplit/config/config.hpp"

#include <gtest/gtest.h>

#include <array>

TEST(ConfigTest, TestIgnoredWindows) {
  static const std::array<std::string, 8> kExpectedIgnoredWindows = {
      "Discord",
      "Google Chrome",
      "Settings",
      "Microsoft Text Input Application",
      "NVIDIA GeForce Overlay",
      "powershell.exe",
      "Program Manager",
      "Visual Studio Code",
  };

  auto ignoredWindows = config::getIgnoredWindows();

  EXPECT_EQ(ignoredWindows.size(), kExpectedIgnoredWindows.size());
  for (size_t i = 0; i < ignoredWindows.size(); ++i) {
    EXPECT_EQ(ignoredWindows[i], kExpectedIgnoredWindows[i]);
  }
}
