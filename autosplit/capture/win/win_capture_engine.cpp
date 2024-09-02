#include "autosplit/capture/win/win_capture_engine.hpp"

#include <Windows.h>

#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

#include "autosplit/config/config.hpp"

namespace capture::win {

static constexpr auto IGNORED_APPLICATIONS = {
    "Discord",
    "Google Chrome",
    "Settings",
    "Microsoft Text Input Application",
    "NVIDIA GeForce Overlay",
    "powershell.exe",
    "Program Manager",
    "Visual Studio Code"};

static BOOL CALLBACK enumWindowCallback(HWND hWnd, LPARAM lParam) {
  std::unordered_map<std::string, std::string>* windows =
      reinterpret_cast<std::unordered_map<std::string, std::string>*>(lParam);

  size_t length = GetWindowTextLength(hWnd);
  char* buffer = new char[length + 1];
  GetWindowText(hWnd, buffer, length + 1);
  std::string windowTitle(buffer);
  delete[] buffer;

  if (IsWindowVisible(hWnd) && length != 0) {
    bool ignoredWindow = false;

    for (const auto& substr : config::getIgnoredWindows()) {
      if (windowTitle.find(substr) != std::string::npos) {
        ignoredWindow = true;
        break;
      }
    }

    if (!ignoredWindow) {
      std::stringstream ss;
      ss << "0x" << std::hex << reinterpret_cast<std::uintptr_t>(hWnd);

      windows->insert({ss.str(), windowTitle});
    }
  }

  return TRUE;
}

std::unordered_map<std::string, std::string>
WinCaptureEngine::enumerateWindows() const {
  std::unordered_map<std::string, std::string> windows;
  EnumWindows(capture::win::enumWindowCallback,
              reinterpret_cast<LPARAM>(&windows));
  return windows;
}

}  // namespace capture::win
