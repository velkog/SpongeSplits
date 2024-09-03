#include <glog/logging.h>

#include <iostream>
#include <span>

#include "autosplit/capture/capture_engine.hpp"
#include "autosplit/capture/win/win_capture_engine.hpp"
#include "autosplit/config/config.hpp"

static uint8_t IMAGE_CONTAINER[4096 * 4096 * 3];

void setup(int argc, char **argv) {
  config::initialize(argc, argv);

  FLAGS_alsologtostderr = 1;
  FLAGS_minloglevel = google::GLOG_INFO;
  google::InitGoogleLogging(argv[0]);
}

void run() {
  capture::win::WinCaptureEngine winCapEng;
  capture::ICaptureEngine &captureEngine = winCapEng;

  auto windows = captureEngine.enumerateWindows();

  std::string selectedWindow;
  for (const auto &[key, val] : windows) {
    selectedWindow = key;
    LOG(INFO) << key << ": " << val;
  }

  LOG(INFO) << "Selecting '" << selectedWindow << "' to capture.";
  captureEngine.selectWindow(selectedWindow);

  std::span<uint8_t> windowImage{IMAGE_CONTAINER};
  captureEngine.captureWindow(windowImage);
}

void teardown() { google::ShutdownGoogleLogging(); }

int main(int argc, char **argv) {
  setup(argc, argv);
  run();
  teardown();
  return 0;
}
