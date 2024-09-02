#pragma once

#include <string>
#include <unordered_map>

namespace capture {

class ICaptureEngine {
 public:
  virtual std::unordered_map<std::string, std::string> enumerateWindows()
      const = 0;
};

}  // namespace capture
