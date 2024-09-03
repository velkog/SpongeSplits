#pragma once

#include <Windows.h>

#include <optional>
#include <string>
#include <unordered_map>

#include "autosplit/capture/capture_engine.hpp"

namespace capture::win {

class WinCaptureEngine : public capture::ICaptureEngine {
 public:
  ~WinCaptureEngine();

  std::unordered_map<std::string, std::string> enumerateWindows()
      const override final;
  void selectWindow(const std::string& windowId) override final;
  void captureWindow(std::span<uint8_t>& windowImage) override final;

  static HWND hexStringToHWND(const std::string& wIdHexString);
  static std::string hWNDToHexString(const HWND hwnd);

 private:
  std::optional<HWND> currentHWND_{};
  HDC currentCompatibleHDC_{NULL};
  HDC currentWindowHDC_{NULL};
};

}  // namespace capture::win
