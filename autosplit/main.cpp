#include <iostream>

#include "autosplit/capture/capture_engine.hpp"
#include "autosplit/capture/win/win_capture_engine.hpp"
#include "autosplit/config/config.hpp"

int main(int argc, char **argv) {
  config::initialize(argc, argv);

  const capture::win::WinCaptureEngine winCapEng;
  const capture::ICaptureEngine &captureEngine = winCapEng;

  auto windows = captureEngine.enumerateWindows();

  for (const auto &[key, val] : windows) {
    std::cout << key << ": " << val << std::endl;
  }

  return 0;
}
