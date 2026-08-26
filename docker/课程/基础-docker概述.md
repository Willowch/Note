1.docker引入:
![[Pasted image 20260812115454.png|697]]
项目 带上自身所需要的环境 
![[Pasted image 20260812115728.png]]
docker解决思路
![[Pasted image 20260812120042.png]]
隔离;打包;

2.docker的历史和优势
![[Pasted image 20260812121008.png]]
虚拟机模拟整个电脑;而docker容器化,只虚拟需要的部分,因此小巧;

3.docker基本
基于go语言开发
![[Pasted image 20260812121309.png]]
dockerhub上其他人发布的镜像,可用类似于git的命令获取;

4.docker的优势
![[Pasted image 20260812121901.png|510]]
虚拟机技术缺点:1.资源占用多(模拟整个电脑)2.冗余步骤多3.启动慢
![[Pasted image 20260812122058.png|514]]
![[Pasted image 20260812122515.png]]
扩容:要扩展服务器a,则在b上运行a,在b上进行扩展;
[[基础-docker安装]]