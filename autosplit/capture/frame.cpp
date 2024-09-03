#include "autosplit/capture/frame.hpp"

#include <cstdint>
#include <span>

namespace capture::frame {

Frame::RGB::RGB(uint8_t r, uint8_t g, uint8_t b) {
  red = r;
  green = g;
  blue = b;
}

Frame::Frame(void *data, uint16_t width, uint16_t height)
    : data_{std::span<RGB>(static_cast<RGB *>(data), width * height)},
      width_{width},
      height_{height} {}

}  // namespace capture::frame
