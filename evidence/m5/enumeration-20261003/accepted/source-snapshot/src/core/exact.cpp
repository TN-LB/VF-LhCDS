#include "vflhcds/core/exact.hpp"
#include <cstdint>
#include <limits>
#include <utility>

namespace vflhcds {
BigInt parse_integer(const std::string_view text, const bool allow_negative) {
    if (text.empty()) throw std::invalid_argument("empty integer");
    const bool negative = text.front() == '-';
    const std::size_t start = negative ? 1U : 0U;
    if ((negative && !allow_negative) || start == text.size()
        || (text[start] == '0' && (negative || text.size() - start != 1)))
        throw std::invalid_argument("noncanonical integer");
    BigInt value = 0;
    for (std::size_t i = start; i < text.size(); ++i) {
        if (text[i] < '0' || text[i] > '9') throw std::invalid_argument("invalid integer");
        value *= 10;
        value += text[i] - '0';
    }
    return negative ? -value : value;
}
std::string decimal(const BigInt& value) { return value.str(); }
std::size_t to_size(const BigInt& value) {
    if (value < 0 || value > std::numeric_limits<std::size_t>::max())
        throw ResourceLimit("container index range exceeded");
    return value.convert_to<std::size_t>();
}
BigInt to_big(const UInt128 value) {
    return (BigInt(static_cast<std::uint64_t>(value >> 64U)) << 64U)
        + static_cast<std::uint64_t>(value);
}
UInt128 to_uint128(const BigInt& value) {
    if (value < 0 || value > to_big(uint128_max)) throw std::overflow_error("uint128 conversion");
    const auto low = (value & ((BigInt(1) << 64U) - 1)).convert_to<std::uint64_t>();
    const auto high = (value >> 64U).convert_to<std::uint64_t>();
    return (UInt128(high) << 64U) | UInt128(low);
}
UInt128 checked_add(const UInt128 a, const UInt128 b) {
    if (b > uint128_max - a) throw std::overflow_error("uint128 addition");
    return a + b;
}
UInt128 checked_sub(const UInt128 a, const UInt128 b) {
    if (b > a) throw std::overflow_error("uint128 subtraction");
    return a - b;
}
UInt128 checked_mul(const UInt128 a, const UInt128 b) {
    if (a != 0 && b > uint128_max / a) throw std::overflow_error("uint128 multiplication");
    return a * b;
}
std::size_t bit_length(const BigInt& value) {
    if (value < 0) throw std::invalid_argument("negative bit length input");
    return value == 0 ? 0U : static_cast<std::size_t>(boost::multiprecision::msb(value)) + 1U;
}
Fraction::Fraction(BigInt numerator, BigInt denominator) {
    if (denominator <= 0) throw std::invalid_argument("nonpositive denominator");
    BigInt a = numerator < 0 ? -numerator : numerator;
    BigInt b = denominator;
    while (b != 0) { BigInt remainder = a % b; a = std::move(b); b = std::move(remainder); }
    numerator_ = numerator / a;
    denominator_ = denominator / a;
}
Fraction Fraction::parse(const std::string_view text) {
    const auto slash = text.find('/');
    if (slash == std::string_view::npos) throw std::invalid_argument("fraction requires A/B");
    return Fraction(parse_integer(text.substr(0, slash)), parse_integer(text.substr(slash + 1)));
}
BigInt scaled_objective(const Fraction& lambda, const BigInt& cliques, const std::size_t vertices) {
    return lambda.denominator() * cliques - lambda.numerator() * vertices;
}
}  // namespace vflhcds
