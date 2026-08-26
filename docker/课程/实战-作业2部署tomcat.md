![[Pasted image 20260815112458.png]]
问题解决: 进入容器后,将webapp.dist目录下的文件全部 放到 webspps目录下即可;
cp -r webapps.dist/* webapps
容器在服务器后端运行,即可通过网页来访问(若更改网页,可进行更改)
[[实战-作业3部署es+Kibana]]
