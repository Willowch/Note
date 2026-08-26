![[Pasted image 20260812155243.png]]

*docker底层原理*
Docker 是一个Client-Server结构的系统，Docker的守护进程运行在主机上。通过Socket从客户端访问!
DockerServer接收到Docker-client的指令，就会执行这个命令
![[Pasted image 20260812155825.png]]
![[Pasted image 20260812160232.png]]
host os:宿主机os;  guess os:虚拟机os;
docker不用加载客户机os,直接利用宿主机os,因此较快;
