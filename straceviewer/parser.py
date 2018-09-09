from lark import Lark

# parser for strace files generated with:
#  strace -ff -ttt -T -o output command

# XXX line length !


# real example:
# strace -ff -ttt -T -o test/ls-full.out bash -c 'time ls'

# XXX
# Attached pid
#
strace_parser = Lark(r"""
    start: lines
    lines: (line NEWLINE)*
    line: attached_process_line
        | syscall_line
        | signal_line
        | exit_process_line
    attached_process_line: "TODO"
    exit_process_line: timestamp "+++ exited with" INT "+++" 

    syscall_line: timestamp system_call "=" return_code ("<" execution_time ">")?
    signal_line: timestamp "---" signal signal_args "---"
    signal: CNAME
    signal_args: enum_arg

    timestamp: FLOAT
    execution_time: FLOAT

    return_code: (SIGNED_NUMBER) return_code_description
        | MEM_ADDRESS // brk
        | "?"
    return_code_description:
        | CNAME (" (" (WORD | "-")+ ")")?

    system_call: system_call_name "(" system_call_args ")"
    system_call_name: CNAME
    system_call_args:
        | system_call_arg ("," system_call_arg)*

    system_call_arg: arg
        
    arg: float_arg
        | makedev_arg
        | named_arg
        | xxx_ioctl_arg
        | xxx_rt_sigprocmask_arg
        | int_arg
        | string_arg
        | list_arg
        | const_arg
        | enum_arg
        | mem_address_arg
        | arg_wifexited_wifexitstatus_arg
        | omitted_entries
        | omitted_vars

    float_arg: FLOAT
    int_arg: SIGNED_NUMBER | formula_int_arg

    // 1536404141.861610 wait4(-1, [{WIFEXITED(s) && WEXITSTATUS(s) == 0}], 0, NULL) =
    //                               ^
    arg_wifexited_wifexitstatus_arg: "{WIFEXITED(s) && WEXITSTATUS(s) == " INT "}"

    // 9 getrlimit(RLIMIT_STACK, {rlim_cur=8192*1024, rlim_max=RLIM64_INFINITY}) = 0 <0
    //                                     ^
    formula_int_arg: SIGNED_NUMBER "*" SIGNED_NUMBER

    named_arg: CNAME "=" arg

    const_arg: CNAME("|" CNAME)*
    string_arg: ESCAPED_STRING (elipsys)?
    mem_address_arg: MEM_ADDRESS

    list_arg: "[" list_arg_members "]"(elipsys)?
    list_arg_members: | list_arg_member ("," list_arg_member)*
    list_arg_member: arg
    
    omitted_entries: "/* " INT " entries */"
    omitted_vars: "/* " INT " vars */"

// XXX "named" enum ?
    enum_arg: "{" enum_members "}"
    enum_members: enum_member ("," enum_member)*
    enum_member: CNAME "=" enum_values
        | elipsys
    enum_values: enum_value ("|" enum_value)*
    enum_value: arg 

// , {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 15), ...}) = 0 <0.000006>
//                                  ^
    makedev_arg: "makedev(" INT ", " INT ")"

// XXX what is this ? it's used in ioctl
// 1536404141.870591 ioctl(1, TCGETS, {B38400 opost isig icanon echo ...}) = 0 <0.000008>
//                                     ^
    xxx_ioctl_arg: "{" xxx_ioctl_members "}"
    xxx_ioctl_members: (xxx_ioctl_member | elipsys)+
    xxx_ioctl_member: const_arg | int_arg

// XXX what is this ? it's used in:
//  rt_sigprocmask(SIG_UNBLOCK, [RTMIN RT_1], NULL, 8) = 0 <0.000006>
//                               ^
    xxx_rt_sigprocmask_arg: "[" const_arg(const_arg)* "]"
    elipsys: "..."
  
    MEM_ADDRESS: "0x" (LETTER|INT)+
    %import common.WORD
    %import common.CNAME
    %import common.FLOAT
    %import common.LETTER
    %import common.INT
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.NEWLINE
    %import common.WS
    %ignore WS

    """)
