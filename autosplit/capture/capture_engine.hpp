#pragma once

#include <span>
#include <string>
#include <unordered_map>

namespace capture {

class ICaptureEngine {
 public:
  virtual std::unordered_map<std::string, std::string> enumerateWindows()
      const = 0;

  virtual void selectWindow(const std::string& windowId) = 0;

  virtual void captureWindow(std::span<uint8_t>& windowImage) = 0;
};

}  // namespace capture
