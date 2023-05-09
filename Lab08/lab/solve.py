import angr
import sys
import struct

main_addr = 0x4011a9
find_addr = 0x401371
avoid_addr = 0x401385



class my_scanf(angr.SimProcedure):
    def run(self, format, size):
        simfd = self.state.posix.get_fd(sys.stdin.fileno())
        data,real_size = simfd.read_data(struct.calcsize('i'))
        self.state.memory.store(size, data)
        return 1 

proj = angr.Project('./src/prog', load_options={'auto_load_libs': False})
proj.hook_symbol('__isoc99_scanf', my_scanf(), replace=True)
state = proj.factory.blank_state(addr=main_addr)

simgr = proj.factory.simulation_manager(state)
simgr.explore(find=find_addr, avoid=avoid_addr)
if simgr.found:
    # print(simgr.found[0].posix.dumps(sys.stdin.fileno()))
    ans_bytes_str = simgr.found[0].posix.dumps(sys.stdin.fileno())
    with open('solve_input', 'w') as file:
        for i in range(0, len(ans_bytes_str), 4):
            temp = int.from_bytes(ans_bytes_str[i:i+4], byteorder='little', signed=True)
            # print(i, ": ", temp)
            # print(str(temp))
            file.write(str(temp) + '\n')
else:
    print('Failed')