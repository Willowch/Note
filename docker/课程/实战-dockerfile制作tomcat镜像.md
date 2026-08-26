![[Pasted image 20260817121135.png]]![[Pasted image 20260817123623.png]]![[Pasted image 20260817133041.png]]
linux中 路径间的冒号是分隔符,代表前后为两个路径;
CLASSPATH为java类搜索路径;CATALITA为tomcat的目录;PATH为环境变量;
$PATH为拼接原有的环境变量;

3.build镜像
docker builder -t diytom
由于Dockerfile是官方名称,不用指定文件目录,docker会自动查找;

4.运行镜像:
docker run -d -p 9090:8080 --name willowTom \
  -v /root/temp/test:/usr/local/apache-tomcat-9.0.65/webapps/test \
  -v /root/temp/tomcatlogs:/usr/local/apache-tomcat-9.0.65/logs \
  diytom
将两个文件夹挂载到本地,并运行容器
进入容器查看:
docker exec -it 容器号 /bin/bash

5.新建页面
test目录下:新建WEB-INF目录,index.jsp文件
mkdir WEB-INF 
vim index.jsp:

<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>

<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>hello, willowch</title>
</head>
<body>
Hello World!<br/>
<% System.out.println("nihao willow"); %>
</body>
</html>

在WEB-INF目录下新建web.xml文件:
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://java.sun.com/xml/ns/javaee"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://java.sun.com/xml/ns/javaee
    http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd"
    version="2.5">
</web-app>
 

解释:
![[Pasted image 20260817153357.png]]
![[Pasted image 20260817153440.png]]
![[Pasted image 20260817153456.png]]
![[Pasted image 20260817153540.png]]

[[实战-发布镜像]]
