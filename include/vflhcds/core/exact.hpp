#pragma once

#include <boost/multiprecision/cpp_int.hpp>
#include <cstddef>
#include <string>
#include <string_view>
#include <stdexcept>

namespace vflhcds {
using BigInt = boost::multiprecision::number<boost::multiprecision::cpp_int_backend<>,
                                            boost::multiprecision::et_off>;
// Localized compiler extension; the project otherwise builds in strict C++17.
__extension__ typedef unsigned __int128 UInt128;
inline constexpr UInt128 uint128_max = ~UInt128{0};

struct ResourceLimit : std::runtime_error { using std::runtime_error::runtime_error; };
struct InvalidGraph : std::invalid_argument { using std::invalid_argument::invalid_argument; };
struct IoError : std::runtime_error { using std::runtime_error::runtime_error; };

BigInt parse_integer(std::string_view text, bool allow_negative = false);
std::string decimal(const BigInt& value);
std::size_t to_size(const BigInt& value);
UInt128 to_uint128(const BigInt& value);
BigInt to_big(UInt128 value);
UInt128 checked_add(UInt128 a, UInt128 b);
UInt128 checked_sub(UInt128 a, UInt128 b);
UInt128 checked_mul(UInt128 a, UInt128 b);
std::size_t bit_length(const BigInt& value);

class Fraction {
public:
    Fraction(BigInt numerator = 0, BigInt denominator = 1);
    static Fraction parse(std::string_view text);
    const BigInt& numerator() const noexcept { return numerator_; }
    const BigInt& denominator() const noexcept { return denominator_; }
    friend bool operator==(const Fraction& a, const Fraction& b) {
        return a.numerator_ == b.numerator_ && a.denominator_ == b.denominator_;
    }
    friend bool operator<(const Fraction& a, const Fraction& b) {
        return a.numerator_ * b.denominator_ < b.numerator_ * a.denominator_;
    }
private:
    BigInt numerator_, denominator_;
};
BigInt scaled_objective(const Fraction& lambda, const BigInt& cliques, std::size_t vertices);
}  // namespace vflhcds
