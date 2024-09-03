#pragma once

#include <cstdint>
#include <span>

namespace capture::frame {

class Frame {
 public:
  class RGB {
   public:
    explicit RGB();
    explicit RGB(uint8_t r, uint8_t g, uint8_t b);

    uint8_t red;
    uint8_t green;
    uint8_t blue;
  };

  explicit Frame(void *data, uint16_t width, uint16_t height);

 private:
  std::span<RGB> data_;
  uint16_t width_;
  uint16_t height_;
};

}  // namespace capture::frame
