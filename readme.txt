这里的代码是我在学习这里的一门视频课程的时候，写下 的代码
这里是课程的地址https://coding.imooc.com/class/78.html，希望大家能够多多支持
这个讲师bobby讲的还是很不错的，因为是别人分享的课程视频，没有相应的课程源码，不过也还好，整个过程一直都是自己敲下来的，前前后后从开始3月初，到现在3月21号，20多天了吧，收获了许多吧！这周末抽空把学到的东西整理一下，传上来。
遇到了蛮多的bug，大概花了有20个小时左右的时间在bugs上，包括配置环境，写代码的时候出现的问题，以及最后在搭建服务器的时候，都遇到了一些问题。最后求人求Google，也都算解决了。


USAGE:
1.pycharm, python3.5+, mysql
2.使用的时候，注意先在mooc文件夹下面的setting.py 里面进行配置，数据库我使用的是云端的，只需要把本地或者云端数据库的参数补上就可以了(96行)，网站里面有个发送邮件的部分(150行)，我是使用的自己的邮箱进行的注册，服务器是163的stmp，这部分的配置，可以自行进行百度，问题不大的，有一点是，现在的邮箱多为了安全，不允许直接使用用户密码进行客户端登录操作，所以要设置一个临时的登录密码进行登录。这是这两个地方需要修改的。

#上面的邮箱不配置应该也是OK的，只是在需要发送验证码的时候，会报错

这些配置好了以后，把requirements.txt文件中的xadmin那一行删除，使用源代码安装
pip install git+git://github.com/sshwsfc/xadmin.git
主要是pip 库安装会出现一些难以预料的问题，然后使用pip 安装requirements.txt 中的依赖

先做次makemigrations  &migrate
连接上就可以运行了。
使用我提供的sql文件添加到数据库数据就可以了



ATTENTION:
1.最开始拿到html,css,js文件的压缩包的时候，login.html有一些"损伤"，所以登录页面就会有些问题，不过不影响登录
2.整个后台都是都是动态的，所以把这些后台的数据都导出成sql文件，方便大家复现(文件是sql.rar)
3.运行之前先做次makemigrations  &migrate


	先写这么多吧，有问题再提



以下来自google translate：

The code here is the code I wrote when I was studying a video course here.
Here is the address of the course https://coding.imooc.com/class/78.html, hope everyone can support it
The lecturer bobby said it was still very good, because it was a lesson video shared by others. There was no corresponding course source code, but it was okay. The whole process had been knocked down from the beginning to the end of March. On the 21st of the month, more than 20 days have passed, and many have been harvested! This weekend took time to sort out what I learned and pass it on.
A lot of bugs have been encountered. It took about 20 hours or so on bugs, including configuring the environment, problems with writing code, and finally problems in building the server. In the end, asking for someone to ask Google has also been resolved.


USAGE:
1.pycharm, python3.5+, mysql
2. When using, pay attention to the settings.py inside the mooc folder to configure. The database I use is the cloud, you only need to fill in the parameters of the local or cloud database (96 lines), website There is a part of the sending mail (150 lines), I use my own mailbox to register, the server is 163 stmp, this part of the configuration, you can own Baidu, the problem is not, there is one point, the current mailbox For security reasons, it is not allowed to use the user password directly for client login. Therefore, you must set a temporary login password to log in. This is where these two places need to be modified.

# The above mailbox is not configured should also be OK, but when you need to send a verification code, it will report an error

After these configurations are completed, delete the xadmin line in the requirements.txt file and install it using source code.
Pip install git+git://github.com/sshwsfc/xadmin.git
Primarily pip-library installations have some unforeseen problems and then use pip to install dependencies in requirements.txt

Do makemigrations &migrate first
Connection can run.
Use the sql file I provided to add data to the database



ATTENTION:
1.When you first get the html, css, and js files, there are some "damages" in login.html, so the login page will have some problems, but it won't affect the login.
2.The entire background is all dynamic, so these background data are exported to sql files, so that everyone can reproduce (the file is sql.rar)
3. Do makemigrations &migrate before running



Write so much first, then there is a problem you can ask！



