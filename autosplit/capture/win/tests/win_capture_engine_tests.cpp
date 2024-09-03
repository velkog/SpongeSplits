#include <Windows.h>
#include <gtest/gtest.h>

#include "autosplit/capture/win/win_capture_engine.hpp"

// Test fixture class for WinCaptureEngine
class WinCaptureEngineTest : public ::testing::Test {
 protected:
  capture::win::WinCaptureEngine engine;
};

// Test to ensure enumerateWindows returns a non-empty map if there are visible
// windows
TEST_F(WinCaptureEngineTest, EnumerateWindows_ReturnsWindows) {
  auto windows = engine.enumerateWindows();
  EXPECT_FALSE(windows.empty());
}

// Test to check if enumerateWindows includes only visible windows
TEST_F(WinCaptureEngineTest, EnumerateWindows_IncludesOnlyVisibleWindows) {
  auto windows = engine.enumerateWindows();

  for (const auto& window : windows) {
    EXPECT_TRUE(IsWindowVisible(engine.hexStringToHWND(window.first)));
  }
}
