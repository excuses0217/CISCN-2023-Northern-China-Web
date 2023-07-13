#!/bin/bash
sleep 1

# 设置 flag 动态替换
flagfile=/flag
if [ -f $flagfile ]; then
    sed -i "s/flag{.*}/$(cat /root/flag.txt)/" $flagfile
fi

su ctfer -c "python3 app.py"
/usr/bin/tail -f /dev/null