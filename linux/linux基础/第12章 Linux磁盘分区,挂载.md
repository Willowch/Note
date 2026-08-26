![[Pasted image 20260814122332.png]]
分区是物理存储空间的逻辑划分;
挂载:将分区(存储空间)与一个现有空目录关联;访问此目录即可访问分区数据;
挂载执行:当执行挂载mount /dev/sdb1 /tmp/usb时,调用文件系统"翻译"原始01存储文件(sdb1),将分析数据(哪些扇区组成照片.jpg,文件名是什么等)关联到Usb;这样访问usb才可以能看懂的方式访问分区数据;
![[Pasted image 20260814123924.png]]![[Pasted image 20260814124034.png]]![[Pasted image 20260814124301.png]]
vd为虚拟io磁盘; vda3挂载到/,说明主存储39.8G在vda3;
![[Pasted image 20260814124534.png]]![[Pasted image 20260814124546.png]]![[Pasted image 20260814124556.png]]
w
![[Pasted image 20260814124648.png]]![[Pasted image 20260814124836.png]]![[Pasted image 20260814125050.png]]![[Pasted image 20260814125133.png]]![[Pasted image 20260814125151.png]]