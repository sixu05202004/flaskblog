flaskblog
===========

简介
^^^^^^^^^^^^

这是一个使用 Flask 开发的个人博客，其目前运行的地址为：http://www.pythonpub.com/


步骤
^^^^^^^^^^^^^

1. pip install -r requirement.txt，安装所有必要的扩展。


2. python manager.py createall，创建所有相关的表，但是首先需要修改 config.py:SQLALCHEMY_DATABASE_URI


3. python manager.py runserver
   
4. 访问 127.0.0.1:5000/login，提交你的文章，访问 127.0.0.1:5000/ 查看首页情况


更多信息
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

flaskblog-blueprints 文件夹中是用蓝图实现的flaskblog，用于说明蓝图的基本使用. 这个只是一个简单的例子，为了方便熟悉蓝图(blueprint)使用，目前templates是集中放在一起的，可以分别放入每一个app单独的文件夹，只需要在指定template_folder='templates'。

例如：about = Blueprint('about', __name__,
                        template_folder='templates')

本例子十分简单，不适合使用蓝图，如果有大型的应用的话，建议使用蓝图。如果只是中小型的应用话，可以参考这个结构:
https://github.com/sixu05202004/autotest

另一个是： https://github.com/sixu05202004/newsmeme