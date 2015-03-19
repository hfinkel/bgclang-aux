#ifdef __llvm__
/*
 * The declaration of this function in V1R2M2 fails to specify __INLINE__.
 */

#include <hwi/include/common/compiler_support.h>

__INLINE__
uint64_t Kernel_GetJobID();

#include_next <spi/include/kernel/process.h>
#endif

