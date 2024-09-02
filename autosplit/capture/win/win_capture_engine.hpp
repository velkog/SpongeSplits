#pragma once

#include <string>
#include <unordered_map>

#include "autosplit/capture/capture_engine.hpp"

namespace capture::win {

class WinCaptureEngine : public capture::ICaptureEngine {
 public:
  std::unordered_map<std::string, std::string> enumerateWindows()
      const override final;
};

}  // namespace capture::win
