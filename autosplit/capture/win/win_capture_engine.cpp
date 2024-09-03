#include "autosplit/capture/win/win_capture_engine.hpp"

#include <Windows.h>
#include <glog/logging.h>
#include <winuser.h>

#include <cassert>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

#include "autosplit/config/config.hpp"

namespace capture::win {

WinCaptureEngine::~WinCaptureEngine() {
  if (!currentHWND_.has_value()) {
    return;
  }
  HWND hwnd = currentHWND_.value();
  ReleaseDC(hwnd, currentWindowHDC_);
  DeleteObject(currentCompatibleHDC_);
  currentCompatibleHDC_ = nullptr;
}

static constexpr auto IGNORED_APPLICATIONS = {
    "Discord",
    "Google Chrome",
    "Settings",
    "Microsoft Text Input Application",
    "NVIDIA GeForce Overlay",
    "powershell.exe",
    "Program Manager",
    "Visual Studio Code"};

static BOOL CALLBACK enumWindowCallback(HWND hwnd, LPARAM lParam) {
  std::unordered_map<std::string, std::string>* windows =
      reinterpret_cast<std::unordered_map<std::string, std::string>*>(lParam);

  size_t length = GetWindowTextLength(hwnd);
  char* buffer = new char[length + 1];
  GetWindowText(hwnd, buffer, length + 1);
  std::string windowTitle(buffer);
  delete[] buffer;

  if (IsWindowVisible(hwnd) && length != 0) {
    bool ignoredWindow = false;

    for (const auto& substr : config::getIgnoredWindows()) {
      if (windowTitle.find(substr) != std::string::npos) {
        ignoredWindow = true;
        break;
      }
    }

    if (!ignoredWindow) {
      windows->insert({WinCaptureEngine::hWNDToHexString(hwnd), windowTitle});
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

void WinCaptureEngine::selectWindow(const std::string& windowId) {
  HWND hwnd = WinCaptureEngine::hexStringToHWND(windowId);
  currentHWND_ = hwnd;
  currentWindowHDC_ = GetDC(hwnd);
  assert(currentWindowHDC_);
  currentCompatibleHDC_ = CreateCompatibleDC(currentWindowHDC_);
  assert(currentWindowHDC_);
}

void WinCaptureEngine::captureWindow(std::span<uint8_t>& windowImage) {
  if (!currentHWND_.has_value()) {
    LOG(WARNING) << "Cannot capture window until a window has been selected.";
    return;
  }

  HWND hwnd = currentHWND_.value();

  RECT clientRect;
  BOOL result = GetClientRect(hwnd, &clientRect);
  assert(result);

  int width = clientRect.right - clientRect.left;
  int height = clientRect.bottom - clientRect.top;
  HBITMAP hbmWindow = CreateCompatibleBitmap(currentWindowHDC_, width, height);
  assert(hbmWindow);

  DLOG(INFO) << "Capturing window '" << hwnd << "' with dimensions (" << width
             << " x " << height << ")";

  SelectObject(currentCompatibleHDC_, hbmWindow);

  result = BitBlt(currentCompatibleHDC_, 0, 0, width, height, currentWindowHDC_,
                  0, 0, SRCCOPY);
  assert(result);

  BITMAP bmpWindow;
  result = GetObject(hbmWindow, sizeof(BITMAP), &bmpWindow);
  assert(result);

  BITMAPFILEHEADER bmfHeader;
  BITMAPINFOHEADER bi;

  bi.biSize = sizeof(BITMAPINFOHEADER);
  bi.biWidth = bmpWindow.bmWidth;
  bi.biHeight = bmpWindow.bmHeight;
  bi.biPlanes = 1;
  bi.biBitCount = 32;
  bi.biCompression = BI_RGB;
  bi.biSizeImage = 0;
  bi.biXPelsPerMeter = 0;
  bi.biYPelsPerMeter = 0;
  bi.biClrUsed = 0;
  bi.biClrImportant = 0;

  // int dwBmpSize =
  //     ((bmpWindow.bmWidth * bi.biBitCount + 31) / 32) * 4 *
  //     bmpWindow.bmHeight;

  // if (!GetDIBits(hdcMem, hBitmap, 0, bmpWindow.bmHeight, buffer.data(),
  //                &bmpInfo, DIB_RGB_COLORS)) {
  //   SelectObject(hdcMem, hOldBitmap);
  //   DeleteDC(hdcMem);
  //   throw std::runtime_error("Failed to get bitmap bits.");
  // }

  DeleteObject(hbmWindow);
}

HWND WinCaptureEngine::hexStringToHWND(const std::string& wIdHexString) {
  return reinterpret_cast<HWND>(std::stoul(wIdHexString, nullptr, 16));
}

std::string WinCaptureEngine::hWNDToHexString(const HWND hwnd) {
  std::stringstream ss;
  ss << "0x" << std::hex << reinterpret_cast<std::uintptr_t>(hwnd);
  return ss.str();
}

}  // namespace capture::win
