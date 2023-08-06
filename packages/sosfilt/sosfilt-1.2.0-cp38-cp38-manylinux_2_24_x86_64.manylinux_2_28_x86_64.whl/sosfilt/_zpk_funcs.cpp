#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/float.hpp>
#include <pythonic/include/types/complex.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/types/complex.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/float.hpp>
#include <pythonic/include/builtins/ValueError.hpp>
#include <pythonic/include/builtins/abs.hpp>
#include <pythonic/include/builtins/assert.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/len.hpp>
#include <pythonic/include/builtins/list.hpp>
#include <pythonic/include/builtins/max.hpp>
#include <pythonic/include/builtins/pythran/and_.hpp>
#include <pythonic/include/builtins/pythran/make_shape.hpp>
#include <pythonic/include/builtins/pythran/static_list.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/numpy/abs.hpp>
#include <pythonic/include/numpy/append.hpp>
#include <pythonic/include/numpy/argmin.hpp>
#include <pythonic/include/numpy/argsort.hpp>
#include <pythonic/include/numpy/array.hpp>
#include <pythonic/include/numpy/complex128.hpp>
#include <pythonic/include/numpy/concatenate.hpp>
#include <pythonic/include/numpy/conj.hpp>
#include <pythonic/include/numpy/convolve.hpp>
#include <pythonic/include/numpy/delete_.hpp>
#include <pythonic/include/numpy/diff.hpp>
#include <pythonic/include/numpy/empty.hpp>
#include <pythonic/include/numpy/finfo.hpp>
#include <pythonic/include/numpy/float64.hpp>
#include <pythonic/include/numpy/isreal.hpp>
#include <pythonic/include/numpy/lexsort.hpp>
#include <pythonic/include/numpy/nonzero.hpp>
#include <pythonic/include/numpy/ones.hpp>
#include <pythonic/include/numpy/sum.hpp>
#include <pythonic/include/numpy/zeros.hpp>
#include <pythonic/include/numpy/zeros_like.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/eq.hpp>
#include <pythonic/include/operator_/floordiv.hpp>
#include <pythonic/include/operator_/gt.hpp>
#include <pythonic/include/operator_/invert.hpp>
#include <pythonic/include/operator_/le.hpp>
#include <pythonic/include/operator_/lt.hpp>
#include <pythonic/include/operator_/mod.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/ne.hpp>
#include <pythonic/include/operator_/neg.hpp>
#include <pythonic/include/operator_/not_.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/ValueError.hpp>
#include <pythonic/builtins/abs.hpp>
#include <pythonic/builtins/assert.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/len.hpp>
#include <pythonic/builtins/list.hpp>
#include <pythonic/builtins/max.hpp>
#include <pythonic/builtins/pythran/and_.hpp>
#include <pythonic/builtins/pythran/make_shape.hpp>
#include <pythonic/builtins/pythran/static_list.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/numpy/abs.hpp>
#include <pythonic/numpy/append.hpp>
#include <pythonic/numpy/argmin.hpp>
#include <pythonic/numpy/argsort.hpp>
#include <pythonic/numpy/array.hpp>
#include <pythonic/numpy/complex128.hpp>
#include <pythonic/numpy/concatenate.hpp>
#include <pythonic/numpy/conj.hpp>
#include <pythonic/numpy/convolve.hpp>
#include <pythonic/numpy/delete_.hpp>
#include <pythonic/numpy/diff.hpp>
#include <pythonic/numpy/empty.hpp>
#include <pythonic/numpy/finfo.hpp>
#include <pythonic/numpy/float64.hpp>
#include <pythonic/numpy/isreal.hpp>
#include <pythonic/numpy/lexsort.hpp>
#include <pythonic/numpy/nonzero.hpp>
#include <pythonic/numpy/ones.hpp>
#include <pythonic/numpy/sum.hpp>
#include <pythonic/numpy/zeros.hpp>
#include <pythonic/numpy/zeros_like.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/eq.hpp>
#include <pythonic/operator_/floordiv.hpp>
#include <pythonic/operator_/gt.hpp>
#include <pythonic/operator_/invert.hpp>
#include <pythonic/operator_/le.hpp>
#include <pythonic/operator_/lt.hpp>
#include <pythonic/operator_/mod.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/ne.hpp>
#include <pythonic/operator_/neg.hpp>
#include <pythonic/operator_/not_.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran__zpk_funcs
{
  struct poly
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type1;
      typedef std::integral_constant<long, 1> __type2;
      typedef decltype(std::declval<__type1>()(std::declval<__type2>())) __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type4;
      typedef __type4 __type5;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type5>())) __type6;
      typedef typename pythonic::assignable<__type6>::type __type7;
      typedef __type7 __type8;
      typedef decltype(std::declval<__type0>()(std::declval<__type3>(), std::declval<__type8>())) __type9;
      typedef typename pythonic::lazy<__type9>::type __type10;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::convolve{})>::type>::type __type11;
      typedef __type10 __type12;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::array{})>::type>::type __type13;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::static_list{})>::type>::type __type14;
      typedef long __type15;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type17;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type18;
      typedef decltype(std::declval<__type18>()(std::declval<__type5>())) __type20;
      typedef decltype(std::declval<__type17>()(std::declval<__type20>())) __type21;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type21>::type::iterator>::value_type>::type __type22;
      typedef __type22 __type23;
      typedef decltype(std::declval<__type5>()[std::declval<__type23>()]) __type24;
      typedef decltype(pythonic::operator_::neg(std::declval<__type24>())) __type25;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type15>(), std::declval<__type25>())) __type26;
      typedef decltype(std::declval<__type14>()(std::declval<__type26>())) __type27;
      typedef decltype(std::declval<__type13>()(std::declval<__type27>(), std::declval<__type8>())) __type29;
      typedef pythonic::types::str __type30;
      typedef decltype(std::declval<__type11>()(std::declval<__type12>(), std::declval<__type29>(), std::declval<__type30>())) __type31;
      typedef typename pythonic::lazy<__type31>::type __type32;
      typedef typename __combined<__type10,__type32>::type __type33;
      typedef __type33 __type34;
      typedef typename pythonic::returnable<__type34>::type __type35;
      typedef __type35 result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& zeros) const
    ;
  }  ;
  struct _nearest_real_complex_idx
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::argsort{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::abs{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef __type2 __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type4;
      typedef __type4 __type5;
      typedef decltype(pythonic::operator_::sub(std::declval<__type3>(), std::declval<__type5>())) __type6;
      typedef decltype(std::declval<__type1>()(std::declval<__type6>())) __type7;
      typedef decltype(std::declval<__type0>()(std::declval<__type7>())) __type8;
      typedef typename pythonic::assignable<__type8>::type __type9;
      typedef __type9 __type10;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::nonzero{})>::type>::type __type11;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::isreal{})>::type>::type __type12;
      typedef decltype(std::declval<__type3>()[std::declval<__type10>()]) __type15;
      typedef decltype(std::declval<__type12>()(std::declval<__type15>())) __type16;
      typedef typename pythonic::lazy<__type16>::type __type17;
      typedef __type17 __type18;
      typedef decltype(pythonic::operator_::invert(std::declval<__type18>())) __type19;
      typedef typename pythonic::lazy<__type19>::type __type20;
      typedef typename __combined<__type17,__type20>::type __type21;
      typedef __type21 __type22;
      typedef decltype(std::declval<__type11>()(std::declval<__type22>())) __type23;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type23>::type>::type __type24;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type24>::type>::type __type25;
      typedef decltype(std::declval<__type10>()[std::declval<__type25>()]) __type26;
      typedef typename pythonic::returnable<__type26>::type __type27;
      typedef __type27 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& fro, argument_type1&& to, argument_type2&& which) const
    ;
  }  ;
  struct _cplxreal
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef __type0 __type1;
      typedef __type1 __type2;
      typedef typename pythonic::assignable<__type1>::type __type3;
      typedef __type3 __type4;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::lexsort{})>::type>::type __type5;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::abs{})>::type>::type __type6;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type4>())) __type8;
      typedef decltype(std::declval<__type6>()(std::declval<__type8>())) __type9;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, std::declval<__type4>())) __type11;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type9>(), std::declval<__type11>())) __type12;
      typedef decltype(std::declval<__type5>()(std::declval<__type12>())) __type13;
      typedef decltype(std::declval<__type4>()[std::declval<__type13>()]) __type14;
      typedef __type14 __type15;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type16;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type17;
      typedef std::integral_constant<long, 0> __type18;
      typedef decltype(std::declval<__type17>()(std::declval<__type18>())) __type19;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::float64{})>::type>::type __type20;
      typedef decltype(std::declval<__type16>()(std::declval<__type19>(), std::declval<__type20>())) __type21;
      typedef typename pythonic::assignable<__type14>::type __type22;
      typedef __type22 __type23;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type23>())) __type25;
      typedef decltype(std::declval<__type6>()(std::declval<__type25>())) __type26;
      typedef long __type27;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::finfo{})>::type>::type __type28;
      typedef double __type29;
      typedef decltype(pythonic::operator_::mul(std::declval<__type29>(), std::declval<__type4>())) __type31;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type31>())) __type32;
      typedef decltype(std::declval<__type28>()(std::declval<__type32>())) __type33;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::EPS{}, std::declval<__type33>())) __type34;
      typedef decltype(pythonic::operator_::mul(std::declval<__type27>(), std::declval<__type34>())) __type35;
      typedef typename pythonic::assignable<__type35>::type __type36;
      typedef __type36 __type37;
      typedef decltype(std::declval<__type6>()(std::declval<__type23>())) __type39;
      typedef decltype(pythonic::operator_::mul(std::declval<__type37>(), std::declval<__type39>())) __type40;
      typedef decltype(pythonic::operator_::le(std::declval<__type26>(), std::declval<__type40>())) __type41;
      typedef typename pythonic::assignable<__type41>::type __type42;
      typedef __type42 __type43;
      typedef decltype(std::declval<__type23>()[std::declval<__type43>()]) __type44;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, std::declval<__type44>())) __type45;
      typedef typename pythonic::assignable<__type45>::type __type46;
      typedef __type46 __type47;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type21>(), std::declval<__type47>())) __type48;
      typedef decltype(pythonic::operator_::invert(std::declval<__type43>())) __type51;
      typedef decltype(std::declval<__type23>()[std::declval<__type51>()]) __type52;
      typedef typename pythonic::assignable<__type52>::type __type53;
      typedef __type53 __type54;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type54>())) __type56;
      typedef decltype(pythonic::operator_::gt(std::declval<__type56>(), std::declval<__type27>())) __type57;
      typedef decltype(std::declval<__type54>()[std::declval<__type57>()]) __type58;
      typedef typename pythonic::assignable<__type58>::type __type59;
      typedef __type59 __type60;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type __type61;
      typedef container<typename std::remove_reference<__type58>::type> __type62;
      typedef typename __combined<__type53,__type62>::type __type63;
      typedef __type63 __type64;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type64>())) __type66;
      typedef decltype(pythonic::operator_::lt(std::declval<__type66>(), std::declval<__type27>())) __type67;
      typedef decltype(std::declval<__type64>()[std::declval<__type67>()]) __type68;
      typedef typename pythonic::assignable<__type68>::type __type69;
      typedef __type69 __type70;
      typedef decltype(std::declval<__type61>()(std::declval<__type70>())) __type71;
      typedef decltype(pythonic::operator_::add(std::declval<__type60>(), std::declval<__type71>())) __type72;
      typedef decltype(pythonic::operator_::div(std::declval<__type72>(), std::declval<__type27>())) __type73;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type73>(), std::declval<__type47>())) __type75;
      typedef typename __combined<__type48,__type75>::type __type76;
      typedef typename pythonic::returnable<__type76>::type __type77;
      typedef __type2 __ptype0;
      typedef __type15 __ptype1;
      typedef __type77 result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& z) const
    ;
  }  ;
  struct zpk2tf
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type0;
      typedef __type0 __type1;
      typedef poly __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type3;
      typedef __type3 __type4;
      typedef decltype(std::declval<__type2>()(std::declval<__type4>())) __type5;
      typedef decltype(pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type5>())) __type6;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, std::declval<__type6>())) __type7;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type8;
      typedef __type8 __type9;
      typedef decltype(std::declval<__type2>()(std::declval<__type9>())) __type10;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, std::declval<__type10>())) __type11;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type7>(), std::declval<__type11>())) __type12;
      typedef typename pythonic::returnable<__type12>::type __type13;
      typedef __type13 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& z, argument_type1&& p, argument_type2&& k) const
    ;
  }  ;
  struct zpk2sos
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef __type0 __type1;
      typedef __type1 __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type3;
      typedef __type3 __type4;
      typedef __type4 __type5;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type6;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type7;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type8;
      typedef __type8 __type9;
      typedef std::integral_constant<long, 6> __type10;
      typedef decltype(std::declval<__type7>()(std::declval<__type9>(), std::declval<__type10>())) __type11;
      typedef decltype(std::declval<__type6>()(std::declval<__type11>())) __type12;
      typedef typename pythonic::assignable<__type12>::type __type13;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type14;
      typedef decltype(std::declval<__type14>()(std::declval<__type9>())) __type16;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type16>::type::iterator>::value_type>::type __type17;
      typedef __type17 __type18;
      typedef indexable<__type18> __type19;
      typedef typename __combined<__type13,__type19>::type __type20;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::concatenate{})>::type>::type __type21;
      typedef zpk2tf __type22;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros_like{})>::type>::type __type23;
      typedef std::integral_constant<long, 2> __type25;
      typedef decltype(std::declval<__type7>()(std::declval<__type9>(), std::declval<__type25>())) __type26;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::complex128{})>::type>::type __type27;
      typedef decltype(std::declval<__type6>()(std::declval<__type26>(), std::declval<__type27>())) __type28;
      typedef typename pythonic::assignable<__type28>::type __type29;
      typedef __type29 __type30;
      typedef decltype(std::declval<__type23>()(std::declval<__type30>())) __type31;
      typedef typename pythonic::assignable<__type31>::type __type32;
      typedef typename __combined<__type32,__type19>::type __type38;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::static_list{})>::type>::type __type39;
      typedef _cplxreal __type40;
      typedef typename pythonic::lazy<__type1>::type __type41;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::append{})>::type>::type __type42;
      typedef __type41 __type43;
      typedef long __type44;
      typedef decltype(std::declval<__type42>()(std::declval<__type43>(), std::declval<__type44>())) __type45;
      typedef typename pythonic::lazy<__type45>::type __type46;
      typedef typename __combined<__type41,__type46>::type __type47;
      typedef __type47 __type48;
      typedef typename _cplxreal::type<__type48>::__ptype0 __type49;
      typedef typename __combined<__type48,__type49>::type __type50;
      typedef typename _cplxreal::type<__type50>::__ptype1 __type51;
      typedef container<typename std::remove_reference<__type51>::type> __type52;
      typedef typename __combined<__type50,__type52>::type __type53;
      typedef decltype(std::declval<__type40>()(std::declval<__type53>())) __type54;
      typedef decltype(std::declval<__type21>()(std::declval<__type54>())) __type55;
      typedef typename pythonic::assignable<__type55>::type __type56;
      typedef __type56 __type57;
      typedef _nearest_real_complex_idx __type58;
      typedef typename pythonic::assignable<__type4>::type __type60;
      typedef __type60 __type61;
      typedef decltype(std::declval<__type42>()(std::declval<__type61>(), std::declval<__type44>())) __type62;
      typedef typename pythonic::assignable<__type62>::type __type63;
      typedef typename __combined<__type60,__type63>::type __type64;
      typedef __type64 __type65;
      typedef typename _cplxreal::type<__type65>::__ptype0 __type66;
      typedef typename __combined<__type65,__type66>::type __type67;
      typedef typename _cplxreal::type<__type67>::__ptype1 __type68;
      typedef container<typename std::remove_reference<__type68>::type> __type69;
      typedef typename __combined<__type67,__type69>::type __type70;
      typedef decltype(std::declval<__type40>()(std::declval<__type70>())) __type71;
      typedef decltype(std::declval<__type21>()(std::declval<__type71>())) __type72;
      typedef typename pythonic::assignable<__type72>::type __type73;
      typedef __type73 __type74;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::argmin{})>::type>::type __type75;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::abs{})>::type>::type __type76;
      typedef decltype(std::declval<__type76>()(std::declval<__type74>())) __type78;
      typedef decltype(pythonic::operator_::sub(std::declval<__type44>(), std::declval<__type78>())) __type79;
      typedef decltype(std::declval<__type76>()(std::declval<__type79>())) __type80;
      typedef decltype(std::declval<__type75>()(std::declval<__type80>())) __type81;
      typedef typename pythonic::assignable<__type81>::type __type82;
      typedef __type82 __type83;
      typedef decltype(std::declval<__type74>()[std::declval<__type83>()]) __type84;
      typedef typename pythonic::assignable<__type84>::type __type85;
      typedef __type85 __type86;
      typedef pythonic::types::str __type87;
      typedef decltype(std::declval<__type58>()(std::declval<__type57>(), std::declval<__type86>(), std::declval<__type87>())) __type88;
      typedef typename pythonic::assignable<__type88>::type __type89;
      typedef __type89 __type90;
      typedef decltype(std::declval<__type57>()[std::declval<__type90>()]) __type91;
      typedef typename pythonic::assignable<__type91>::type __type92;
      typedef container<typename std::remove_reference<__type91>::type> __type93;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::delete_{})>::type>::type __type94;
      typedef typename __combined<__type56,__type93,__type93,__type93,__type93>::type __type95;
      typedef __type95 __type96;
      typedef decltype(std::declval<__type94>()(std::declval<__type96>(), std::declval<__type90>())) __type98;
      typedef typename pythonic::assignable<__type98>::type __type99;
      typedef typename __combined<__type56,__type93,__type93,__type93,__type93,__type99>::type __type100;
      typedef __type100 __type101;
      typedef decltype(std::declval<__type58>()(std::declval<__type101>(), std::declval<__type86>(), std::declval<__type87>())) __type104;
      typedef typename pythonic::assignable<__type104>::type __type105;
      typedef decltype(pythonic::operator_::sub(std::declval<__type86>(), std::declval<__type101>())) __type108;
      typedef decltype(std::declval<__type76>()(std::declval<__type108>())) __type109;
      typedef decltype(std::declval<__type75>()(std::declval<__type109>())) __type110;
      typedef typename pythonic::assignable<__type110>::type __type111;
      typedef typename __combined<__type105,__type111>::type __type112;
      typedef __type112 __type113;
      typedef decltype(std::declval<__type101>()[std::declval<__type113>()]) __type114;
      typedef typename pythonic::assignable<__type114>::type __type115;
      typedef typename __combined<__type92,__type115>::type __type116;
      typedef __type116 __type117;
      typedef typename pythonic::assignable<__type44>::type __type118;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type __type119;
      typedef decltype(std::declval<__type119>()(std::declval<__type117>())) __type121;
      typedef typename pythonic::assignable<__type121>::type __type122;
      typedef container<typename std::remove_reference<__type114>::type> __type123;
      typedef typename __combined<__type56,__type93,__type93,__type93,__type93,__type99,__type123,__type123,__type123,__type123>::type __type124;
      typedef __type124 __type125;
      typedef decltype(std::declval<__type94>()(std::declval<__type125>(), std::declval<__type113>())) __type127;
      typedef typename pythonic::assignable<__type127>::type __type128;
      typedef typename __combined<__type56,__type93,__type93,__type93,__type93,__type99,__type123,__type123,__type123,__type123,__type128>::type __type129;
      typedef __type129 __type130;
      typedef decltype(std::declval<__type58>()(std::declval<__type130>(), std::declval<__type86>(), std::declval<__type87>())) __type133;
      typedef typename pythonic::assignable<__type133>::type __type134;
      typedef __type134 __type135;
      typedef decltype(std::declval<__type130>()[std::declval<__type135>()]) __type136;
      typedef typename pythonic::assignable<__type136>::type __type137;
      typedef container<typename std::remove_reference<__type136>::type> __type141;
      typedef typename __combined<__type56,__type93,__type93,__type93,__type93,__type99,__type123,__type123,__type123,__type123,__type128,__type141>::type __type142;
      typedef __type142 __type143;
      typedef decltype(std::declval<__type94>()(std::declval<__type143>(), std::declval<__type135>())) __type145;
      typedef typename pythonic::assignable<__type145>::type __type146;
      typedef typename __combined<__type56,__type93,__type93,__type93,__type93,__type99,__type123,__type123,__type123,__type123,__type128,__type141,__type146>::type __type147;
      typedef __type147 __type148;
      typedef decltype(std::declval<__type119>()(std::declval<__type86>())) __type151;
      typedef typename pythonic::assignable<__type151>::type __type152;
      typedef container<typename std::remove_reference<__type84>::type> __type156;
      typedef typename __combined<__type73,__type156,__type156>::type __type157;
      typedef __type157 __type158;
      typedef decltype(std::declval<__type94>()(std::declval<__type158>(), std::declval<__type83>())) __type160;
      typedef typename pythonic::assignable<__type160>::type __type161;
      typedef typename __combined<__type73,__type156,__type156,__type161>::type __type162;
      typedef __type162 __type163;
      typedef decltype(std::declval<__type58>()(std::declval<__type163>(), std::declval<__type117>(), std::declval<__type87>())) __type166;
      typedef typename pythonic::assignable<__type166>::type __type167;
      typedef __type167 __type168;
      typedef decltype(std::declval<__type163>()[std::declval<__type168>()]) __type169;
      typedef typename pythonic::assignable<__type169>::type __type170;
      typedef container<typename std::remove_reference<__type169>::type> __type171;
      typedef typename __combined<__type73,__type156,__type156,__type161,__type171>::type __type172;
      typedef __type172 __type173;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::nonzero{})>::type>::type __type174;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::isreal{})>::type>::type __type175;
      typedef decltype(std::declval<__type175>()(std::declval<__type173>())) __type177;
      typedef decltype(std::declval<__type174>()(std::declval<__type177>())) __type178;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type178>::type>::type __type179;
      typedef typename pythonic::assignable<__type179>::type __type180;
      typedef __type180 __type181;
      typedef decltype(std::declval<__type173>()[std::declval<__type181>()]) __type184;
      typedef decltype(std::declval<__type76>()(std::declval<__type184>())) __type185;
      typedef decltype(pythonic::operator_::sub(std::declval<__type185>(), std::declval<__type44>())) __type186;
      typedef decltype(std::declval<__type76>()(std::declval<__type186>())) __type187;
      typedef decltype(std::declval<__type75>()(std::declval<__type187>())) __type188;
      typedef decltype(std::declval<__type181>()[std::declval<__type188>()]) __type189;
      typedef typename pythonic::assignable<__type189>::type __type190;
      typedef typename __combined<__type167,__type190>::type __type191;
      typedef __type191 __type192;
      typedef decltype(std::declval<__type173>()[std::declval<__type192>()]) __type193;
      typedef typename pythonic::assignable<__type193>::type __type194;
      typedef typename __combined<__type118,__type152,__type152,__type170,__type194>::type __type195;
      typedef __type195 __type196;
      typedef decltype(std::declval<__type58>()(std::declval<__type148>(), std::declval<__type196>(), std::declval<__type87>())) __type197;
      typedef typename pythonic::assignable<__type197>::type __type198;
      typedef __type198 __type199;
      typedef decltype(std::declval<__type148>()[std::declval<__type199>()]) __type200;
      typedef typename pythonic::assignable<__type200>::type __type201;
      typedef typename __combined<__type118,__type122,__type137,__type122,__type201>::type __type202;
      typedef __type202 __type203;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type117>(), std::declval<__type203>())) __type204;
      typedef decltype(std::declval<__type39>()(std::declval<__type204>())) __type205;
      typedef container<typename std::remove_reference<__type205>::type> __type206;
      typedef typename __combined<__type38,__type206,__type19,__type206>::type __type207;
      typedef __type207 __type208;
      typedef pythonic::types::slice __type209;
      typedef decltype(std::declval<__type208>()[std::declval<__type209>()]) __type210;
      typedef typename pythonic::assignable<__type210>::type __type211;
      typedef __type211 __type212;
      typedef decltype(std::declval<__type212>()[std::declval<__type18>()]) __type214;
      typedef typename __combined<__type29,__type19>::type __type217;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type86>(), std::declval<__type196>())) __type220;
      typedef decltype(std::declval<__type39>()(std::declval<__type220>())) __type221;
      typedef container<typename std::remove_reference<__type221>::type> __type222;
      typedef typename __combined<__type217,__type222,__type19,__type222>::type __type223;
      typedef __type223 __type224;
      typedef decltype(std::declval<__type224>()[std::declval<__type209>()]) __type225;
      typedef typename pythonic::assignable<__type225>::type __type226;
      typedef __type226 __type227;
      typedef decltype(std::declval<__type227>()[std::declval<__type18>()]) __type229;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type230;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::array{})>::type>::type __type232;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type233;
      typedef __type233 __type234;
      typedef decltype(std::declval<__type232>()(std::declval<__type234>())) __type235;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type235>())) __type236;
      typedef decltype(std::declval<__type230>()(std::declval<__type9>(), std::declval<__type236>())) __type237;
      typedef typename pythonic::assignable<__type237>::type __type238;
      typedef indexable<__type44> __type239;
      typedef typename __combined<__type238,__type239>::type __type240;
      typedef std::integral_constant<long,0> __type241;
      typedef indexable_container<__type241, typename std::remove_reference<__type234>::type> __type243;
      typedef typename __combined<__type240,__type243,__type239,__type243>::type __type244;
      typedef __type244 __type245;
      typedef decltype(std::declval<__type245>()[std::declval<__type18>()]) __type247;
      typedef decltype(std::declval<__type22>()(std::declval<__type214>(), std::declval<__type229>(), std::declval<__type247>())) __type248;
      typedef decltype(std::declval<__type21>()(std::declval<__type248>())) __type249;
      typedef container<typename std::remove_reference<__type249>::type> __type250;
      typedef typename __combined<__type20,__type250,__type19>::type __type251;
      typedef __type251 __type252;
      typedef typename pythonic::returnable<__type252>::type __type253;
      typedef __type2 __ptype2;
      typedef __type5 __ptype3;
      typedef __type253 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    inline
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& z, argument_type1&& p, argument_type2&& k, argument_type3&& n_sections) const
    ;
  }  ;
  struct zpk2sos_multiple
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef __type0 __type1;
      typedef __type1 __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type3;
      typedef __type3 __type4;
      typedef __type4 __type5;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type6;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type7;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type8;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type9;
      typedef __type9 __type10;
      typedef decltype(std::declval<__type8>()(std::declval<__type10>())) __type11;
      typedef typename pythonic::assignable<__type11>::type __type12;
      typedef __type12 __type13;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::max{})>::type>::type __type14;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::concatenate{})>::type>::type __type15;
      typedef typename pythonic::assignable<__type4>::type __type16;
      typedef __type16 __type17;
      typedef typename pythonic::assignable<__type1>::type __type18;
      typedef __type18 __type19;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type19>())) __type20;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type20>::type>::type __type21;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type17>())) __type23;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type23>::type>::type __type24;
      typedef decltype(pythonic::operator_::sub(std::declval<__type21>(), std::declval<__type24>())) __type25;
      typedef long __type26;
      typedef typename __combined<__type25,__type26>::type __type27;
      typedef decltype(std::declval<__type14>()(std::declval<__type27>(), std::declval<__type26>())) __type28;
      typedef decltype(std::declval<__type7>()(std::declval<__type28>(), std::declval<__type13>())) __type30;
      typedef decltype(std::declval<__type6>()(std::declval<__type30>())) __type31;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type17>(), std::declval<__type31>())) __type32;
      typedef decltype(std::declval<__type15>()(std::declval<__type32>(), std::declval<__type26>())) __type33;
      typedef typename pythonic::assignable<__type33>::type __type34;
      typedef __type34 __type35;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type35>())) __type36;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type36>::type>::type __type37;
      typedef decltype(pythonic::operator_::sub(std::declval<__type37>(), std::declval<__type21>())) __type45;
      typedef typename __combined<__type45,__type26>::type __type46;
      typedef decltype(std::declval<__type14>()(std::declval<__type46>(), std::declval<__type26>())) __type47;
      typedef decltype(std::declval<__type7>()(std::declval<__type47>(), std::declval<__type13>())) __type49;
      typedef decltype(std::declval<__type6>()(std::declval<__type49>())) __type50;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type19>(), std::declval<__type50>())) __type51;
      typedef decltype(std::declval<__type15>()(std::declval<__type51>(), std::declval<__type26>())) __type52;
      typedef typename pythonic::assignable<__type52>::type __type53;
      typedef __type53 __type54;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type54>())) __type55;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type55>::type>::type __type56;
      typedef typename __combined<__type37,__type56>::type __type57;
      typedef decltype(std::declval<__type14>()(std::declval<__type57>(), std::declval<__type56>())) __type58;
      typedef decltype(pythonic::operator_::add(std::declval<__type58>(), std::declval<__type26>())) __type59;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type59>(), std::declval<__type26>())) __type60;
      typedef typename pythonic::assignable<__type60>::type __type61;
      typedef __type61 __type62;
      typedef std::integral_constant<long, 6> __type63;
      typedef decltype(std::declval<__type7>()(std::declval<__type13>(), std::declval<__type62>(), std::declval<__type63>())) __type64;
      typedef decltype(std::declval<__type6>()(std::declval<__type64>())) __type65;
      typedef typename pythonic::assignable<__type65>::type __type66;
      typedef zpk2sos __type67;
      typedef pythonic::types::contiguous_slice __type69;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type70;
      typedef decltype(std::declval<__type70>()(std::declval<__type13>())) __type72;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type72>::type::iterator>::value_type>::type __type73;
      typedef __type73 __type74;
      typedef decltype(std::declval<__type54>()(std::declval<__type69>(), std::declval<__type74>())) __type75;
      typedef decltype(std::declval<__type35>()(std::declval<__type69>(), std::declval<__type74>())) __type78;
      typedef decltype(std::declval<__type10>()[std::declval<__type74>()]) __type81;
      typedef decltype(std::declval<__type67>()(std::declval<__type75>(), std::declval<__type78>(), std::declval<__type81>(), std::declval<__type62>())) __type83;
      typedef container<typename std::remove_reference<__type83>::type> __type84;
      typedef typename __combined<__type66,__type84>::type __type85;
      typedef __type85 __type86;
      typedef typename pythonic::returnable<__type86>::type __type87;
      typedef __type2 __ptype8;
      typedef __type5 __ptype9;
      typedef __type87 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& z, argument_type1&& p, argument_type2&& k) const
    ;
  }  ;
  template <typename argument_type0 >
  inline
  typename poly::type<argument_type0>::result_type poly::operator()(argument_type0&& zeros) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type1;
    typedef std::integral_constant<long, 1> __type2;
    typedef decltype(std::declval<__type1>()(std::declval<__type2>())) __type3;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type4;
    typedef __type4 __type5;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type5>())) __type6;
    typedef typename pythonic::assignable<__type6>::type __type7;
    typedef __type7 __type8;
    typedef decltype(std::declval<__type0>()(std::declval<__type3>(), std::declval<__type8>())) __type9;
    typedef typename pythonic::lazy<__type9>::type __type10;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::convolve{})>::type>::type __type11;
    typedef __type10 __type12;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::array{})>::type>::type __type13;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::static_list{})>::type>::type __type14;
    typedef long __type15;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type17;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type18;
    typedef decltype(std::declval<__type18>()(std::declval<__type5>())) __type20;
    typedef decltype(std::declval<__type17>()(std::declval<__type20>())) __type21;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type21>::type::iterator>::value_type>::type __type22;
    typedef __type22 __type23;
    typedef decltype(std::declval<__type5>()[std::declval<__type23>()]) __type24;
    typedef decltype(pythonic::operator_::neg(std::declval<__type24>())) __type25;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type15>(), std::declval<__type25>())) __type26;
    typedef decltype(std::declval<__type14>()(std::declval<__type26>())) __type27;
    typedef decltype(std::declval<__type13>()(std::declval<__type27>(), std::declval<__type8>())) __type29;
    typedef pythonic::types::str __type30;
    typedef decltype(std::declval<__type11>()(std::declval<__type12>(), std::declval<__type29>(), std::declval<__type30>())) __type31;
    typedef typename pythonic::lazy<__type31>::type __type32;
    typedef typename __combined<__type10,__type32>::type __type33;
    typedef typename pythonic::lazy<__type33>::type __type34;
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, zeros))>::type dt = pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, zeros);
    __type34 a = pythonic::numpy::functor::ones{}(pythonic::builtins::pythran::functor::make_shape{}(std::integral_constant<long, 1>{}), dt);
    {
      long  __target139890632274768 = pythonic::builtins::functor::len{}(zeros);
      for (long  k=0L; k < __target139890632274768; k += 1L)
      {
        a = pythonic::numpy::functor::convolve{}(a, pythonic::numpy::functor::array{}(pythonic::builtins::pythran::functor::static_list{}(pythonic::types::make_tuple(1L, pythonic::operator_::neg(zeros.fast(k)))), dt), pythonic::types::str("full"));
      }
    }
    return a;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename _nearest_real_complex_idx::type<argument_type0, argument_type1, argument_type2>::result_type _nearest_real_complex_idx::operator()(argument_type0&& fro, argument_type1&& to, argument_type2&& which) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::isreal{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
    typedef __type1 __type2;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::argsort{})>::type>::type __type3;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::abs{})>::type>::type __type4;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type6;
    typedef __type6 __type7;
    typedef decltype(pythonic::operator_::sub(std::declval<__type2>(), std::declval<__type7>())) __type8;
    typedef decltype(std::declval<__type4>()(std::declval<__type8>())) __type9;
    typedef decltype(std::declval<__type3>()(std::declval<__type9>())) __type10;
    typedef typename pythonic::assignable<__type10>::type __type11;
    typedef __type11 __type12;
    typedef decltype(std::declval<__type2>()[std::declval<__type12>()]) __type13;
    typedef decltype(std::declval<__type0>()(std::declval<__type13>())) __type14;
    typedef typename pythonic::lazy<__type14>::type __type15;
    typedef __type15 __type16;
    typedef decltype(pythonic::operator_::invert(std::declval<__type16>())) __type17;
    typedef typename pythonic::lazy<__type17>::type __type18;
    typedef typename __combined<__type15,__type18>::type __type19;
    typedef typename pythonic::lazy<__type19>::type __type20;
    typename pythonic::assignable_noescape<decltype(pythonic::numpy::functor::argsort{}(pythonic::numpy::functor::abs{}(pythonic::operator_::sub(fro, to))))>::type order = pythonic::numpy::functor::argsort{}(pythonic::numpy::functor::abs{}(pythonic::operator_::sub(fro, to)));
    __type20 mask = pythonic::numpy::functor::isreal{}(fro.fast(order));
    if (pythonic::operator_::eq(which, pythonic::types::str("complex")))
    {
      mask = pythonic::operator_::invert(mask);
    }
    return order[std::get<0>(std::get<0>(pythonic::numpy::functor::nonzero{}(mask)))];
  }
  template <typename argument_type0 >
  inline
  typename _cplxreal::type<argument_type0>::result_type _cplxreal::operator()(argument_type0&& z) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
    typedef __type0 __type1;
    typedef typename pythonic::assignable<__type1>::type __type2;
    typedef __type2 __type3;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::lexsort{})>::type>::type __type4;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::abs{})>::type>::type __type5;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type3>())) __type7;
    typedef decltype(std::declval<__type5>()(std::declval<__type7>())) __type8;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, std::declval<__type3>())) __type10;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type8>(), std::declval<__type10>())) __type11;
    typedef decltype(std::declval<__type4>()(std::declval<__type11>())) __type12;
    typedef decltype(std::declval<__type3>()[std::declval<__type12>()]) __type13;
    typedef container<typename std::remove_reference<__type13>::type> __type14;
    typedef typename __combined<__type0,__type14>::type __type15;
    typedef typename pythonic::assignable<__type13>::type __type16;
    typedef __type16 __type17;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type17>())) __type19;
    typedef decltype(std::declval<__type5>()(std::declval<__type19>())) __type20;
    typedef long __type21;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::finfo{})>::type>::type __type22;
    typedef double __type23;
    typedef decltype(pythonic::operator_::mul(std::declval<__type23>(), std::declval<__type3>())) __type25;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type25>())) __type26;
    typedef decltype(std::declval<__type22>()(std::declval<__type26>())) __type27;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::EPS{}, std::declval<__type27>())) __type28;
    typedef decltype(pythonic::operator_::mul(std::declval<__type21>(), std::declval<__type28>())) __type29;
    typedef typename pythonic::assignable<__type29>::type __type30;
    typedef __type30 __type31;
    typedef decltype(std::declval<__type5>()(std::declval<__type17>())) __type33;
    typedef decltype(pythonic::operator_::mul(std::declval<__type31>(), std::declval<__type33>())) __type34;
    typedef decltype(pythonic::operator_::le(std::declval<__type20>(), std::declval<__type34>())) __type35;
    typedef typename pythonic::assignable<__type35>::type __type36;
    typedef __type36 __type37;
    typedef decltype(pythonic::operator_::invert(std::declval<__type37>())) __type38;
    typedef decltype(std::declval<__type17>()[std::declval<__type38>()]) __type39;
    typedef typename pythonic::assignable<__type39>::type __type40;
    typedef __type40 __type41;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type41>())) __type43;
    typedef decltype(pythonic::operator_::gt(std::declval<__type43>(), std::declval<__type21>())) __type44;
    typedef decltype(std::declval<__type41>()[std::declval<__type44>()]) __type45;
    typedef container<typename std::remove_reference<__type45>::type> __type46;
    typedef typename __combined<__type40,__type46>::type __type47;
    typedef __type47 __type48;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type48>())) __type50;
    typedef decltype(pythonic::operator_::lt(std::declval<__type50>(), std::declval<__type21>())) __type51;
    typedef decltype(std::declval<__type48>()[std::declval<__type51>()]) __type52;
    typedef container<typename std::remove_reference<__type52>::type> __type53;
    typedef typename __combined<__type40,__type46,__type53>::type __type54;
    typedef typename pythonic::assignable<__type54>::type __type55;
    typedef pythonic::types::list<typename std::remove_reference<__type21>::type> __type56;
    typedef typename pythonic::assignable<__type56>::type __type57;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::nonzero{})>::type>::type __type58;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::diff{})>::type>::type __type59;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::concatenate{})>::type>::type __type60;
    typedef typename pythonic::assignable<__type45>::type __type61;
    typedef __type61 __type62;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, std::declval<__type62>())) __type63;
    typedef decltype(std::declval<__type59>()(std::declval<__type63>())) __type64;
    typedef pythonic::types::contiguous_slice __type67;
    typedef decltype(std::declval<__type62>()[std::declval<__type67>()]) __type68;
    typedef decltype(std::declval<__type5>()(std::declval<__type68>())) __type69;
    typedef decltype(pythonic::operator_::mul(std::declval<__type31>(), std::declval<__type69>())) __type70;
    typedef decltype(pythonic::operator_::le(std::declval<__type64>(), std::declval<__type70>())) __type71;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type56>(), std::declval<__type71>(), std::declval<__type56>())) __type72;
    typedef decltype(std::declval<__type60>()(std::declval<__type72>())) __type73;
    typedef decltype(std::declval<__type59>()(std::declval<__type73>())) __type74;
    typedef typename pythonic::assignable<__type74>::type __type75;
    typedef __type75 __type76;
    typedef decltype(pythonic::operator_::gt(std::declval<__type76>(), std::declval<__type21>())) __type77;
    typedef decltype(std::declval<__type58>()(std::declval<__type77>())) __type78;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type78>::type>::type __type79;
    typedef typename pythonic::assignable<__type79>::type __type80;
    typedef __type80 __type81;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type82;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type83;
    typedef decltype(std::declval<__type83>()(std::declval<__type81>())) __type85;
    typedef decltype(std::declval<__type82>()(std::declval<__type85>())) __type86;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type86>::type::iterator>::value_type>::type __type87;
    typedef __type87 __type88;
    typedef decltype(std::declval<__type81>()[std::declval<__type88>()]) __type89;
    typedef container<typename std::remove_reference<__type89>::type> __type90;
    typedef typename __combined<__type80,__type90>::type __type91;
    typedef typename pythonic::assignable<__type91>::type __type92;
    typedef typename pythonic::assignable<__type68>::type __type95;
    typedef __type95 __type96;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::static_list{})>::type>::type __type97;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type96>())) __type99;
    typedef decltype(std::declval<__type5>()(std::declval<__type99>())) __type100;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type100>())) __type101;
    typedef decltype(std::declval<__type97>()(std::declval<__type101>())) __type102;
    typedef decltype(std::declval<__type4>()(std::declval<__type102>())) __type103;
    typedef decltype(std::declval<__type96>()[std::declval<__type103>()]) __type104;
    typedef typename __combined<__type95,__type104>::type __type105;
    typedef typename pythonic::assignable<__type105>::type __type106;
    typedef typename pythonic::assignable<__type52>::type __type107;
    typedef __type107 __type108;
    typedef decltype(std::declval<__type108>()[std::declval<__type67>()]) __type109;
    typedef typename pythonic::assignable<__type109>::type __type110;
    typedef __type110 __type111;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, std::declval<__type111>())) __type113;
    typedef decltype(std::declval<__type5>()(std::declval<__type113>())) __type114;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type114>())) __type115;
    typedef decltype(std::declval<__type97>()(std::declval<__type115>())) __type116;
    typedef decltype(std::declval<__type4>()(std::declval<__type116>())) __type117;
    typedef decltype(std::declval<__type111>()[std::declval<__type117>()]) __type118;
    typedef typename __combined<__type110,__type118>::type __type119;
    typedef typename pythonic::assignable<__type119>::type __type120;
    typename pythonic::assignable_noescape<decltype(z)>::type z_ = z;
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::mul(100L, pythonic::builtins::getattr(pythonic::types::attr::EPS{}, pythonic::numpy::functor::finfo{}(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, pythonic::operator_::mul(1.0, z_))))))>::type tol = pythonic::operator_::mul(100L, pythonic::builtins::getattr(pythonic::types::attr::EPS{}, pythonic::numpy::functor::finfo{}(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, pythonic::operator_::mul(1.0, z_)))));
    typename pythonic::assignable_noescape<decltype(z_[pythonic::numpy::functor::lexsort{}(pythonic::types::make_tuple(pythonic::builtins::functor::abs{}(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z_)), pythonic::builtins::getattr(pythonic::types::attr::REAL{}, z_)))])>::type z__ = z_[pythonic::numpy::functor::lexsort{}(pythonic::types::make_tuple(pythonic::builtins::functor::abs{}(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z_)), pythonic::builtins::getattr(pythonic::types::attr::REAL{}, z_)))];
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::le(pythonic::builtins::functor::abs{}(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z__)), pythonic::operator_::mul(tol, pythonic::builtins::functor::abs{}(z__))))>::type real_indices = pythonic::operator_::le(pythonic::builtins::functor::abs{}(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z__)), pythonic::operator_::mul(tol, pythonic::builtins::functor::abs{}(z__)));
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, z__[real_indices]))>::type zr = pythonic::builtins::getattr(pythonic::types::attr::REAL{}, z__[real_indices]);
    if (pythonic::operator_::eq(pythonic::builtins::functor::len{}(zr), pythonic::builtins::functor::len{}(z__)))
    {
      return pythonic::types::make_tuple(pythonic::numpy::functor::empty{}(pythonic::builtins::pythran::functor::make_shape{}(std::integral_constant<long, 0>{}), pythonic::numpy::functor::float64{}), zr);
    }
    else
    {
      __type55 z___ = z__[pythonic::operator_::invert(real_indices)];
      typename pythonic::assignable_noescape<decltype(z___.fast(pythonic::operator_::gt(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z___), 0L)))>::type zp = z___.fast(pythonic::operator_::gt(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z___), 0L));
      typename pythonic::assignable_noescape<decltype(z___.fast(pythonic::operator_::lt(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z___), 0L)))>::type zn = z___.fast(pythonic::operator_::lt(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, z___), 0L));
      if (pythonic::operator_::ne(pythonic::builtins::functor::len{}(zp), pythonic::builtins::functor::len{}(zn)))
      {
        throw pythonic::builtins::functor::ValueError{}(pythonic::types::str("Array contains complex value without conjugate"));
      }
      typename pythonic::assignable_noescape<decltype(pythonic::numpy::functor::diff{}(pythonic::numpy::functor::concatenate{}(pythonic::types::make_tuple(__type57(0L, pythonic::types::single_value()), pythonic::operator_::le(pythonic::numpy::functor::diff{}(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, zp)), pythonic::operator_::mul(tol, pythonic::builtins::functor::abs{}(zp[pythonic::types::contiguous_slice(pythonic::builtins::None,-1L)]))), __type57(0L, pythonic::types::single_value())))))>::type diffs = pythonic::numpy::functor::diff{}(pythonic::numpy::functor::concatenate{}(pythonic::types::make_tuple(__type57(0L, pythonic::types::single_value()), pythonic::operator_::le(pythonic::numpy::functor::diff{}(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, zp)), pythonic::operator_::mul(tol, pythonic::builtins::functor::abs{}(zp[pythonic::types::contiguous_slice(pythonic::builtins::None,-1L)]))), __type57(0L, pythonic::types::single_value()))));
      __type92 run_starts = std::get<0>(pythonic::numpy::functor::nonzero{}(pythonic::operator_::gt(diffs, 0L)));
      typename pythonic::assignable_noescape<decltype(std::get<0>(pythonic::numpy::functor::nonzero{}(pythonic::operator_::lt(diffs, 0L))))>::type run_stops = std::get<0>(pythonic::numpy::functor::nonzero{}(pythonic::operator_::lt(diffs, 0L)));
      {
        long  __target139890632268304 = pythonic::builtins::functor::len{}(run_starts);
        for (long  i=0L; i < __target139890632268304; i += 1L)
        {
          typename pythonic::assignable_noescape<decltype(run_starts.fast(i))>::type start = run_starts.fast(i);
          typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(run_stops.fast(i), 1L))>::type stop = pythonic::operator_::add(run_stops.fast(i), 1L);
          __type106 chunk = zp[pythonic::types::contiguous_slice(start,stop)];
          chunk[pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None)] = chunk[pythonic::numpy::functor::lexsort{}(pythonic::builtins::pythran::functor::static_list{}(pythonic::types::make_tuple(pythonic::builtins::functor::abs{}(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, chunk)))))];
          __type120 chunk_ = zn[pythonic::types::contiguous_slice(start,stop)];
          chunk_[pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None)] = chunk_[pythonic::numpy::functor::lexsort{}(pythonic::builtins::pythran::functor::static_list{}(pythonic::types::make_tuple(pythonic::builtins::functor::abs{}(pythonic::builtins::getattr(pythonic::types::attr::IMAG{}, chunk_)))))];
        }
      }
      return pythonic::types::make_tuple(pythonic::operator_::div(pythonic::operator_::add(zp, pythonic::numpy::functor::conj{}(zn)), 2L), zr);
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename zpk2tf::type<argument_type0, argument_type1, argument_type2>::result_type zpk2tf::operator()(argument_type0&& z, argument_type1&& p, argument_type2&& k) const
  {
    return pythonic::types::make_tuple(pythonic::builtins::getattr(pythonic::types::attr::REAL{}, pythonic::operator_::mul(k, poly()(z))), pythonic::builtins::getattr(pythonic::types::attr::REAL{}, poly()(p)));
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  inline
  typename zpk2sos::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type zpk2sos::operator()(argument_type0&& z, argument_type1&& p, argument_type2&& k, argument_type3&& n_sections) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
    typedef __type0 __type1;
    typedef typename pythonic::lazy<__type1>::type __type2;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::append{})>::type>::type __type3;
    typedef __type2 __type4;
    typedef long __type5;
    typedef decltype(std::declval<__type3>()(std::declval<__type4>(), std::declval<__type5>())) __type6;
    typedef typename pythonic::lazy<__type6>::type __type7;
    typedef typename __combined<__type2,__type7>::type __type8;
    typedef __type8 __type9;
    typedef typename _cplxreal::type<__type9>::__ptype0 __type10;
    typedef typename __combined<__type7,__type10>::type __type11;
    typedef typename __combined<__type9,__type10>::type __type12;
    typedef typename _cplxreal::type<__type12>::__ptype1 __type13;
    typedef container<typename std::remove_reference<__type13>::type> __type14;
    typedef typename __combined<__type11,__type14>::type __type15;
    typedef typename __combined<__type12,__type14>::type __type16;
    typedef typename __combined<__type2,__type15,__type16>::type __type17;
    typedef typename pythonic::lazy<__type17>::type __type18;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type19;
    typedef __type19 __type20;
    typedef typename pythonic::assignable<__type20>::type __type21;
    typedef __type21 __type22;
    typedef decltype(std::declval<__type3>()(std::declval<__type22>(), std::declval<__type5>())) __type23;
    typedef typename pythonic::assignable<__type23>::type __type24;
    typedef typename __combined<__type21,__type24>::type __type25;
    typedef __type25 __type26;
    typedef typename _cplxreal::type<__type26>::__ptype0 __type27;
    typedef typename __combined<__type24,__type27>::type __type28;
    typedef typename __combined<__type26,__type27>::type __type29;
    typedef typename _cplxreal::type<__type29>::__ptype1 __type30;
    typedef container<typename std::remove_reference<__type30>::type> __type31;
    typedef typename __combined<__type28,__type31>::type __type32;
    typedef typename __combined<__type29,__type31>::type __type33;
    typedef typename __combined<__type21,__type32,__type33>::type __type34;
    typedef typename pythonic::assignable<__type34>::type __type35;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type36;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type37;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type38;
    typedef __type38 __type39;
    typedef std::integral_constant<long, 6> __type40;
    typedef decltype(std::declval<__type37>()(std::declval<__type39>(), std::declval<__type40>())) __type41;
    typedef decltype(std::declval<__type36>()(std::declval<__type41>())) __type42;
    typedef typename pythonic::assignable<__type42>::type __type43;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type44;
    typedef decltype(std::declval<__type44>()(std::declval<__type39>())) __type46;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type46>::type::iterator>::value_type>::type __type47;
    typedef __type47 __type48;
    typedef indexable<__type48> __type49;
    typedef typename __combined<__type43,__type49>::type __type50;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::concatenate{})>::type>::type __type51;
    typedef zpk2tf __type52;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros_like{})>::type>::type __type53;
    typedef std::integral_constant<long, 2> __type55;
    typedef decltype(std::declval<__type37>()(std::declval<__type39>(), std::declval<__type55>())) __type56;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::complex128{})>::type>::type __type57;
    typedef decltype(std::declval<__type36>()(std::declval<__type56>(), std::declval<__type57>())) __type58;
    typedef typename pythonic::assignable<__type58>::type __type59;
    typedef typename __combined<__type59,__type49>::type __type65;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::static_list{})>::type>::type __type66;
    typedef _cplxreal __type67;
    typedef decltype(std::declval<__type67>()(std::declval<__type33>())) __type68;
    typedef decltype(std::declval<__type51>()(std::declval<__type68>())) __type69;
    typedef typename pythonic::assignable<__type69>::type __type70;
    typedef __type70 __type71;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::argmin{})>::type>::type __type72;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::abs{})>::type>::type __type73;
    typedef decltype(std::declval<__type73>()(std::declval<__type71>())) __type75;
    typedef decltype(pythonic::operator_::sub(std::declval<__type5>(), std::declval<__type75>())) __type76;
    typedef decltype(std::declval<__type73>()(std::declval<__type76>())) __type77;
    typedef decltype(std::declval<__type72>()(std::declval<__type77>())) __type78;
    typedef typename pythonic::assignable<__type78>::type __type79;
    typedef __type79 __type80;
    typedef decltype(std::declval<__type71>()[std::declval<__type80>()]) __type81;
    typedef container<typename std::remove_reference<__type81>::type> __type82;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::delete_{})>::type>::type __type83;
    typedef typename __combined<__type70,__type82,__type82>::type __type84;
    typedef __type84 __type85;
    typedef decltype(std::declval<__type83>()(std::declval<__type85>(), std::declval<__type80>())) __type87;
    typedef typename pythonic::assignable<__type87>::type __type88;
    typedef typename __combined<__type70,__type82,__type82,__type88>::type __type89;
    typedef __type89 __type90;
    typedef _nearest_real_complex_idx __type91;
    typedef decltype(std::declval<__type67>()(std::declval<__type16>())) __type93;
    typedef decltype(std::declval<__type51>()(std::declval<__type93>())) __type94;
    typedef typename pythonic::assignable<__type94>::type __type95;
    typedef __type95 __type96;
    typedef typename pythonic::assignable<__type81>::type __type98;
    typedef __type98 __type99;
    typedef pythonic::types::str __type100;
    typedef decltype(std::declval<__type91>()(std::declval<__type96>(), std::declval<__type99>(), std::declval<__type100>())) __type101;
    typedef typename pythonic::assignable<__type101>::type __type102;
    typedef __type102 __type103;
    typedef decltype(std::declval<__type96>()[std::declval<__type103>()]) __type104;
    typedef container<typename std::remove_reference<__type104>::type> __type105;
    typedef typename __combined<__type95,__type105,__type105,__type105,__type105>::type __type106;
    typedef __type106 __type107;
    typedef decltype(std::declval<__type83>()(std::declval<__type107>(), std::declval<__type103>())) __type109;
    typedef typename pythonic::assignable<__type109>::type __type110;
    typedef typename __combined<__type95,__type105,__type105,__type105,__type105,__type110>::type __type111;
    typedef __type111 __type112;
    typedef decltype(std::declval<__type91>()(std::declval<__type112>(), std::declval<__type99>(), std::declval<__type100>())) __type115;
    typedef typename pythonic::assignable<__type115>::type __type116;
    typedef decltype(pythonic::operator_::sub(std::declval<__type99>(), std::declval<__type112>())) __type119;
    typedef decltype(std::declval<__type73>()(std::declval<__type119>())) __type120;
    typedef decltype(std::declval<__type72>()(std::declval<__type120>())) __type121;
    typedef typename pythonic::assignable<__type121>::type __type122;
    typedef typename __combined<__type116,__type122>::type __type123;
    typedef __type123 __type124;
    typedef decltype(std::declval<__type112>()[std::declval<__type124>()]) __type125;
    typedef container<typename std::remove_reference<__type125>::type> __type126;
    typedef typename __combined<__type95,__type105,__type105,__type105,__type105,__type110,__type126,__type126,__type126,__type126>::type __type127;
    typedef __type127 __type128;
    typedef decltype(std::declval<__type83>()(std::declval<__type128>(), std::declval<__type124>())) __type130;
    typedef typename pythonic::assignable<__type130>::type __type131;
    typedef typename __combined<__type95,__type105,__type105,__type105,__type105,__type110,__type126,__type126,__type126,__type126,__type131>::type __type132;
    typedef __type132 __type133;
    typedef decltype(std::declval<__type91>()(std::declval<__type133>(), std::declval<__type99>(), std::declval<__type100>())) __type136;
    typedef typename pythonic::assignable<__type136>::type __type137;
    typedef __type137 __type138;
    typedef decltype(std::declval<__type133>()[std::declval<__type138>()]) __type139;
    typedef container<typename std::remove_reference<__type139>::type> __type140;
    typedef typename __combined<__type95,__type105,__type105,__type105,__type105,__type110,__type126,__type126,__type126,__type126,__type131,__type140>::type __type141;
    typedef __type141 __type142;
    typedef decltype(std::declval<__type83>()(std::declval<__type142>(), std::declval<__type138>())) __type144;
    typedef typename pythonic::assignable<__type144>::type __type145;
    typedef typename __combined<__type95,__type105,__type105,__type105,__type105,__type110,__type126,__type126,__type126,__type126,__type131,__type140,__type145>::type __type146;
    typedef __type146 __type147;
    typedef typename pythonic::assignable<__type5>::type __type149;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type __type150;
    typedef decltype(std::declval<__type150>()(std::declval<__type99>())) __type152;
    typedef typename pythonic::assignable<__type152>::type __type153;
    typedef typename pythonic::assignable<__type104>::type __type157;
    typedef typename pythonic::assignable<__type125>::type __type158;
    typedef typename __combined<__type157,__type158>::type __type159;
    typedef __type159 __type160;
    typedef decltype(std::declval<__type91>()(std::declval<__type90>(), std::declval<__type160>(), std::declval<__type100>())) __type161;
    typedef typename pythonic::assignable<__type161>::type __type162;
    typedef __type162 __type163;
    typedef decltype(std::declval<__type90>()[std::declval<__type163>()]) __type164;
    typedef typename pythonic::assignable<__type164>::type __type165;
    typedef container<typename std::remove_reference<__type164>::type> __type166;
    typedef typename __combined<__type70,__type82,__type82,__type88,__type166>::type __type167;
    typedef __type167 __type168;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::nonzero{})>::type>::type __type169;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::isreal{})>::type>::type __type170;
    typedef decltype(std::declval<__type170>()(std::declval<__type168>())) __type172;
    typedef decltype(std::declval<__type169>()(std::declval<__type172>())) __type173;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type173>::type>::type __type174;
    typedef typename pythonic::assignable<__type174>::type __type175;
    typedef __type175 __type176;
    typedef decltype(std::declval<__type168>()[std::declval<__type176>()]) __type179;
    typedef decltype(std::declval<__type73>()(std::declval<__type179>())) __type180;
    typedef decltype(pythonic::operator_::sub(std::declval<__type180>(), std::declval<__type5>())) __type181;
    typedef decltype(std::declval<__type73>()(std::declval<__type181>())) __type182;
    typedef decltype(std::declval<__type72>()(std::declval<__type182>())) __type183;
    typedef decltype(std::declval<__type176>()[std::declval<__type183>()]) __type184;
    typedef container<typename std::remove_reference<__type184>::type> __type185;
    typedef typename __combined<__type175,__type185>::type __type186;
    typedef typename pythonic::assignable<__type184>::type __type187;
    typedef typename __combined<__type162,__type187>::type __type188;
    typedef __type188 __type189;
    typedef decltype(std::declval<__type168>()[std::declval<__type189>()]) __type190;
    typedef container<typename std::remove_reference<__type190>::type> __type191;
    typedef typename __combined<__type70,__type82,__type82,__type88,__type166,__type191>::type __type192;
    typedef __type192 __type193;
    typedef decltype(std::declval<__type83>()(std::declval<__type193>(), std::declval<__type189>())) __type195;
    typedef typename pythonic::assignable<__type195>::type __type196;
    typedef typename __combined<__type70,__type82,__type88,__type166,__type191,__type196>::type __type197;
    typedef typename pythonic::assignable<__type190>::type __type198;
    typedef typename __combined<__type149,__type153,__type153,__type165,__type198>::type __type199;
    typedef __type199 __type200;
    typedef decltype(std::declval<__type91>()(std::declval<__type147>(), std::declval<__type200>(), std::declval<__type100>())) __type201;
    typedef typename pythonic::assignable<__type201>::type __type202;
    typedef __type202 __type203;
    typedef decltype(std::declval<__type147>()[std::declval<__type203>()]) __type204;
    typedef container<typename std::remove_reference<__type204>::type> __type205;
    typedef typename __combined<__type95,__type105,__type105,__type105,__type105,__type110,__type126,__type126,__type126,__type126,__type131,__type140,__type145,__type205>::type __type206;
    typedef __type206 __type207;
    typedef decltype(std::declval<__type83>()(std::declval<__type207>(), std::declval<__type203>())) __type209;
    typedef typename pythonic::assignable<__type209>::type __type210;
    typedef typename __combined<__type95,__type105,__type110,__type126,__type131,__type140,__type145,__type205,__type210>::type __type211;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type99>(), std::declval<__type200>())) __type214;
    typedef decltype(std::declval<__type66>()(std::declval<__type214>())) __type215;
    typedef container<typename std::remove_reference<__type215>::type> __type216;
    typedef typename __combined<__type65,__type216,__type49,__type216>::type __type217;
    typedef __type217 __type218;
    typedef pythonic::types::slice __type219;
    typedef decltype(std::declval<__type218>()[std::declval<__type219>()]) __type220;
    typedef typename __combined<__type65,__type216,__type49,__type220>::type __type221;
    typedef __type221 __type222;
    typedef decltype(std::declval<__type53>()(std::declval<__type222>())) __type223;
    typedef typename pythonic::assignable<__type223>::type __type224;
    typedef typename __combined<__type224,__type49>::type __type227;
    typedef decltype(std::declval<__type150>()(std::declval<__type160>())) __type230;
    typedef typename pythonic::assignable<__type230>::type __type231;
    typedef typename pythonic::assignable<__type139>::type __type232;
    typedef typename pythonic::assignable<__type204>::type __type236;
    typedef typename __combined<__type149,__type231,__type232,__type231,__type236>::type __type237;
    typedef __type237 __type238;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type160>(), std::declval<__type238>())) __type239;
    typedef decltype(std::declval<__type66>()(std::declval<__type239>())) __type240;
    typedef container<typename std::remove_reference<__type240>::type> __type241;
    typedef typename __combined<__type227,__type241,__type49,__type241>::type __type242;
    typedef __type242 __type243;
    typedef decltype(std::declval<__type243>()[std::declval<__type219>()]) __type244;
    typedef typename __combined<__type227,__type241,__type49,__type244>::type __type245;
    typedef typename pythonic::assignable<__type244>::type __type246;
    typedef __type246 __type247;
    typedef decltype(std::declval<__type247>()[std::declval<__type48>()]) __type249;
    typedef typename pythonic::assignable<__type220>::type __type250;
    typedef __type250 __type251;
    typedef decltype(std::declval<__type251>()[std::declval<__type48>()]) __type253;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type254;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::array{})>::type>::type __type256;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type257;
    typedef __type257 __type258;
    typedef decltype(std::declval<__type256>()(std::declval<__type258>())) __type259;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type259>())) __type260;
    typedef decltype(std::declval<__type254>()(std::declval<__type39>(), std::declval<__type260>())) __type261;
    typedef typename pythonic::assignable<__type261>::type __type262;
    typedef indexable<__type5> __type263;
    typedef typename __combined<__type262,__type263>::type __type264;
    typedef std::integral_constant<long,0> __type265;
    typedef indexable_container<__type265, typename std::remove_reference<__type258>::type> __type267;
    typedef typename __combined<__type264,__type267,__type263>::type __type268;
    typedef __type268 __type269;
    typedef decltype(std::declval<__type269>()[std::declval<__type48>()]) __type271;
    typedef decltype(std::declval<__type52>()(std::declval<__type249>(), std::declval<__type253>(), std::declval<__type271>())) __type272;
    typedef decltype(std::declval<__type51>()(std::declval<__type272>())) __type273;
    typedef container<typename std::remove_reference<__type273>::type> __type274;
    typedef typename __combined<__type50,__type274,__type49>::type __type275;
    typedef typename pythonic::assignable<__type275>::type __type276;
    typedef typename pythonic::assignable<__type211>::type __type277;
    typedef typename pythonic::assignable<__type197>::type __type278;
    typedef typename pythonic::assignable<__type221>::type __type279;
    typedef typename pythonic::assignable<__type245>::type __type280;
    typedef typename pythonic::assignable<__type137>::type __type281;
    typedef typename pythonic::assignable<__type186>::type __type282;
    typedef typename pythonic::assignable<__type202>::type __type283;
    typedef typename pythonic::assignable<__type123>::type __type284;
    typedef typename pythonic::assignable<__type268>::type __type285;
    typedef typename pythonic::assignable<__type188>::type __type286;
    typedef typename pythonic::assignable<__type237>::type __type287;
    typedef typename pythonic::assignable<__type159>::type __type288;
    typedef typename pythonic::assignable<__type199>::type __type289;
    __type286 p2_idx;
    __type287 z2;
    __type288 z1;
    __type289 p2;
    __type18 z_ = z;
    __type35 p_ = p;
    __type276 sos = pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(n_sections, std::integral_constant<long, 6>{}));
    if (pythonic::operator_::eq(pythonic::operator_::mod(pythonic::builtins::functor::len{}(p_), 2L), 1L))
    {
      p_ = pythonic::numpy::functor::append{}(p_, 0L);
      z_ = pythonic::numpy::functor::append{}(z_, 0L);
    }
    __type277 z__ = pythonic::numpy::functor::concatenate{}(_cplxreal()(z_));
    __type278 p__ = pythonic::numpy::functor::concatenate{}(_cplxreal()(p_));
    __type279 p_sos = pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(n_sections, std::integral_constant<long, 2>{}), pythonic::numpy::functor::complex128{});
    __type280 z_sos = pythonic::numpy::functor::zeros_like{}(p_sos);
    {
      long  __target139890632301840 = n_sections;
      for (long  si=0L; si < __target139890632301840; si += 1L)
      {
        typename pythonic::assignable_noescape<decltype(pythonic::numpy::functor::argmin{}(pythonic::numpy::functor::abs{}(pythonic::operator_::sub(1L, pythonic::numpy::functor::abs{}(p__)))))>::type p1_idx = pythonic::numpy::functor::argmin{}(pythonic::numpy::functor::abs{}(pythonic::operator_::sub(1L, pythonic::numpy::functor::abs{}(p__))));
        typename pythonic::assignable_noescape<decltype(p__[p1_idx])>::type p1 = p__[p1_idx];
        p__ = pythonic::numpy::functor::delete_{}(p__, p1_idx);
        {
          __type284 z1_idx_;
          if (pythonic::builtins::pythran::and_([&] () { return pythonic::numpy::functor::isreal{}(p1); }, [&] () { return pythonic::operator_::eq(pythonic::numpy::functor::sum{}(pythonic::numpy::functor::isreal{}(p__)), 0L); }))
          {
            typename pythonic::assignable_noescape<decltype(_nearest_real_complex_idx()(z__, p1, pythonic::types::str("real")))>::type z1_idx = _nearest_real_complex_idx()(z__, p1, pythonic::types::str("real"));
            z1 = z__[z1_idx];
            z__ = pythonic::numpy::functor::delete_{}(z__, z1_idx);
            p2= z2 = 0L;
          }
          else
          {
            if (pythonic::builtins::pythran::and_([&] () { return pythonic::operator_::not_(pythonic::numpy::functor::isreal{}(p1)); }, [&] () { return pythonic::operator_::eq(pythonic::numpy::functor::sum{}(pythonic::numpy::functor::isreal{}(z__)), 1L); }))
            {
              z1_idx_ = _nearest_real_complex_idx()(z__, p1, pythonic::types::str("complex"));
              pythonic::pythran_assert(pythonic::operator_::not_(pythonic::numpy::functor::isreal{}(z__[z1_idx_])));
            }
            else
            {
              z1_idx_ = pythonic::numpy::functor::argmin{}(pythonic::numpy::functor::abs{}(pythonic::operator_::sub(p1, z__)));
            }
            z1 = z__[z1_idx_];
            z__ = pythonic::numpy::functor::delete_{}(z__, z1_idx_);
            if (pythonic::operator_::not_(pythonic::numpy::functor::isreal{}(p1)))
            {
              {
                __type281 z2_idx;
                if (pythonic::operator_::not_(pythonic::numpy::functor::isreal{}(z1)))
                {
                  p2 = pythonic::numpy::functor::conj{}(p1);
                  z2 = pythonic::numpy::functor::conj{}(z1);
                }
                else
                {
                  p2 = pythonic::numpy::functor::conj{}(p1);
                  z2_idx = _nearest_real_complex_idx()(z__, p1, pythonic::types::str("real"));
                  z2 = z__[z2_idx];
                  pythonic::pythran_assert(pythonic::numpy::functor::isreal{}(z2));
                  z__ = pythonic::numpy::functor::delete_{}(z__, z2_idx);
                }
              }
            }
            else
            {
              {
                __type282 idx;
                __type283 z2_idx_;
                if (pythonic::operator_::not_(pythonic::numpy::functor::isreal{}(z1)))
                {
                  z2 = pythonic::numpy::functor::conj{}(z1);
                  p2_idx = _nearest_real_complex_idx()(p__, z1, pythonic::types::str("real"));
                  p2 = p__[p2_idx];
                  pythonic::pythran_assert(pythonic::numpy::functor::isreal{}(p2));
                }
                else
                {
                  idx = std::get<0>(pythonic::numpy::functor::nonzero{}(pythonic::numpy::functor::isreal{}(p__)));
                  pythonic::pythran_assert(pythonic::operator_::gt(pythonic::builtins::functor::len{}(idx), 0L));
                  p2_idx = idx[pythonic::numpy::functor::argmin{}(pythonic::numpy::functor::abs{}(pythonic::operator_::sub(pythonic::numpy::functor::abs{}(p__[idx]), 1L)))];
                  p2 = p__[p2_idx];
                  pythonic::pythran_assert(pythonic::numpy::functor::isreal{}(p2));
                  z2_idx_ = _nearest_real_complex_idx()(z__, p2, pythonic::types::str("real"));
                  z2 = z__[z2_idx_];
                  pythonic::pythran_assert(pythonic::numpy::functor::isreal{}(z2));
                  z__ = pythonic::numpy::functor::delete_{}(z__, z2_idx_);
                }
              }
              p__ = pythonic::numpy::functor::delete_{}(p__, p2_idx);
            }
          }
        }
        p_sos[si] = pythonic::builtins::pythran::functor::static_list{}(pythonic::types::make_tuple(p1, p2));
        z_sos[si] = pythonic::builtins::pythran::functor::static_list{}(pythonic::types::make_tuple(z1, z2));
      }
    }
    pythonic::pythran_assert(pythonic::operator_::eq(pythonic::builtins::functor::len{}(p__), pythonic::builtins::functor::len{}(z__)) and pythonic::operator_::eq(pythonic::builtins::functor::len{}(z__), 0L));
    
    typename pythonic::assignable_noescape<decltype(p_sos[pythonic::types::slice(pythonic::builtins::None,pythonic::builtins::None,-1L)])>::type p_sos_ = p_sos[pythonic::types::slice(pythonic::builtins::None,pythonic::builtins::None,-1L)];
    typename pythonic::assignable_noescape<decltype(z_sos[pythonic::types::slice(pythonic::builtins::None,pythonic::builtins::None,-1L)])>::type z_sos_ = z_sos[pythonic::types::slice(pythonic::builtins::None,pythonic::builtins::None,-1L)];
    __type285 gains = pythonic::numpy::functor::ones{}(n_sections, pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, pythonic::numpy::functor::array{}(k)));
    std::get<0>(gains) = k;
    {
      long  __target139890632372304 = n_sections;
      for (long  si_=0L; si_ < __target139890632372304; si_ += 1L)
      {
        sos[si_] = pythonic::numpy::functor::concatenate{}(zpk2tf()(z_sos_[si_], p_sos_[si_], gains[si_]));
      }
    }
    return sos;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename zpk2sos_multiple::type<argument_type0, argument_type1, argument_type2>::result_type zpk2sos_multiple::operator()(argument_type0&& z, argument_type1&& p, argument_type2&& k) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::concatenate{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
    typedef __type1 __type2;
    typedef typename pythonic::assignable<__type2>::type __type3;
    typedef __type3 __type4;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type5;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type6;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::max{})>::type>::type __type7;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type8;
    typedef __type8 __type9;
    typedef typename pythonic::assignable<__type9>::type __type10;
    typedef __type10 __type11;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type11>())) __type12;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type12>::type>::type __type13;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type4>())) __type15;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type15>::type>::type __type16;
    typedef decltype(pythonic::operator_::sub(std::declval<__type13>(), std::declval<__type16>())) __type17;
    typedef long __type18;
    typedef typename __combined<__type17,__type18>::type __type19;
    typedef decltype(std::declval<__type7>()(std::declval<__type19>(), std::declval<__type18>())) __type20;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type21;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type22;
    typedef __type22 __type23;
    typedef decltype(std::declval<__type21>()(std::declval<__type23>())) __type24;
    typedef typename pythonic::assignable<__type24>::type __type25;
    typedef __type25 __type26;
    typedef decltype(std::declval<__type6>()(std::declval<__type20>(), std::declval<__type26>())) __type27;
    typedef decltype(std::declval<__type5>()(std::declval<__type27>())) __type28;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type4>(), std::declval<__type28>())) __type29;
    typedef decltype(std::declval<__type0>()(std::declval<__type29>(), std::declval<__type18>())) __type30;
    typedef typename pythonic::assignable<__type30>::type __type31;
    typedef __type31 __type33;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type33>())) __type34;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type34>::type>::type __type35;
    typedef decltype(pythonic::operator_::sub(std::declval<__type35>(), std::declval<__type13>())) __type39;
    typedef typename __combined<__type39,__type18>::type __type40;
    typedef decltype(std::declval<__type7>()(std::declval<__type40>(), std::declval<__type18>())) __type41;
    typedef decltype(std::declval<__type6>()(std::declval<__type41>(), std::declval<__type26>())) __type43;
    typedef decltype(std::declval<__type5>()(std::declval<__type43>())) __type44;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type11>(), std::declval<__type44>())) __type45;
    typedef decltype(std::declval<__type0>()(std::declval<__type45>(), std::declval<__type18>())) __type46;
    typedef typename pythonic::assignable<__type46>::type __type47;
    typedef __type47 __type48;
    typedef pythonic::types::contiguous_slice __type49;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type50;
    typedef decltype(std::declval<__type50>()(std::declval<__type26>())) __type52;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type52>::type::iterator>::value_type>::type __type53;
    typedef __type53 __type54;
    typedef decltype(std::declval<__type48>()(std::declval<__type49>(), std::declval<__type54>())) __type55;
    typedef decltype(std::declval<__type33>()(std::declval<__type49>(), std::declval<__type54>())) __type58;
    typedef decltype(std::declval<__type23>()[std::declval<__type54>()]) __type61;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type48>())) __type66;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type66>::type>::type __type67;
    typedef typename __combined<__type35,__type67>::type __type68;
    typedef decltype(std::declval<__type7>()(std::declval<__type68>(), std::declval<__type67>())) __type69;
    typedef decltype(pythonic::operator_::add(std::declval<__type69>(), std::declval<__type18>())) __type70;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type70>(), std::declval<__type18>())) __type71;
    typedef typename pythonic::assignable<__type71>::type __type72;
    typedef __type72 __type73;
    typedef typename zpk2sos::type<__type55, __type58, __type61, __type73>::__ptype2 __type74;
    typedef container<typename std::remove_reference<__type74>::type> __type75;
    typedef typename __combined<__type47,__type75>::type __type76;
    typedef typename zpk2sos::type<__type55, __type58, __type61, __type73>::__ptype3 __type77;
    typedef container<typename std::remove_reference<__type77>::type> __type78;
    typedef typename __combined<__type31,__type78>::type __type79;
    typedef typename pythonic::assignable<__type79>::type __type80;
    typedef typename pythonic::assignable<__type76>::type __type81;
    typedef std::integral_constant<long, 6> __type84;
    typedef decltype(std::declval<__type6>()(std::declval<__type26>(), std::declval<__type73>(), std::declval<__type84>())) __type85;
    typedef decltype(std::declval<__type5>()(std::declval<__type85>())) __type86;
    typedef typename pythonic::assignable<__type86>::type __type87;
    typedef zpk2sos __type88;
    typedef decltype(std::declval<__type88>()(std::declval<__type55>(), std::declval<__type58>(), std::declval<__type61>(), std::declval<__type73>())) __type89;
    typedef container<typename std::remove_reference<__type89>::type> __type90;
    typedef typename __combined<__type87,__type90>::type __type91;
    typedef typename pythonic::assignable<__type91>::type __type92;
    typename pythonic::assignable_noescape<decltype(z)>::type z_ = z;
    typename pythonic::assignable_noescape<decltype(p)>::type p_ = p;
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::len{}(k))>::type nfilt = pythonic::builtins::functor::len{}(k);
    pythonic::pythran_assert(pythonic::operator_::eq(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, z_)), std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, p_))) and pythonic::operator_::eq(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, p_)), nfilt));
    __type80 p__ = pythonic::numpy::functor::concatenate{}(pythonic::types::make_tuple(p_, pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(pythonic::builtins::functor::max{}(pythonic::operator_::sub(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, z_)), std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, p_))), 0L), nfilt))), 0L);
    __type81 z__ = pythonic::numpy::functor::concatenate{}(pythonic::types::make_tuple(z_, pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(pythonic::builtins::functor::max{}(pythonic::operator_::sub(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, p__)), std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, z_))), 0L), nfilt))), 0L);
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::functor::floordiv()(pythonic::operator_::add(pythonic::builtins::functor::max{}(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, p__)), std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, z__))), 1L), 2L))>::type n_sections = pythonic::operator_::functor::floordiv()(pythonic::operator_::add(pythonic::builtins::functor::max{}(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, p__)), std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, z__))), 1L), 2L);
    __type92 sos = pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(nfilt, n_sections, std::integral_constant<long, 6>{}));
    {
      long  __target139890700418192 = nfilt;
      for (long  filt=0L; filt < __target139890700418192; filt += 1L)
      {
        sos(filt,pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None)) = zpk2sos()(z__(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),filt), p__(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),filt), k[filt], n_sections);
      }
    }
    return sos;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
inline
typename __pythran__zpk_funcs::zpk2sos_multiple::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>>::result_type zpk2sos_multiple0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& z, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& p, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& k) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__zpk_funcs::zpk2sos_multiple()(z, p, k);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__zpk_funcs::zpk2sos_multiple::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>>::result_type zpk2sos_multiple1(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& z, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& p, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& k) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__zpk_funcs::zpk2sos_multiple()(z, p, k);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__zpk_funcs::zpk2sos_multiple::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>>::result_type zpk2sos_multiple2(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& z, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>&& p, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& k) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__zpk_funcs::zpk2sos_multiple()(z, p, k);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__zpk_funcs::zpk2sos_multiple::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>>::result_type zpk2sos_multiple3(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& z, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>&& p, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& k) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__zpk_funcs::zpk2sos_multiple()(z, p, k);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__zpk_funcs::_cplxreal::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>::result_type _cplxreal0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& z) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__zpk_funcs::_cplxreal()(z);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap_zpk2sos_multiple0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"z", "p", "k",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]))
        return to_python(zpk2sos_multiple0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_zpk2sos_multiple1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"z", "p", "k",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]))
        return to_python(zpk2sos_multiple1(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_zpk2sos_multiple2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"z", "p", "k",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]))
        return to_python(zpk2sos_multiple2(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_zpk2sos_multiple3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"z", "p", "k",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]))
        return to_python(zpk2sos_multiple3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__cplxreal0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"z",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[0]))
        return to_python(_cplxreal0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_zpk2sos_multiple(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_zpk2sos_multiple0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_zpk2sos_multiple1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_zpk2sos_multiple2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_zpk2sos_multiple3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "zpk2sos_multiple", "\n""    - zpk2sos_multiple(complex[:,:], complex[:,:], float[:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall__cplxreal(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__cplxreal0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_cplxreal", "\n""    - _cplxreal(complex[:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "zpk2sos_multiple",
    (PyCFunction)__pythran_wrapall_zpk2sos_multiple,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - zpk2sos_multiple(complex[:,:], complex[:,:], float[:])"},{
    "_cplxreal",
    (PyCFunction)__pythran_wrapall__cplxreal,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - _cplxreal(complex[:])"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_zpk_funcs",            /* m_name */
    "",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_zpk_funcs)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
#if defined(GNUC) && !defined(__clang__)
__attribute__ ((externally_visible))
#endif
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_zpk_funcs)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("_zpk_funcs",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.11.0",
                                      "2022-07-07 06:41:21.961380",
                                      "b899aad88a57e48712df1ad0823acfa35403746bfe70efe19a440548a5712797");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif