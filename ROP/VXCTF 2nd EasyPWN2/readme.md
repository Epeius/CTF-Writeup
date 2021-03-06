# VXCTF 2nd EasyPWN2

題目:

>EasyPWN2
>Another pwn, a little bit harder than easypwn1.
>Hint: no hint
>
>[bof2](bof2)
>
>[libc.so.6](libc.so.6)

呢題寫parsing addr 個script有d難, 其他都只係基本ROP


首先IDA左佢,

```C++
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  const char **v3; // [sp+0h] [bp-30h]@1
  char s[8]; // [sp+1Ch] [bp-14h]@8
  int v5; // [sp+24h] [bp-Ch]@8
  int v6; // [sp+28h] [bp-8h]@5
  int v7; // [sp+2Ch] [bp-4h]@2

  v3 = argv;
  set_gid(*(_QWORD *)&argc, argv, envp);
  while ( 1 )
  {
    write(1, "\n1. Print Message\n", 0x12uLL);
    write(1, "2. Change Message\n", 0x12uLL);
    write(1, "3. Exit\n", 8uLL);
    write(1, "Input:\n", 7uLL);
    scanf("%d", &v7, v3);
    if ( v7 != 1 && v7 != 2 )
      break;
    if ( v7 == 1 )
    {
      v6 = 0;
      write(1, "The message-id that you would like to print[0-2]:\n", 0x32uLL);
      scanf("%d", &v6);
      if ( v6 > 2 )
        exit(0);
      write(1, &message1 + v6, 8uLL);
      putchar(10);
    }
    else
    {
      v5 = 0;
      *(_QWORD *)s = 0LL;
      write(1, "The message-id that you would like to change[0-2]:\n", 0x33uLL);
      scanf("%d", &v5);
      if ( v5 > 2 )
        exit(0);
      write(1, "New massage[at most 8 word]:\n", 0x1DuLL);
      scanf("%8s", s);
      if ( strchr(s, 37) )
      {
        write(1, "Don't hurt me!", 0xEuLL);
        exit(0);
      }
      *(&message1 + v5) = *(_QWORD *)s;
    }
  }
  exit(0);
}
```
由於佢只係check input 係唔係大過2,加上:

```C++
 *(&message1 + v5) = *(_QWORD *)s;
 ```

所以可以用黎做越界存取

我地可以用呢個bug leak libc base,做got hijacking,再get shell.

可以點樣leak libc addr/got table?

望一望個data段,可以利用輸入負數,leak到一堆got table addr,再利用libc 求libc base,再加返去system或者指去任意libc code

```
.got.plt:0000000000601018 off_601018      dq offset putchar       ; DATA XREF: _putcharr
.got.plt:0000000000601020 off_601020      dq offset write         ; DATA XREF: _writer
.got.plt:0000000000601028 off_601028      dq offset setresgid     ; DATA XREF: _setresgidr
.got.plt:0000000000601030 off_601030      dq offset strchr        ; DATA XREF: _strchrr
.got.plt:0000000000601038 off_601038      dq offset getegid       ; DATA XREF: _getegidr
.got.plt:0000000000601040 off_601040      dq offset scanf         ; DATA XREF: _scanfr
.got.plt:0000000000601048 off_601048      dq offset exit          ; DATA XREF: _exitr
.got.plt:0000000000601048 _got_plt        ends
.got.plt:0000000000601048
                              .
                              .
                              .

.data:000000000060105F                 db    0
.data:0000000000601060                 public message1
.data:0000000000601060 ; _QWORD message1
````

呢個時候有atleast兩個possible solution,

1.執行system("/bin/sh")

2.one time RCE Gadget

首先就講左work個個solution先.

由x64 calling convention,我地知道係system 執行save 左係rdi 裏面嘅argument

所以目標好簡單,就係要做一個類似 pop_rdi_ret+/bin/sh\x00+system_addr 嘅 payload

不過由於冇bof,所以只可以GOT hijacking之後再ret2libc

咁我地可以hijack邊個function,其實只有一個:_strchr

因為其他function係原本嘅call之前都做左mov rdi,0 呢個動作 (´･ω･`)

follow呢個思路,個exploit其實好簡單...

寫好個addr parser, nc之後揀1,leak 1個已經call左嘅function eg.scanf, 用提供嘅libc計libc base

再用function 2 overwrite strchr,再用function 2 係position 0 input /bin/sh\x00 

佢call strchr個刻就execute system("/bin/sh\x00") get shell (•‿•)

[solve.py](solve.py)

# One time RCE Gadget

至於one time rce gadget,其實係源於Dragon Sector [Dragons’ notes on CTFs](http://j00ru.vexillium.org/slides/2015/insomnihack.pdf)

佢裏面講到libc裏面有mov rdi,/bin/sh   call exceve 嘅 code segment

用IDA check libc:
```asm
.text:000000000004647C                 mov     rax, cs:environ_ptr_0
.text:0000000000046483                 lea     rdi, aBinSh     ; "/bin/sh"
.text:000000000004648A                 lea     rsi, [rsp+180h+var_150]
.text:000000000004648F                 mov     cs:dword_3C46C0, 0
.text:0000000000046499                 mov     cs:dword_3C46D0, 0
.text:00000000000464A3                 mov     rdx, [rax]
.text:00000000000464A6                 call    execve
.text:00000000000464AB                 mov     edi, 7Fh        ; status
.text:00000000000464B0                 call    _exit
```

真係有呢段code, 不過係呢題用唔到,因為行到去exceve個陣; rsi,rdi唔滿足call exceve嘅要求

再係gdb強制將rsi rdx set 0,可以彈到shell,不過即刻exit (´-ω-`)

相信call one time gadget之前要call一個 xor_rsi_rxi_.........嘅gadget,再call rce gadget and get shell

希望遲d可以玩下呢個payload (｀▽´)


