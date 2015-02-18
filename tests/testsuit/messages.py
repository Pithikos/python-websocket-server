#
# Fixed messages by length
# Every message ends with its length..
#

msg_125b   = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqr125'                                  # 125
msg_126b   = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrs126'                                 # 126
msg_127b   = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrst127'                                # 127
msg_208b   = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'\
             'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvw208'   # 208
msg_1251b  = (msg_125b*10)+'1'       # 1251
msg_68Kb   = ('a'*67995)+'68000' # 68000
msg_1500Kb = ('a'*1500000)+'1500000' # 1.5Mb
