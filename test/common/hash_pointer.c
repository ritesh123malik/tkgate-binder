/* Standalone regression: cc -Isrc/common test/common/hash_pointer.c
 * src/common/hash.c -o /tmp/tkgate-hash-test && /tmp/tkgate-hash-test */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hash.h"

/* The regression uses the ordinary allocator; satisfy the object allocator API. */
void *ob_malloc(int n, char *name) { (void)name; return malloc(n); }
void *ob_calloc(int n, int size, char *name) { (void)name; return calloc(n, size); }
void ob_free(void *p) { free(p); }
char *ob_strdup(const char *s) { return strdup(s); }
void ob_touch(void *p) { (void)p; }

int main(void)
{
  PHash *h = new_PHash_noob();
  int values[256];
  uintptr_t keys[256];
  HashElem *e;
  unsigned count = 0;
  int i;

  for (i = 0; i < 256; i++) {
#if UINTPTR_MAX > UINT32_MAX
    keys[i] = ((uintptr_t)(i + 1) << 32) | 0x1234;
#else
    keys[i] = (uintptr_t)(i + 1) * 256 | 0x34;
#endif
    values[i] = i;
    assert(PHash_insert(h, (void *)keys[i], &values[i]) == 0);
  }
  assert(Hash_numElems(h) == 256);
  for (i = 0; i < 256; i++) {
    assert(PHash_find(h, (void *)keys[i]) == &values[i]);
    assert(PHash_insert(h, (void *)keys[i], &values[i]) == -1);
  }
  for (e = Hash_first(h); e; e = Hash_next(h, e)) {
    int index = *(int *)HashElem_obj(e);
    assert((uintptr_t)PHashElem_key(e) == keys[index]);
    count++;
  }
  assert(count == 256);
  assert(NHash_replace(h, keys[0], &values[1]) == 0);
  assert(PHash_find(h, (void *)keys[0]) == &values[1]);
  assert(PHash_remove(h, (void *)keys[0]) == 0);
  assert(PHash_find(h, (void *)keys[0]) == NULL);
  assert(PHash_find(h, (void *)keys[1]) == &values[1]);
  assert(NHash_insert(h, -1, &values[0]) == 0);
  assert(NHash_find(h, -1) == &values[0]);
  assert(NHash_remove(h, -1) == 0);
  delete_PHash(h);
  puts("Pointer hash high-bit identity, iteration, resize, replace, remove and integer IDs: PASS");
  return 0;
}
