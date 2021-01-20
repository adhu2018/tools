# -*- coding: utf-8 -*-
import sys
import importlib

# 动态加载模块 相当于在{path}路径下使用`import {_module}`
def reload(_module="tools", path=None, raise_=False):
    """
    试用阶段！！
    
    - 在系统环境路径列表`最前方`插入{path}
    - 使用`importlib.import_module(".", _module)`导入模块
    - 测试中，从`dir({_module})`的结果来看，相关的 类/函数 进行删减的时候是无法同步删减的，会保持原样
    - `在sys.path各路径下存在模块名称冲突`
      * 按照已知的常规导入模块方法，返回的结果是在sys.path中各个路径顺序找到的第一个(第一步的原因)
      * 测试可行，应该也是这样的，不过毕竟样本过少，不能保证稳定性。。
    - `importlib.reload(module_)`语句可以对模块进行热重载(即在代码运行的过程中进行重载，`即时生效`)
    
    - _module   需要导入的模块
    - path      模块所在的路径，可选
    - raise_    导入失败时是否报错，可选
    """
    if path:
        sys_path_temp = list(sys.path)
        sys.path.insert(0, path)
    try:
        module_ = importlib.import_module(".", _module)
        _module_ = importlib.reload(module_)
        if _module != "tools":
            return _module_
    except (ImportError, ModuleNotFoundError) as err:
        if path:
            sys.path = sys_path_temp
        if raise_:
            raise err
        return None


if __name__ == "__main__":
    pass
