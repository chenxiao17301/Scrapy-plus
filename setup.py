#coding:utf-8

try: # for pip <= 9.0.1
    from pip.req import parse_requirements
except: # for pip >= 10.0.1
    from pip._internal.req import parse_requirements


from setuptools import find_packages, setup


# with open(join(dirname(__file__), './VERSION.txt'), 'rb') as f:
#     version = f.read().decode('ascii').strip()
# 获取版本号
with open("./VERSION.txt", "r") as f:
    version = f.read().strip()

    """
        作为一个合格的模块，应该要有版本号哦。
    """

setup(
    name='scrapy_plus',    # 模块名称
    version=version,
    description='A mini spider framework, like Scrapy',    # 描述
    packages=find_packages(exclude=[]),
    author='itcast',
    author_email='your@email.com',
    license='Apache License v2', # GPL、BSD、APL
    # 纯开源，免费使用源码再发行
    # 免费使用可以该源码，但是不能卖钱
    # 免费使用，不允许修改源码
    # 付费使用，需要购买注册码
    package_data={'': ['*.*']},
    url='#',
    install_requires=[str(ir.req) for ir in parse_requirements("requirements.txt", session=False)],#所需的运行环境
    zip_safe=False, # Windows下使用。防止卸载报错
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
