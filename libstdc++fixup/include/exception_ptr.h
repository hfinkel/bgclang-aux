/* workaround for LLVM PR13364 */
#ifdef __GXX_EXPERIMENTAL_CXX0X__
namespace std { class type_info; }
#endif
#include_next <exception_ptr.h>

// -*- C++ -*-
//===-------------------------- exception ---------------------------------===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is dual licensed under the MIT and the University of Illinois Open
// Source Licenses. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

#ifndef _LIBCPP_EXCEPTION
#define _LIBCPP_EXCEPTION

#ifndef _NOEXCEPT
#if (__has_feature(cxx_noexcept))
#  define _NOEXCEPT noexcept
#else
#  define _NOEXCEPT throw()
#endif
#endif

namespace std {

template<class _Ep>
exception_ptr
make_exception_ptr(_Ep __e) _NOEXCEPT
{
#ifndef _LIBCPP_NO_EXCEPTIONS
    try
    {
        throw __e;
    }
    catch (...)
    {
        return current_exception();
    }
#endif  // _LIBCPP_NO_EXCEPTIONS
}

}  // std

#endif  // _LIBCPP_EXCEPTION

