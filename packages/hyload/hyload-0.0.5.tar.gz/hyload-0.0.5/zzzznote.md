## 注意

确保所有python包 子目录里面都有 `__init__.py` , 否则打包安装会有问题



## minify
https://python-minifier.com/

pip install python-minifier

```bat
CHCP 65001
pyminify --remove-literal-statements hyload/httpclient.py>hyload/httpclient.py
```



## 编译package
<!-- 
参考  https://packaging.python.org/tutorials/packaging-projects/

参考 https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
 -->


```py
python setup.py sdist
```

## 安装twine

    pip install  twine
    

<br>
    
## 上传pypi

先修改  version 版本， 然后

1. 先上传到测试pypi

直接执行 publish-test.bat

在输入用户名密码之前， 

打开 dist目录里面的tar文件，看看utils目录里面的东西全不全。 

然后，直接 `pip install d:\projects\byhy\hyload\dist\hyload-0.1.XXXXX.tar.gz` 本地安装看看能不能成功，如果可以，

再输入用户名密码

username: byhy
password: Itellin1!
    
    
然后测试一下 

    pip install hyload -U --index-url https://test.pypi.org/simple/    

<br>

2. 测试没有问题后，再上传到 pypi

直接执行 publish.bat

username: byhy
password: Itellin1!



