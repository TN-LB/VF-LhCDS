#include "vflhcds/io/graph.hpp"
#include <array>
#include <cstdint>
#include <iomanip>
#include <limits>
#include <sstream>

namespace vflhcds {
namespace {
constexpr std::array<std::uint32_t, 64> constants{
    0x428a2f98U,0x71374491U,0xb5c0fbcfU,0xe9b5dba5U,0x3956c25bU,0x59f111f1U,0x923f82a4U,0xab1c5ed5U,
    0xd807aa98U,0x12835b01U,0x243185beU,0x550c7dc3U,0x72be5d74U,0x80deb1feU,0x9bdc06a7U,0xc19bf174U,
    0xe49b69c1U,0xefbe4786U,0x0fc19dc6U,0x240ca1ccU,0x2de92c6fU,0x4a7484aaU,0x5cb0a9dcU,0x76f988daU,
    0x983e5152U,0xa831c66dU,0xb00327c8U,0xbf597fc7U,0xc6e00bf3U,0xd5a79147U,0x06ca6351U,0x14292967U,
    0x27b70a85U,0x2e1b2138U,0x4d2c6dfcU,0x53380d13U,0x650a7354U,0x766a0abbU,0x81c2c92eU,0x92722c85U,
    0xa2bfe8a1U,0xa81a664bU,0xc24b8b70U,0xc76c51a3U,0xd192e819U,0xd6990624U,0xf40e3585U,0x106aa070U,
    0x19a4c116U,0x1e376c08U,0x2748774cU,0x34b0bcb5U,0x391c0cb3U,0x4ed8aa4aU,0x5b9cca4fU,0x682e6ff3U,
    0x748f82eeU,0x78a5636fU,0x84c87814U,0x8cc70208U,0x90befffaU,0xa4506cebU,0xbef9a3f7U,0xc67178f2U};
std::uint32_t rotate(const std::uint32_t x, const unsigned n) { return (x >> n) | (x << (32U - n)); }
}  // namespace
std::string sha256(const std::string_view bytes) {
    if (bytes.size() > std::numeric_limits<std::uint64_t>::max() / 8U) throw ResourceLimit("SHA-256 length");
    std::vector<unsigned char> data(bytes.begin(), bytes.end());
    const auto bits = static_cast<std::uint64_t>(bytes.size()) * 8U;
    data.push_back(0x80U);
    while (data.size() % 64U != 56U) data.push_back(0);
    for (unsigned i = 8; i > 0; --i) data.push_back(static_cast<unsigned char>(bits >> ((i - 1U) * 8U)));
    std::array<std::uint32_t, 8> state{0x6a09e667U,0xbb67ae85U,0x3c6ef372U,0xa54ff53aU,0x510e527fU,0x9b05688cU,0x1f83d9abU,0x5be0cd19U};
    for (std::size_t offset = 0; offset < data.size(); offset += 64U) {
        std::array<std::uint32_t, 64> words{};
        for (std::size_t i = 0; i < 16; ++i)
            for (std::size_t j = 0; j < 4; ++j) words[i] = (words[i] << 8U) | data[offset + 4U * i + j];
        for (std::size_t i = 16; i < 64; ++i) {
            const auto x = words[i - 15], y = words[i - 2];
            const auto s0 = rotate(x, 7) ^ rotate(x, 18) ^ (x >> 3U);
            const auto s1 = rotate(y, 17) ^ rotate(y, 19) ^ (y >> 10U);
            words[i] = words[i - 16] + s0 + words[i - 7] + s1;
        }
        auto a = state[0], b = state[1], c = state[2], d = state[3];
        auto e = state[4], f = state[5], g = state[6], h = state[7];
        for (std::size_t i = 0; i < 64; ++i) {
            const auto sum1 = rotate(e, 6) ^ rotate(e, 11) ^ rotate(e, 25);
            const auto choose = (e & f) ^ (~e & g);
            const auto t1 = h + sum1 + choose + constants[i] + words[i];
            const auto sum0 = rotate(a, 2) ^ rotate(a, 13) ^ rotate(a, 22);
            const auto majority = (a & b) ^ (a & c) ^ (b & c);
            h = g; g = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + sum0 + majority;
        }
        state[0] += a; state[1] += b; state[2] += c; state[3] += d;
        state[4] += e; state[5] += f; state[6] += g; state[7] += h;
    }
    std::ostringstream out; out << std::hex << std::setfill('0');
    for (const auto word : state) out << std::setw(8) << word;
    return out.str();
}
}  // namespace vflhcds
