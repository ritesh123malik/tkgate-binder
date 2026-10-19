/* Run with AddressSanitizer to catch pool teardown overruns on LP64. */
#include <assert.h>
#include <string.h>
#include "ycmalloc.h"

int main(void)
{
  int cycle, block;
  yc_setup();
  for (cycle = 0; cycle < 20; ++cycle) {
    for (block = 0; block < 40; ++block) {
      char *p = yc_calloc(1024, 1, ALGN_LONG);
      assert(p[0] == 0 && p[1023] == 0);
      memset(p, 0x5a, 1024);
    }
    yc_freeall();
  }
  yc_poppool();
  return 0;
}
