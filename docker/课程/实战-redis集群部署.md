![[Pasted image 20260817213941.png]]
目标:redis集群,例如当r-m3失效,则r-s3备份可以顶上使用;
统一集群所以建立网络;
1.创建redis网络
![[Pasted image 20260817214116.png]]
2.通过脚本创建
![[Pasted image 20260817214311.png]]
![[Pasted image 20260817215045.png]]![[Pasted image 20260817215054.png]]
通过执行脚本来创建;
3.运行服务
![[Pasted image 20260817220050.png]]![[Pasted image 20260817220433.png]]![[Pasted image 20260817220449.png]]![[Pasted image 20260817220456.png]]
创建脚本来启动6个容器:
![[Pasted image 20260817221516.png]]
查看:redis1-6![[Pasted image 20260817221545.png]]
4.创建集群:
进入容器:
![[Pasted image 20260817221655.png]]
![[Pasted image 20260817221846.png]]查看集群:![[Pasted image 20260817221939.png]]
[[进阶-项目打包]]
