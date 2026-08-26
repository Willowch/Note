![[Pasted image 20260817172834.png]]![[Pasted image 20260817202408.png]]![[Pasted image 20260817202606.png]]
启动了一个容器后,就会多一对网卡(ip),261,262;
其中容器内为261:262;而外部为262:261;
![[Pasted image 20260817203013.png]]
![[Pasted image 20260817203257.png]]
![[Pasted image 20260817203433.png]]原理图:![[Pasted image 20260817203650.png]]
![[Pasted image 20260817203953.png]]![[Pasted image 20260817204107.png]]![[Pasted image 20260817204605.png]]
![[Pasted image 20260817204754.png]]
docker inspect 容器id    查看网络配置;
![[Pasted image 20260817205209.png]]
在tomcat03的/etc/hosts文件中配置了tomcat02,即访问tomcat02就走到前面的地址中;
故用容器名称也可以ping通;
![[Pasted image 20260817205429.png]]
[[进阶-自定义网络]]
