![[Pasted image 20260814181002.png]]![[Pasted image 20260814181119.png]]操作os内核的命令行解释器shell
![[Pasted image 20260814181216.png]]![[Pasted image 20260814181241.png]]![[Pasted image 20260814181837.png]]![[Pasted image 20260814181913.png]]![[Pasted image 20260814182149.png]]
unset静态变量会报错:
![[Pasted image 20260814182210.png]]
![[Pasted image 20260814182234.png]]![[Pasted image 20260814182416.png]]
环境变量定义在/etc/profile文件中,生效后才可使用;
![[Pasted image 20260814182531.png]]![[Pasted image 20260814182536.png]]![[Pasted image 20260814182828.png]]![[Pasted image 20260814183250.png]]
![[Pasted image 20260814183142.png]]![[Pasted image 20260814183157.png]]![[Pasted image 20260814183217.png]]![[Pasted image 20260814183234.png]]
![[Pasted image 20260814183311.png]]![[Pasted image 20260814183633.png]]![[Pasted image 20260814184311.png]]![[Pasted image 20260814184512.png]]![[Pasted image 20260814184518.png]]![[Pasted image 20260814185929.png]]三目运算符:![[Pasted image 20260814190536.png]]![[Pasted image 20260814185937.png]]![[Pasted image 20260814185944.png]]![[Pasted image 20260814185950.png]]
![[Pasted image 20260814190631.png]]![[Pasted image 20260814190946.png]]![[Pasted image 20260814191035.png]]![[Pasted image 20260814191043.png]]![[Pasted image 20260814191438.png]]![[Pasted image 20260814191509.png]]![[Pasted image 20260814191640.png]]![[Pasted image 20260814191818.png]]![[Pasted image 20260814191953.png]]![[Pasted image 20260814192025.png]]![[Pasted image 20260814192402.png]]![[Pasted image 20260814192450.png]]![[Pasted image 20260814192533.png]]![[Pasted image 20260814192552.png]]![[Pasted image 20260814192634.png]]
可以不传入参数,而调用时传入;
![[Pasted image 20260814192817.png]]![[Pasted image 20260814193929.png]]![[Pasted image 20260814193941.png]]
$()和\`\`会先执行其中的命令后,再将内容赋给变量;
[! -d "${BACKUP}/${DATETIME}"]为判断目录是否存在,!为取反,若不存在,条件成立;
mysqldump -u\${DB_USER} -p\${DB_PW} --host=${HOST} -q -R --databases \${DATABASE} | gzip > \${BACKUP}/\${DATETIME}/\${DATETIME}.sql.gz
管道符:将备份的sql内容 直接压缩到.gz文件;
tar -zcvf \$DATETIME.tar.gz \${DATETIME}
将刚才放.sql.gz文件连带目录打包为.tar.gz文件;
find 以名字时,可以用字符串通配符;
;号可以隔绝代码行;
find \$\{BACKUP\} -atime +10 -name \"\*.tar.gz\" -exec rm -rf {} \\;
![[Pasted image 20260814194916.png]]
这里的分号是find命令一部分,而非语句结束,故转义;
![[Pasted image 20260814195102.png]]