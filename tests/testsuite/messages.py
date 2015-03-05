#
# Fixed messages by length
# Every message ends with its length..
#

msg_125B   = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqr125'
msg_126B   = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrs126'
msg_127B   = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrst127'
msg_208B   = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvw208'
msg_1251B  = (msg_125B*10)+'1'       # 1251
msg_68KB   = ('a'*67995)+'68000'     # 68000
msg_1500KB = ('a'*1500000)+'1500000' # 1.5Mb
