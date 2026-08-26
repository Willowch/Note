1.docker架构,名词
![[Pasted image 20260812123401.png]]
![[Pasted image 20260812123434.png]]
镜像->类;容器->对象;
[[基础-Linux服务器购买]]

**安装过程**
*1.环境准备:*
* centos stream9/10的服务器;
* xshell连接服务器;
*2.环境查看:*
* cat /etc/os-release  #查看系统版本
	NAME="CentOS Stream"
	VERSION="10 (Coughlan)"
	RELEASE_TYPE=stable
	ID="centos"
	ID_LIKE="rhel fedora"
	VERSION_ID="10"
	PLATFORM_ID="platform:el10"
	PRETTY_NAME="CentOS Stream 10 (Coughlan)"
	ANSI_COLOR="0;31"
	LOGO="fedora-logo-icon"
	CPE_NAME="cpe:/o:centos:centos:10"
	HOME_URL="https://centos.org/"
	VENDOR_NAME="CentOS"
	VENDOR_URL="https://centos.org/"
	BUG_REPORT_URL="https://issues.redhat.com/"
	REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux 10"
	REDHAT_SUPPORT_PRODUCT_VERSION="CentOS Stream"
*3.安装*
* 卸载当前内容
	dnf remove docker \
	                  docker-client \
	                  docker-client-latest \
	                  docker-common \
	                  docker-latest \
	                  docker-latest-logrotate \
	                  docker-logrotate \
	                  docker-engine
	DNF是新一代的 RPM 软件包管理器,yum命令升级版
* 安装
	dnf -y install dnf-plugins-core   下载dnf官方核心插件工具包
	dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
	该命令会通过网络访问后面附带的 URL 链接，下载一个名为 docker-ce.repo 的配置文件，并将其自动保存到系统的 /etc/yum.repos.d/ 目录下。此后，你执行 dnf install docker-ce 时，系统就会从这个新增的源里去查找软件包。
	但由于阿里服务器翻不了外网,所以官方源无法访问;

	
* 启动
	systemctl enable --now docker
	检查:docker version
	![[Pasted image 20260812152450.png]]
* 测试
docker run hello-world
问题重现:本地没有helloworld镜像,需要拉取;但无法访问国外源,因此无法运行;
docker images
查看已下载的镜像
* 卸载
	* dnf remove docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
	卸载docker依赖
	* rm -rf /var/lib/docker  docker的默认工作路径
	* rm -rf /var/lib/containerd
	删除资源



[[基础-配置镜像加速器]]
[[基础-run的流程分析]]

[[基础-docker的常用命令]]