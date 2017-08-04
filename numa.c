#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <sys/types.h>
#include <numa.h>
#include <sched.h>
#include <inttypes.h>

int core_mem_binding(int core, int mem, int pid) {
  // Memory parameter initialize
  char mem_node[2];
  struct bitmask* mem_node_bit;
  sprintf(mem_node, "%d", mem);
  mem_node_bit = numa_parse_nodestring(mem_node);

  // Core parameter initialize
  cpu_set_t cpu_mask;
  CPU_ZERO(&cpu_mask);
  CPU_SET(core, &cpu_mask);

  // Memory Binding
  numa_set_membind(mem_node_bit);

  // Core Binding
  if (sched_setaffinity(pid, sizeof(cpu_set_t), &cpu_mask)) {
    fprintf(stderr, "Failed to %d core binding\n", core);
    return 0;
  }

  printf("Process bind in %d core, %d node\n", core, mem);
  return 1;

}

//int main() {
//	return 0;
//}
