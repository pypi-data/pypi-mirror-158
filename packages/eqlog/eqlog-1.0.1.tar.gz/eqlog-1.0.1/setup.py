from setuptools import setup, find_packages

setup(
    name="eqlog",
    version="1.0.1",
    keywords=("eqlog", "log", "logging", "logger"),
    description="日志工具",
    long_description="日志工具：1.0.1修复文件读取bug",
    license="GPL-2.0",

    url="https://gitee.com/jingenqiang/eqlog.git",
    author="eq",
    author_email="eq_enqiang@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)

"""
项目打包
python setup.py bdist_egg     # 生成类似 eqlog-0.0.1-py2.7.egg，支持 easy_install 
# 使用此方式
python setup.py sdist         # 生成类似 eqlog-0.0.1.tar.gz，支持 pip
# twine 需要安装
twine upload dist/eqlog-1.0.1.tar.gz
"""
