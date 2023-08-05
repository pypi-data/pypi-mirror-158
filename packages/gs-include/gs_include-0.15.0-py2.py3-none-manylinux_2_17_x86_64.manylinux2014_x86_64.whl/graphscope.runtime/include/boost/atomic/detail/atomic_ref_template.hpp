/*
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file LICENSE_1_0.txt or copy at
 * http://www.boost.org/LICENSE_1_0.txt)
 *
 * Copyright (c) 2020 Andrey Semashev
 */
/*!
 * \file   atomic/detail/atomic_ref_template.hpp
 *
 * This header contains interface definition of \c atomic_ref template.
 */

#ifndef BOOST_ATOMIC_DETAIL_ATOMIC_REF_TEMPLATE_HPP_INCLUDED_
#define BOOST_ATOMIC_DETAIL_ATOMIC_REF_TEMPLATE_HPP_INCLUDED_

#include <cstddef>
#include <boost/cstdint.hpp>
#include <boost/assert.hpp>
#include <boost/static_assert.hpp>
#include <boost/memory_order.hpp>
#include <boost/atomic/detail/config.hpp>
#include <boost/atomic/detail/intptr.hpp>
#include <boost/atomic/detail/classify.hpp>
#include <boost/atomic/detail/addressof.hpp>
#include <boost/atomic/detail/storage_traits.hpp>
#include <boost/atomic/detail/bitwise_cast.hpp>
#include <boost/atomic/detail/integral_conversions.hpp>
#include <boost/atomic/detail/operations.hpp>
#include <boost/atomic/detail/extra_operations.hpp>
#include <boost/atomic/detail/memory_order_utils.hpp>
#include <boost/atomic/detail/type_traits/is_signed.hpp>
#include <boost/atomic/detail/type_traits/is_trivially_copyable.hpp>
#include <boost/atomic/detail/type_traits/is_trivially_default_constructible.hpp>
#include <boost/atomic/detail/type_traits/alignment_of.hpp>
#include <boost/atomic/detail/type_traits/conditional.hpp>
#include <boost/atomic/detail/type_traits/integral_constant.hpp>
#if !defined(BOOST_ATOMIC_NO_FLOATING_POINT)
#include <boost/atomic/detail/bitwise_fp_cast.hpp>
#include <boost/atomic/detail/fp_operations.hpp>
#include <boost/atomic/detail/extra_fp_operations.hpp>
#endif

#ifdef BOOST_HAS_PRAGMA_ONCE
#pragma once
#endif

#if defined(BOOST_MSVC)
#pragma warning(push)
// 'boost::atomics::atomic_ref<T>' : multiple assignment operators specified
#pragma warning(disable: 4522)
#endif

/*
 * IMPLEMENTATION NOTE: All interface functions MUST be declared with BOOST_FORCEINLINE,
 *                      see comment for convert_memory_order_to_gcc in ops_gcc_atomic.hpp.
 */

namespace boost {
namespace atomics {
namespace detail {

template< typename T, bool IsSigned >
struct is_atomic_ref_lock_free
{
    typedef T value_type;
    typedef atomics::detail::operations< sizeof(value_type), IsSigned > operations;
    typedef typename operations::storage_type storage_type;

    static BOOST_CONSTEXPR_OR_CONST bool value = sizeof(value_type) == sizeof(storage_type) && operations::is_always_lock_free;
};

template< typename T, bool IsSigned >
class base_atomic_ref_common
{
public:
    typedef T value_type;

protected:
    typedef typename atomics::detail::conditional<
        atomics::detail::is_atomic_ref_lock_free< T, IsSigned >::value,
        atomics::detail::operations< sizeof(value_type), IsSigned >,
        atomics::detail::emulated_operations< sizeof(value_type), atomics::detail::alignment_of< value_type >::value, IsSigned >
    >::type operations;
    typedef typename atomics::detail::conditional< sizeof(value_type) <= sizeof(void*), value_type, value_type const& >::type value_arg_type;
    typedef typename operations::storage_type storage_type;

public:
    static BOOST_CONSTEXPR_OR_CONST std::size_t required_alignment = atomics::detail::alignment_of< value_type >::value <= operations::storage_alignment ? operations::storage_alignment : atomics::detail::alignment_of< value_type >::value;
    static BOOST_CONSTEXPR_OR_CONST bool is_always_lock_free = operations::is_always_lock_free;

protected:
    value_type* m_value;

public:
    BOOST_FORCEINLINE explicit base_atomic_ref_common(value_type& v) BOOST_NOEXCEPT : m_value(atomics::detail::addressof(v))
    {
    }

protected:
    BOOST_FORCEINLINE storage_type& storage() const BOOST_NOEXCEPT
    {
        return *reinterpret_cast< storage_type* >(m_value);
    }
};

#if defined(BOOST_NO_CXX17_INLINE_VARIABLES)
template< typename T, bool IsSigned >
BOOST_CONSTEXPR_OR_CONST std::size_t base_atomic_ref_common< T, IsSigned >::required_alignment;
template< typename T, bool IsSigned >
BOOST_CONSTEXPR_OR_CONST bool base_atomic_ref_common< T, IsSigned >::is_always_lock_free;
#endif


template< typename T, typename Kind >
class base_atomic_ref;

//! General template. Implementation for user-defined types, such as structs and enums, and pointers to non-object types
template< typename T >
class base_atomic_ref< T, void > :
    public base_atomic_ref_common< T, false >
{
private:
    typedef base_atomic_ref_common< T, false > base_type;

public:
    typedef typename base_type::value_type value_type;

protected:
    typedef typename base_type::operations operations;
    typedef typename base_type::storage_type storage_type;
    typedef typename base_type::value_arg_type value_arg_type;

private:
    typedef atomics::detail::integral_constant< bool, atomics::detail::alignment_of< value_type >::value <= operations::storage_alignment > use_bitwise_cast;

public:
    BOOST_DEFAULTED_FUNCTION(base_atomic_ref(base_atomic_ref const& that) BOOST_ATOMIC_DETAIL_DEF_NOEXCEPT_DECL, BOOST_ATOMIC_DETAIL_DEF_NOEXCEPT_IMPL : base_type(static_cast< base_type const& >(that)) {})
    BOOST_FORCEINLINE explicit base_atomic_ref(value_type& v) BOOST_NOEXCEPT : base_type(v)
    {
    }

    BOOST_FORCEINLINE void store(value_arg_type v, memory_order order = memory_order_seq_cst) const BOOST_NOEXCEPT
    {
        BOOST_ASSERT(order != memory_order_consume);
        BOOST_ASSERT(order != memory_order_acquire);
        BOOST_ASSERT(order != memory_order_acq_rel);

        operations::store(this->storage(), atomics::detail::bitwise_cast< storage_type >(v), order);
    }

    BOOST_FORCEINLINE value_type load(memory_order order = memory_order_seq_cst) const BOOST_NOEXCEPT
    {
        BOOST_ASSERT(order != memory_order_release);
        BOOST_ASSERT(order != memory_order_acq_rel);

        return atomics::detail::bitwise_cast< value_type >(operations::load(this->storage(), order));
    }

    BOOST_FORCEINLINE value_type exchange(value_arg_type v, memory_order order = memory_order_seq_cst) const BOOST_NOEXCEPT
    {
        return atomics::detail::bitwise_cast< value_type >(operations::exchange(this->storage(), atomics::detail::bitwise_cast< storage_type >(v), order));
    }

    BOOST_FORCEINLINE bool compare_exchange_strong(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order) const BOOST_NOEXCEPT
    {
        BOOST_ASSERT(failure_order != memory_order_release);
        BOOST_ASSERT(failure_order != memory_order_acq_rel);
        BOOST_ASSERT(cas_failure_order_must_not_be_stronger_than_success_order(success_order, failure_order));

        return compare_exchange_strong_impl(expected, desired, success_order, failure_order, use_bitwise_cast());
    }

    BOOST_FORCEINLINE bool compare_exchange_strong(value_type& expected, value_arg_type desired, memory_order order = memory_order_seq_cst) const BOOST_NOEXCEPT
    {
        return compare_exchange_strong(expected, desired, order, atomics::detail::deduce_failure_order(order));
    }

    BOOST_FORCEINLINE bool compare_exchange_weak(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order) const BOOST_NOEXCEPT
    {
        BOOST_ASSERT(failure_order != memory_order_release);
        BOOST_ASSERT(failure_order != memory_order_acq_rel);
        BOOST_ASSERT(cas_failure_order_must_not_be_stronger_than_success_order(success_order, failure_order));

        return compare_exchange_weak_impl(expected, desired, success_order, failure_order, use_bitwise_cast());
    }

    BOOST_FORCEINLINE bool compare_exchange_weak(value_type& expected, value_arg_type desired, memory_order order = memory_order_seq_cst) const BOOST_NOEXCEPT
    {
        return compare_exchange_weak(expected, desired, order, atomics::detail::deduce_failure_order(order));
    }

    BOOST_DELETED_FUNCTION(base_atomic_ref& operator=(base_atomic_ref const&))

private:
    BOOST_FORCEINLINE bool compare_exchange_strong_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::false_type) const BOOST_NOEXCEPT
    {
#if defined(BOOST_ATOMIC_DETAIL_STORAGE_TYPE_MAY_ALIAS)
        return operations::compare_exchange_strong(this->storage(), reinterpret_cast< storage_type& >(expected), atomics::detail::bitwise_cast< storage_type >(desired), success_order, failure_order);
#else
        return compare_exchange_strong_impl(expected, desired, success_order, failure_order, atomics::detail::true_type());
#endif
    }

    BOOST_FORCEINLINE bool compare_exchange_strong_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::true_type) const BOOST_NOEXCEPT
    {
        storage_type old_value = atomics::detail::bitwise_cast< storage_type >(expected);
        const bool res = operations::compare_exchange_strong(this->storage(), old_value, atomics::detail::bitwise_cast< storage_type >(desired), success_order, failure_order);
        expected = atomics::detail::bitwise_cast< value_type >(old_value);
        return res;
    }

    BOOST_FORCEINLINE bool compare_exchange_weak_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::false_type) const BOOST_NOEXCEPT
    {
#if defined(BOOST_ATOMIC_DETAIL_STORAGE_TYPE_MAY_ALIAS)
        return operations::compare_exchange_weak(this->storage(), reinterpret_cast< storage_type& >(expected), atomics::detail::bitwise_cast< storage_type >(desired), success_order, failure_order);
#else
        return compare_exchange_weak_impl(expected, desired, success_order, failure_order, atomics::detail::true_type());
#endif
    }

    BOOST_FORCEINLINE bool compare_exchange_weak_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::true_type) const BOOST_NOEXCEPT
    {
        storage_type old_value = atomics::detail::bitwise_cast< storage_type >(expected);
        const bool res = operations::compare_exchange_weak(this->storage(), old_value, atomics::detail::bitwise_cast< storage_type >(desired), success_order, failure_order);
        expected = atomics::detail::bitwise_cast< value_type >(old_value);
        return res;
    }
};


//! Implementation for integers
template< typename T >
class base_atomic_ref< T, int > :
    public base_atomic_ref_common< T, atomics::detail::is_signed< T >::value >
{
private:
    typedef base_atomic_ref_common< T, atomics::detail::is_signed< T >::value > base_type;

public:
    typedef typename base_type::value_type value_type;
    typedef typename base_type::value_type difference_type;

protected:
    typedef typename base_type::operations operations;
    typedef atomics::detail::extra_operations< operations, operations::storage_size, operations::is_signed > extra_operations;
    typedef typename base_type::storage_type storage_type;
    typedef value_type value_arg_type;

private:
    typedef atomics::detail::integral_constant< bool, atomics::detail::alignment_of< value_type >::value <= operations::storage_alignment > use_bitwise_cast;

public:
    BOOST_DEFAULTED_FUNCTION(base_atomic_ref(base_atomic_ref const& that) BOOST_ATOMIC_DETAIL_DEF_NOEXCEPT_DECL, BOOST_ATOMIC_DETAIL_DEF_NOEXCEPT_IMPL : base_type(static_cast< base_type const& >(that)) {})
    BOOST_FORCEINLINE explicit base_atomic_ref(value_type& v) BOOST_NOEXCEPT : base_type(v)
    {
    }

    // Standard methods
    BOOST_FORCEINLINE void store(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        BOOST_ASSERT(order != memory_order_consume);
        BOOST_ASSERT(order != memory_order_acquire);
        BOOST_ASSERT(order != memory_order_acq_rel);

        operations::store(this->storage(), static_cast< storage_type >(v), order);
    }

    BOOST_FORCEINLINE value_type load(memory_order order = memory_order_seq_cst) const BOOST_NOEXCEPT
    {
        BOOST_ASSERT(order != memory_order_release);
        BOOST_ASSERT(order != memory_order_acq_rel);

        return atomics::detail::integral_truncate< value_type >(operations::load(this->storage(), order));
    }

    BOOST_FORCEINLINE value_type fetch_add(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::integral_truncate< value_type >(operations::fetch_add(this->storage(), static_cast< storage_type >(v), order));
    }

    BOOST_FORCEINLINE value_type fetch_sub(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::integral_truncate< value_type >(operations::fetch_sub(this->storage(), static_cast< storage_type >(v), order));
    }

    BOOST_FORCEINLINE value_type exchange(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::integral_truncate< value_type >(operations::exchange(this->storage(), static_cast< storage_type >(v), order));
    }

    BOOST_FORCEINLINE bool compare_exchange_strong(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order) BOOST_NOEXCEPT
    {
        BOOST_ASSERT(failure_order != memory_order_release);
        BOOST_ASSERT(failure_order != memory_order_acq_rel);
        BOOST_ASSERT(cas_failure_order_must_not_be_stronger_than_success_order(success_order, failure_order));

        return compare_exchange_strong_impl(expected, desired, success_order, failure_order, use_bitwise_cast());
    }

    BOOST_FORCEINLINE bool compare_exchange_strong(value_type& expected, value_arg_type desired, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return compare_exchange_strong(expected, desired, order, atomics::detail::deduce_failure_order(order));
    }

    BOOST_FORCEINLINE bool compare_exchange_weak(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order) BOOST_NOEXCEPT
    {
        BOOST_ASSERT(failure_order != memory_order_release);
        BOOST_ASSERT(failure_order != memory_order_acq_rel);
        BOOST_ASSERT(cas_failure_order_must_not_be_stronger_than_success_order(success_order, failure_order));

        return compare_exchange_weak_impl(expected, desired, success_order, failure_order, use_bitwise_cast());
    }

    BOOST_FORCEINLINE bool compare_exchange_weak(value_type& expected, value_arg_type desired, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return compare_exchange_weak(expected, desired, order, atomics::detail::deduce_failure_order(order));
    }

    BOOST_FORCEINLINE value_type fetch_and(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::integral_truncate< value_type >(operations::fetch_and(this->storage(), static_cast< storage_type >(v), order));
    }

    BOOST_FORCEINLINE value_type fetch_or(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::integral_truncate< value_type >(operations::fetch_or(this->storage(), static_cast< storage_type >(v), order));
    }

    BOOST_FORCEINLINE value_type fetch_xor(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::integral_truncate< value_type >(operations::fetch_xor(this->storage(), static_cast< storage_type >(v), order));
    }

    // Boost.Atomic extensions
    BOOST_FORCEINLINE value_type fetch_negate(memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::integral_truncate< value_type >(extra_operations::fetch_negate(this->storage(), order));
    }

    BOOST_FORCEINLINE value_type fetch_complement(memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::integral_truncate< value_type >(extra_operations::fetch_complement(this->storage(), order));
    }

    BOOST_FORCEINLINE value_type add(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::integral_truncate< value_type >(extra_operations::add(this->storage(), static_cast< storage_type >(v), order));
    }

    BOOST_FORCEINLINE value_type sub(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::integral_truncate< value_type >(extra_operations::sub(this->storage(), static_cast< storage_type >(v), order));
    }

    BOOST_FORCEINLINE value_type negate(memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::integral_truncate< value_type >(extra_operations::negate(this->storage(), order));
    }

    BOOST_FORCEINLINE value_type bitwise_and(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::integral_truncate< value_type >(extra_operations::bitwise_and(this->storage(), static_cast< storage_type >(v), order));
    }

    BOOST_FORCEINLINE value_type bitwise_or(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::integral_truncate< value_type >(extra_operations::bitwise_or(this->storage(), static_cast< storage_type >(v), order));
    }

    BOOST_FORCEINLINE value_type bitwise_xor(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::integral_truncate< value_type >(extra_operations::bitwise_xor(this->storage(), static_cast< storage_type >(v), order));
    }

    BOOST_FORCEINLINE value_type bitwise_complement(memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::integral_truncate< value_type >(extra_operations::bitwise_complement(this->storage(), order));
    }

    BOOST_FORCEINLINE void opaque_add(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        extra_operations::opaque_add(this->storage(), static_cast< storage_type >(v), order);
    }

    BOOST_FORCEINLINE void opaque_sub(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        extra_operations::opaque_sub(this->storage(), static_cast< storage_type >(v), order);
    }

    BOOST_FORCEINLINE void opaque_negate(memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        extra_operations::opaque_negate(this->storage(), order);
    }

    BOOST_FORCEINLINE void opaque_and(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        extra_operations::opaque_and(this->storage(), static_cast< storage_type >(v), order);
    }

    BOOST_FORCEINLINE void opaque_or(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        extra_operations::opaque_or(this->storage(), static_cast< storage_type >(v), order);
    }

    BOOST_FORCEINLINE void opaque_xor(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        extra_operations::opaque_xor(this->storage(), static_cast< storage_type >(v), order);
    }

    BOOST_FORCEINLINE void opaque_complement(memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        extra_operations::opaque_complement(this->storage(), order);
    }

    BOOST_FORCEINLINE bool add_and_test(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return extra_operations::add_and_test(this->storage(), static_cast< storage_type >(v), order);
    }

    BOOST_FORCEINLINE bool sub_and_test(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return extra_operations::sub_and_test(this->storage(), static_cast< storage_type >(v), order);
    }

    BOOST_FORCEINLINE bool negate_and_test(memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return extra_operations::negate_and_test(this->storage(), order);
    }

    BOOST_FORCEINLINE bool and_and_test(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return extra_operations::and_and_test(this->storage(), static_cast< storage_type >(v), order);
    }

    BOOST_FORCEINLINE bool or_and_test(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return extra_operations::or_and_test(this->storage(), static_cast< storage_type >(v), order);
    }

    BOOST_FORCEINLINE bool xor_and_test(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return extra_operations::xor_and_test(this->storage(), static_cast< storage_type >(v), order);
    }

    BOOST_FORCEINLINE bool complement_and_test(memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return extra_operations::complement_and_test(this->storage(), order);
    }

    BOOST_FORCEINLINE bool bit_test_and_set(unsigned int bit_number, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        BOOST_ASSERT(bit_number < sizeof(value_type) * 8u);
        return extra_operations::bit_test_and_set(this->storage(), bit_number, order);
    }

    BOOST_FORCEINLINE bool bit_test_and_reset(unsigned int bit_number, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        BOOST_ASSERT(bit_number < sizeof(value_type) * 8u);
        return extra_operations::bit_test_and_reset(this->storage(), bit_number, order);
    }

    BOOST_FORCEINLINE bool bit_test_and_complement(unsigned int bit_number, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        BOOST_ASSERT(bit_number < sizeof(value_type) * 8u);
        return extra_operations::bit_test_and_complement(this->storage(), bit_number, order);
    }

    // Operators
    BOOST_FORCEINLINE value_type operator++(int) BOOST_NOEXCEPT
    {
        return fetch_add(1);
    }

    BOOST_FORCEINLINE value_type operator++() BOOST_NOEXCEPT
    {
        return add(1);
    }

    BOOST_FORCEINLINE value_type operator--(int) BOOST_NOEXCEPT
    {
        return fetch_sub(1);
    }

    BOOST_FORCEINLINE value_type operator--() BOOST_NOEXCEPT
    {
        return sub(1);
    }

    BOOST_FORCEINLINE value_type operator+=(difference_type v) BOOST_NOEXCEPT
    {
        return add(v);
    }

    BOOST_FORCEINLINE value_type operator-=(difference_type v) BOOST_NOEXCEPT
    {
        return sub(v);
    }

    BOOST_FORCEINLINE value_type operator&=(value_type v) BOOST_NOEXCEPT
    {
        return bitwise_and(v);
    }

    BOOST_FORCEINLINE value_type operator|=(value_type v) BOOST_NOEXCEPT
    {
        return bitwise_or(v);
    }

    BOOST_FORCEINLINE value_type operator^=(value_type v) BOOST_NOEXCEPT
    {
        return bitwise_xor(v);
    }

    BOOST_DELETED_FUNCTION(base_atomic_ref& operator=(base_atomic_ref const&))

private:
    BOOST_FORCEINLINE bool compare_exchange_strong_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::false_type) const BOOST_NOEXCEPT
    {
#if defined(BOOST_ATOMIC_DETAIL_STORAGE_TYPE_MAY_ALIAS)
        return operations::compare_exchange_strong(this->storage(), reinterpret_cast< storage_type& >(expected), static_cast< storage_type >(desired), success_order, failure_order);
#else
        return compare_exchange_strong_impl(expected, desired, success_order, failure_order, atomics::detail::true_type());
#endif
    }

    BOOST_FORCEINLINE bool compare_exchange_strong_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::true_type) const BOOST_NOEXCEPT
    {
        storage_type old_value = static_cast< storage_type >(expected);
        const bool res = operations::compare_exchange_strong(this->storage(), old_value, static_cast< storage_type >(desired), success_order, failure_order);
        expected = atomics::detail::integral_truncate< value_type >(old_value);
        return res;
    }

    BOOST_FORCEINLINE bool compare_exchange_weak_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::false_type) const BOOST_NOEXCEPT
    {
#if defined(BOOST_ATOMIC_DETAIL_STORAGE_TYPE_MAY_ALIAS)
        return operations::compare_exchange_weak(this->storage(), reinterpret_cast< storage_type& >(expected), static_cast< storage_type >(desired), success_order, failure_order);
#else
        return compare_exchange_weak_impl(expected, desired, success_order, failure_order, atomics::detail::true_type());
#endif
    }

    BOOST_FORCEINLINE bool compare_exchange_weak_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::true_type) const BOOST_NOEXCEPT
    {
        storage_type old_value = static_cast< storage_type >(expected);
        const bool res = operations::compare_exchange_weak(this->storage(), old_value, static_cast< storage_type >(desired), success_order, failure_order);
        expected = atomics::detail::integral_truncate< value_type >(old_value);
        return res;
    }
};

//! Implementation for bool
template< >
class base_atomic_ref< bool, int > :
    public base_atomic_ref_common< bool, false >
{
private:
    typedef base_atomic_ref_common< bool, false > base_type;

public:
    typedef bool value_type;

protected:
    typedef base_type::operations operations;
    typedef atomics::detail::extra_operations< operations, operations::storage_size, operations::is_signed > extra_operations;
    typedef base_type::storage_type storage_type;
    typedef value_type value_arg_type;

private:
    typedef atomics::detail::integral_constant< bool, atomics::detail::alignment_of< value_type >::value <= operations::storage_alignment > use_bitwise_cast;

public:
    BOOST_DEFAULTED_FUNCTION(base_atomic_ref(base_atomic_ref const& that) BOOST_ATOMIC_DETAIL_DEF_NOEXCEPT_DECL, BOOST_ATOMIC_DETAIL_DEF_NOEXCEPT_IMPL : base_type(static_cast< base_type const& >(that)) {})
    BOOST_FORCEINLINE explicit base_atomic_ref(value_type& v) BOOST_NOEXCEPT : base_type(v)
    {
    }

    // Standard methods
    BOOST_FORCEINLINE void store(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        BOOST_ASSERT(order != memory_order_consume);
        BOOST_ASSERT(order != memory_order_acquire);
        BOOST_ASSERT(order != memory_order_acq_rel);

        operations::store(this->storage(), static_cast< storage_type >(v), order);
    }

    BOOST_FORCEINLINE value_type load(memory_order order = memory_order_seq_cst) const BOOST_NOEXCEPT
    {
        BOOST_ASSERT(order != memory_order_release);
        BOOST_ASSERT(order != memory_order_acq_rel);

        return !!operations::load(this->storage(), order);
    }

    BOOST_FORCEINLINE value_type exchange(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return !!operations::exchange(this->storage(), static_cast< storage_type >(v), order);
    }

    BOOST_FORCEINLINE bool compare_exchange_strong(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order) BOOST_NOEXCEPT
    {
        BOOST_ASSERT(failure_order != memory_order_release);
        BOOST_ASSERT(failure_order != memory_order_acq_rel);
        BOOST_ASSERT(cas_failure_order_must_not_be_stronger_than_success_order(success_order, failure_order));

        return compare_exchange_strong_impl(expected, desired, success_order, failure_order, use_bitwise_cast());
    }

    BOOST_FORCEINLINE bool compare_exchange_strong(value_type& expected, value_arg_type desired, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return compare_exchange_strong(expected, desired, order, atomics::detail::deduce_failure_order(order));
    }

    BOOST_FORCEINLINE bool compare_exchange_weak(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order) BOOST_NOEXCEPT
    {
        BOOST_ASSERT(failure_order != memory_order_release);
        BOOST_ASSERT(failure_order != memory_order_acq_rel);
        BOOST_ASSERT(cas_failure_order_must_not_be_stronger_than_success_order(success_order, failure_order));

        return compare_exchange_weak_impl(expected, desired, success_order, failure_order, use_bitwise_cast());
    }

    BOOST_FORCEINLINE bool compare_exchange_weak(value_type& expected, value_arg_type desired, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return compare_exchange_weak(expected, desired, order, atomics::detail::deduce_failure_order(order));
    }

    BOOST_DELETED_FUNCTION(base_atomic_ref& operator=(base_atomic_ref const&))

private:
    BOOST_FORCEINLINE bool compare_exchange_strong_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::false_type) const BOOST_NOEXCEPT
    {
#if defined(BOOST_ATOMIC_DETAIL_STORAGE_TYPE_MAY_ALIAS)
        return operations::compare_exchange_strong(this->storage(), reinterpret_cast< storage_type& >(expected), static_cast< storage_type >(desired), success_order, failure_order);
#else
        return compare_exchange_strong_impl(expected, desired, success_order, failure_order, atomics::detail::true_type());
#endif
    }

    BOOST_FORCEINLINE bool compare_exchange_strong_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::true_type) const BOOST_NOEXCEPT
    {
        storage_type old_value = static_cast< storage_type >(expected);
        const bool res = operations::compare_exchange_strong(this->storage(), old_value, static_cast< storage_type >(desired), success_order, failure_order);
        expected = !!old_value;
        return res;
    }

    BOOST_FORCEINLINE bool compare_exchange_weak_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::false_type) const BOOST_NOEXCEPT
    {
#if defined(BOOST_ATOMIC_DETAIL_STORAGE_TYPE_MAY_ALIAS)
        return operations::compare_exchange_weak(this->storage(), reinterpret_cast< storage_type& >(expected), static_cast< storage_type >(desired), success_order, failure_order);
#else
        return compare_exchange_weak_impl(expected, desired, success_order, failure_order, atomics::detail::true_type());
#endif
    }

    BOOST_FORCEINLINE bool compare_exchange_weak_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::true_type) const BOOST_NOEXCEPT
    {
        storage_type old_value = static_cast< storage_type >(expected);
        const bool res = operations::compare_exchange_weak(this->storage(), old_value, static_cast< storage_type >(desired), success_order, failure_order);
        expected = !!old_value;
        return res;
    }
};


#if !defined(BOOST_ATOMIC_NO_FLOATING_POINT)

//! Implementation for floating point types
template< typename T >
class base_atomic_ref< T, float > :
    public base_atomic_ref_common< T, false >
{
private:
    typedef base_atomic_ref_common< T, false > base_type;

public:
    typedef typename base_type::value_type value_type;
    typedef typename base_type::value_type difference_type;

protected:
    typedef typename base_type::operations operations;
    typedef atomics::detail::extra_operations< operations, operations::storage_size, operations::is_signed > extra_operations;
    typedef atomics::detail::fp_operations< extra_operations, value_type, operations::storage_size > fp_operations;
    typedef atomics::detail::extra_fp_operations< fp_operations, value_type, operations::storage_size > extra_fp_operations;
    typedef typename base_type::storage_type storage_type;
    typedef value_type value_arg_type;

private:
    typedef atomics::detail::integral_constant< bool, atomics::detail::value_sizeof< value_type >::value != sizeof(storage_type) > has_padding_bits;
    typedef atomics::detail::integral_constant< bool, has_padding_bits::value || atomics::detail::alignment_of< value_type >::value <= operations::storage_alignment > use_bitwise_cast;

public:
    BOOST_DEFAULTED_FUNCTION(base_atomic_ref(base_atomic_ref const& that) BOOST_ATOMIC_DETAIL_DEF_NOEXCEPT_DECL, BOOST_ATOMIC_DETAIL_DEF_NOEXCEPT_IMPL : base_type(static_cast< base_type const& >(that)) {})
    BOOST_FORCEINLINE explicit base_atomic_ref(value_type& v) BOOST_NOEXCEPT : base_type(v)
    {
        this->clear_padding_bits(has_padding_bits());
    }

    BOOST_FORCEINLINE void store(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        BOOST_ASSERT(order != memory_order_consume);
        BOOST_ASSERT(order != memory_order_acquire);
        BOOST_ASSERT(order != memory_order_acq_rel);

        operations::store(this->storage(), atomics::detail::bitwise_fp_cast< storage_type >(v), order);
    }

    BOOST_FORCEINLINE value_type load(memory_order order = memory_order_seq_cst) const BOOST_NOEXCEPT
    {
        BOOST_ASSERT(order != memory_order_release);
        BOOST_ASSERT(order != memory_order_acq_rel);

        return atomics::detail::bitwise_fp_cast< value_type >(operations::load(this->storage(), order));
    }

    BOOST_FORCEINLINE value_type fetch_add(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return fp_operations::fetch_add(this->storage(), v, order);
    }

    BOOST_FORCEINLINE value_type fetch_sub(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return fp_operations::fetch_sub(this->storage(), v, order);
    }

    BOOST_FORCEINLINE value_type exchange(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::bitwise_fp_cast< value_type >(operations::exchange(this->storage(), atomics::detail::bitwise_fp_cast< storage_type >(v), order));
    }

    BOOST_FORCEINLINE bool compare_exchange_strong(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order) BOOST_NOEXCEPT
    {
        BOOST_ASSERT(failure_order != memory_order_release);
        BOOST_ASSERT(failure_order != memory_order_acq_rel);
        BOOST_ASSERT(cas_failure_order_must_not_be_stronger_than_success_order(success_order, failure_order));

        return compare_exchange_strong_impl(expected, desired, success_order, failure_order, use_bitwise_cast());
    }

    BOOST_FORCEINLINE bool compare_exchange_strong(value_type& expected, value_arg_type desired, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return compare_exchange_strong(expected, desired, order, atomics::detail::deduce_failure_order(order));
    }

    BOOST_FORCEINLINE bool compare_exchange_weak(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order) BOOST_NOEXCEPT
    {
        BOOST_ASSERT(failure_order != memory_order_release);
        BOOST_ASSERT(failure_order != memory_order_acq_rel);
        BOOST_ASSERT(cas_failure_order_must_not_be_stronger_than_success_order(success_order, failure_order));

        return compare_exchange_weak_impl(expected, desired, success_order, failure_order, use_bitwise_cast());
    }

    BOOST_FORCEINLINE bool compare_exchange_weak(value_type& expected, value_arg_type desired, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return compare_exchange_weak(expected, desired, order, atomics::detail::deduce_failure_order(order));
    }

    // Boost.Atomic extensions
    BOOST_FORCEINLINE value_type fetch_negate(memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return extra_fp_operations::fetch_negate(this->storage(), order);
    }

    BOOST_FORCEINLINE value_type add(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return extra_fp_operations::add(this->storage(), v, order);
    }

    BOOST_FORCEINLINE value_type sub(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return extra_fp_operations::sub(this->storage(), v, order);
    }

    BOOST_FORCEINLINE value_type negate(memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return extra_fp_operations::negate(this->storage(), order);
    }

    BOOST_FORCEINLINE void opaque_add(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        extra_fp_operations::opaque_add(this->storage(), v, order);
    }

    BOOST_FORCEINLINE void opaque_sub(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        extra_fp_operations::opaque_sub(this->storage(), v, order);
    }

    BOOST_FORCEINLINE void opaque_negate(memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        extra_fp_operations::opaque_negate(this->storage(), order);
    }

    // Operators
    BOOST_FORCEINLINE value_type operator+=(difference_type v) BOOST_NOEXCEPT
    {
        return add(v);
    }

    BOOST_FORCEINLINE value_type operator-=(difference_type v) BOOST_NOEXCEPT
    {
        return sub(v);
    }

    BOOST_DELETED_FUNCTION(base_atomic_ref& operator=(base_atomic_ref const&))

private:
    BOOST_FORCEINLINE void clear_padding_bits(atomics::detail::false_type) const BOOST_NOEXCEPT
    {
    }

    BOOST_FORCEINLINE void clear_padding_bits(atomics::detail::true_type) const BOOST_NOEXCEPT
    {
        storage_type old_value = operations::load(this->storage(), boost::memory_order_relaxed);
        while (true)
        {
            storage_type new_value = old_value;
            atomics::detail::clear_tail_padding_bits< atomics::detail::value_sizeof< value_type >::value >(new_value);
            bool res = operations::compare_exchange_weak(this->storage(), old_value, new_value, boost::memory_order_relaxed, boost::memory_order_relaxed);
            if (BOOST_LIKELY(res))
                break;
        }
    }

    BOOST_FORCEINLINE bool compare_exchange_strong_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::false_type) const BOOST_NOEXCEPT
    {
#if defined(BOOST_ATOMIC_DETAIL_STORAGE_TYPE_MAY_ALIAS)
        return operations::compare_exchange_strong(this->storage(), reinterpret_cast< storage_type& >(expected), atomics::detail::bitwise_fp_cast< storage_type >(desired), success_order, failure_order);
#else
        return compare_exchange_strong_impl(expected, desired, success_order, failure_order, atomics::detail::true_type());
#endif
    }

    BOOST_FORCEINLINE bool compare_exchange_strong_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::true_type) const BOOST_NOEXCEPT
    {
        storage_type old_value = atomics::detail::bitwise_fp_cast< storage_type >(expected);
        const bool res = operations::compare_exchange_strong(this->storage(), old_value, atomics::detail::bitwise_fp_cast< storage_type >(desired), success_order, failure_order);
        expected = atomics::detail::bitwise_fp_cast< value_type >(old_value);
        return res;
    }

    BOOST_FORCEINLINE bool compare_exchange_weak_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::false_type) const BOOST_NOEXCEPT
    {
#if defined(BOOST_ATOMIC_DETAIL_STORAGE_TYPE_MAY_ALIAS)
        return operations::compare_exchange_weak(this->storage(), reinterpret_cast< storage_type& >(expected), atomics::detail::bitwise_fp_cast< storage_type >(desired), success_order, failure_order);
#else
        return compare_exchange_weak_impl(expected, desired, success_order, failure_order, atomics::detail::true_type());
#endif
    }

    BOOST_FORCEINLINE bool compare_exchange_weak_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::true_type) const BOOST_NOEXCEPT
    {
        storage_type old_value = atomics::detail::bitwise_fp_cast< storage_type >(expected);
        const bool res = operations::compare_exchange_weak(this->storage(), old_value, atomics::detail::bitwise_fp_cast< storage_type >(desired), success_order, failure_order);
        expected = atomics::detail::bitwise_fp_cast< value_type >(old_value);
        return res;
    }
};

#endif // !defined(BOOST_ATOMIC_NO_FLOATING_POINT)


//! Implementation for pointers to object types
template< typename T >
class base_atomic_ref< T*, void* > :
    public base_atomic_ref_common< T*, false >
{
private:
    typedef base_atomic_ref_common< T*, false > base_type;

public:
    typedef typename base_type::value_type value_type;
    typedef std::ptrdiff_t difference_type;

protected:
    typedef typename base_type::operations operations;
    typedef atomics::detail::extra_operations< operations, operations::storage_size, operations::is_signed > extra_operations;
    typedef typename base_type::storage_type storage_type;
    typedef value_type value_arg_type;

private:
    typedef atomics::detail::integral_constant< bool, atomics::detail::alignment_of< value_type >::value <= operations::storage_alignment > use_bitwise_cast;

    // uintptr_storage_type is the minimal storage type that is enough to store pointers. The actual storage_type theoretically may be larger,
    // if the target architecture only supports atomic ops on larger data. Typically, though, they are the same type.
    typedef atomics::detail::uintptr_t uintptr_storage_type;

public:
    BOOST_DEFAULTED_FUNCTION(base_atomic_ref(base_atomic_ref const& that) BOOST_ATOMIC_DETAIL_DEF_NOEXCEPT_DECL, BOOST_ATOMIC_DETAIL_DEF_NOEXCEPT_IMPL : base_type(static_cast< base_type const& >(that)) {})
    BOOST_FORCEINLINE explicit base_atomic_ref(value_type& v) BOOST_NOEXCEPT : base_type(v)
    {
    }

    // Standard methods
    BOOST_FORCEINLINE void store(value_arg_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        BOOST_ASSERT(order != memory_order_consume);
        BOOST_ASSERT(order != memory_order_acquire);
        BOOST_ASSERT(order != memory_order_acq_rel);

        operations::store(this->storage(), atomics::detail::bitwise_cast< uintptr_storage_type >(v), order);
    }

    BOOST_FORCEINLINE value_type load(memory_order order = memory_order_seq_cst) const BOOST_NOEXCEPT
    {
        BOOST_ASSERT(order != memory_order_release);
        BOOST_ASSERT(order != memory_order_acq_rel);

        return atomics::detail::bitwise_cast< value_type >(static_cast< uintptr_storage_type >(operations::load(this->storage(), order)));
    }

    BOOST_FORCEINLINE value_type fetch_add(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::bitwise_cast< value_type >(static_cast< uintptr_storage_type >(operations::fetch_add(this->storage(), static_cast< uintptr_storage_type >(v * sizeof(T)), order)));
    }

    BOOST_FORCEINLINE value_type fetch_sub(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::bitwise_cast< value_type >(static_cast< uintptr_storage_type >(operations::fetch_sub(this->storage(), static_cast< uintptr_storage_type >(v * sizeof(T)), order)));
    }

    BOOST_FORCEINLINE value_type exchange(value_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::bitwise_cast< value_type >(static_cast< uintptr_storage_type >(operations::exchange(this->storage(), atomics::detail::bitwise_cast< uintptr_storage_type >(v), order)));
    }

    BOOST_FORCEINLINE bool compare_exchange_strong(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order) BOOST_NOEXCEPT
    {
        BOOST_ASSERT(failure_order != memory_order_release);
        BOOST_ASSERT(failure_order != memory_order_acq_rel);
        BOOST_ASSERT(cas_failure_order_must_not_be_stronger_than_success_order(success_order, failure_order));

        return compare_exchange_strong_impl(expected, desired, success_order, failure_order, use_bitwise_cast());
    }

    BOOST_FORCEINLINE bool compare_exchange_strong(value_type& expected, value_arg_type desired, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return compare_exchange_strong(expected, desired, order, atomics::detail::deduce_failure_order(order));
    }

    BOOST_FORCEINLINE bool compare_exchange_weak(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order) BOOST_NOEXCEPT
    {
        BOOST_ASSERT(failure_order != memory_order_release);
        BOOST_ASSERT(failure_order != memory_order_acq_rel);
        BOOST_ASSERT(cas_failure_order_must_not_be_stronger_than_success_order(success_order, failure_order));

        return compare_exchange_weak_impl(expected, desired, success_order, failure_order, use_bitwise_cast());
    }

    BOOST_FORCEINLINE bool compare_exchange_weak(value_type& expected, value_arg_type desired, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return compare_exchange_weak(expected, desired, order, atomics::detail::deduce_failure_order(order));
    }

    // Boost.Atomic extensions
    BOOST_FORCEINLINE value_type add(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::bitwise_cast< value_type >(static_cast< uintptr_storage_type >(extra_operations::add(this->storage(), static_cast< uintptr_storage_type >(v * sizeof(T)), order)));
    }

    BOOST_FORCEINLINE value_type sub(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return atomics::detail::bitwise_cast< value_type >(static_cast< uintptr_storage_type >(extra_operations::sub(this->storage(), static_cast< uintptr_storage_type >(v * sizeof(T)), order)));
    }

    BOOST_FORCEINLINE void opaque_add(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        extra_operations::opaque_add(this->storage(), static_cast< uintptr_storage_type >(v * sizeof(T)), order);
    }

    BOOST_FORCEINLINE void opaque_sub(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        extra_operations::opaque_sub(this->storage(), static_cast< uintptr_storage_type >(v * sizeof(T)), order);
    }

    BOOST_FORCEINLINE bool add_and_test(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return extra_operations::add_and_test(this->storage(), static_cast< uintptr_storage_type >(v * sizeof(T)), order);
    }

    BOOST_FORCEINLINE bool sub_and_test(difference_type v, memory_order order = memory_order_seq_cst) BOOST_NOEXCEPT
    {
        return extra_operations::sub_and_test(this->storage(), static_cast< uintptr_storage_type >(v * sizeof(T)), order);
    }

    // Operators
    BOOST_FORCEINLINE value_type operator++(int) BOOST_NOEXCEPT
    {
        return fetch_add(1);
    }

    BOOST_FORCEINLINE value_type operator++() BOOST_NOEXCEPT
    {
        return add(1);
    }

    BOOST_FORCEINLINE value_type operator--(int) BOOST_NOEXCEPT
    {
        return fetch_sub(1);
    }

    BOOST_FORCEINLINE value_type operator--() BOOST_NOEXCEPT
    {
        return sub(1);
    }

    BOOST_FORCEINLINE value_type operator+=(difference_type v) BOOST_NOEXCEPT
    {
        return add(v);
    }

    BOOST_FORCEINLINE value_type operator-=(difference_type v) BOOST_NOEXCEPT
    {
        return sub(v);
    }

    BOOST_DELETED_FUNCTION(base_atomic_ref& operator=(base_atomic_ref const&))

private:
    BOOST_FORCEINLINE bool compare_exchange_strong_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::false_type) const BOOST_NOEXCEPT
    {
#if defined(BOOST_ATOMIC_DETAIL_STORAGE_TYPE_MAY_ALIAS)
        return operations::compare_exchange_strong(this->storage(), reinterpret_cast< storage_type& >(expected), atomics::detail::bitwise_cast< uintptr_storage_type >(desired), success_order, failure_order);
#else
        return compare_exchange_strong_impl(expected, desired, success_order, failure_order, atomics::detail::true_type());
#endif
    }

    BOOST_FORCEINLINE bool compare_exchange_strong_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::true_type) const BOOST_NOEXCEPT
    {
        storage_type old_value = atomics::detail::bitwise_cast< uintptr_storage_type >(expected);
        const bool res = operations::compare_exchange_strong(this->storage(), old_value, atomics::detail::bitwise_cast< uintptr_storage_type >(desired), success_order, failure_order);
        expected = atomics::detail::bitwise_cast< value_type >(static_cast< uintptr_storage_type >(old_value));
        return res;
    }

    BOOST_FORCEINLINE bool compare_exchange_weak_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::false_type) const BOOST_NOEXCEPT
    {
#if defined(BOOST_ATOMIC_DETAIL_STORAGE_TYPE_MAY_ALIAS)
        return operations::compare_exchange_weak(this->storage(), reinterpret_cast< storage_type& >(expected), atomics::detail::bitwise_cast< uintptr_storage_type >(desired), success_order, failure_order);
#else
        return compare_exchange_weak_impl(expected, desired, success_order, failure_order, atomics::detail::true_type());
#endif
    }

    BOOST_FORCEINLINE bool compare_exchange_weak_impl(value_type& expected, value_arg_type desired, memory_order success_order, memory_order failure_order, atomics::detail::true_type) const BOOST_NOEXCEPT
    {
        storage_type old_value = atomics::detail::bitwise_cast< uintptr_storage_type >(expected);
        const bool res = operations::compare_exchange_weak(this->storage(), old_value, atomics::detail::bitwise_cast< uintptr_storage_type >(desired), success_order, failure_order);
        expected = atomics::detail::bitwise_cast< value_type >(static_cast< uintptr_storage_type >(old_value));
        return res;
    }
};

} // namespace detail

template< typename T >
class atomic_ref :
    public atomics::detail::base_atomic_ref< T, typename atomics::detail::classify< T >::type >
{
private:
    typedef atomics::detail::base_atomic_ref< T, typename atomics::detail::classify< T >::type > base_type;
    typedef typename base_type::value_arg_type value_arg_type;

public:
    typedef typename base_type::value_type value_type;

    BOOST_STATIC_ASSERT_MSG(sizeof(value_type) > 0u, "boost::atomic_ref<T> requires T to be a complete type");
#if !defined(BOOST_ATOMIC_DETAIL_NO_CXX11_IS_TRIVIALLY_COPYABLE)
    BOOST_STATIC_ASSERT_MSG(atomics::detail::is_trivially_copyable< value_type >::value, "boost::atomic_ref<T> requires T to be a trivially copyable type");
#endif

private:
    typedef typename base_type::storage_type storage_type;

public:
    BOOST_DEFAULTED_FUNCTION(atomic_ref(atomic_ref const& that) BOOST_ATOMIC_DETAIL_DEF_NOEXCEPT_DECL, BOOST_ATOMIC_DETAIL_DEF_NOEXCEPT_IMPL : base_type(static_cast< base_type const& >(that)) {})
    BOOST_FORCEINLINE explicit atomic_ref(value_type& v) BOOST_NOEXCEPT : base_type(v)
    {
        // Check that referenced object alignment satisfies required alignment
        BOOST_ASSERT((((atomics::detail::uintptr_t)this->m_value) & (base_type::required_alignment - 1u)) == 0u);
    }

    BOOST_FORCEINLINE value_type operator= (value_arg_type v) BOOST_NOEXCEPT
    {
        this->store(v);
        return v;
    }

    BOOST_FORCEINLINE operator value_type() const BOOST_NOEXCEPT
    {
        return this->load();
    }

    BOOST_FORCEINLINE bool is_lock_free() const BOOST_NOEXCEPT
    {
        // C++20 specifies that is_lock_free returns true if operations on *all* objects of the atomic_ref<T> type are lock-free.
        // This does not allow to return true or false depending on the referenced object runtime alignment. Currently, Boost.Atomic
        // follows this specification, although we may support runtime alignment checking in the future.
        return base_type::is_always_lock_free;
    }

    BOOST_FORCEINLINE value_type& value() const BOOST_NOEXCEPT { return *this->m_value; }

    BOOST_DELETED_FUNCTION(atomic_ref& operator= (atomic_ref const&))
};

} // namespace atomics
} // namespace boost

#if defined(BOOST_MSVC)
#pragma warning(pop)
#endif

#endif // BOOST_ATOMIC_DETAIL_ATOMIC_REF_TEMPLATE_HPP_INCLUDED_
