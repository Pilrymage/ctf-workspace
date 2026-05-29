class F:
    """支持参数绑定和首位传参的超级管道"""
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._is_right = False
        self._is_lazy = False

    def __ror__(self, other):
        if self._is_right:
        # 核心逻辑：当执行 "data | F" 时
        # 将左侧的 data (other) 强制作为 func 的第一个参数，拼接上提前捕获的参数
            return self.func(*(self.args + (other,)), **self.kwargs)
        else:
            return self.func(other, *self.args, **self.kwargs)

    def __pos__(self):
        """触发器：单目 + 运算符，将当前算子转化为一个惰性闭包管道的起点"""
        new_f = F(self.func, *self.args, **self.kwargs)
        new_f._is_right = self._is_right
        new_f._is_lazy = True  # 开启传染模式
        return new_f

    def __or__(self, other):
        """
        正向管道：当 F 算子在 | 左侧时触发 (例如： +F1 | F2)
        在这里实现向右侧的“传染”和“函数串联”。
        """
        if self._is_lazy:
            # 确保右侧也是个管道，如果只是原生函数(如 len, list)，自动包一层
            other_f = other if isinstance(other, F) else F(other)
            
            # 闭包生成：将左侧和右侧的逻辑串联
            def _lazy_chain(data):
                # 数据先流过左侧(self)，再流过右侧(other_f)
                step1 = self.__ror__(data)
                return other_f.__ror__(step1)
                
            new_f = F(_lazy_chain)
            new_f._is_lazy = True  # 完美传染给下一个！
            return new_f
        
        return NotImplemented

    def __call__(self, *args, **kwargs):
        """区分模式：是参数绑定，还是执行闭包？"""
        if self._is_lazy:
            # 如果它已经被 + 固化成了闭包管道，直接调用就是在执行管道！
            # 兼容 map/filter 等高阶函数传入单个参数的情况
            if len(args) == 1 and not kwargs:
                return self.__ror__(args[0])
            return self.func(*args, **kwargs)

        # 否则，保持原有的参数绑定逻辑
        new_f = F(self.func, *(self.args + args), **{**self.kwargs, **kwargs})
        new_f._is_right = self._is_right
        return new_f
        

    @classmethod
    def R(cls, func, *args, **kwargs):
        """快捷构造器：创建一个 APL 交换模式（末位插值）的管道算子"""
        instance = cls(func, *args, **kwargs)
        instance._is_right = True
        return instance

    def __repr__(self):
        func_name = getattr(self.func, '__name__', str(self.func))
        if "lambda" in func_name: func_name = "<lambda>"
        args_str = ", ".join(map(repr, self.args))
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in self.kwargs.items())
        bound_str = ", ".join([p for p in [args_str, kwargs_str] if p])
        
        # 打印时清晰区分是 F 还是 F.R
        prefix = "F.R" if self._is_right else "F"
        return f"{prefix}<{func_name}>(bound: ({bound_str}))"

    def __matmul__(self, other):
        """
        重载 @ 运算符实现函数组合：f @ g 转换为 f(g(x))
        完美保留外层 (self) 和内层 (other) 的所有参数及侧向状态。
        """
        def _composed(data):
            # 1. 先让数据流经右侧的 g (inner)
            if hasattr(other, '__ror__'):
                inner_result = other.__ror__(data)
            elif callable(other):
                inner_result = other(data)
            else:
                raise TypeError("组合算子的右侧必须是可调用的对象或管道")
            
            # 2. 将内层的结果，喂给左侧的 f (outer)
            # 这里直接调用 self.__ror__，完美继承 f 的预绑参数和 F.R 逻辑！
            return self.__ror__(inner_result)
            
        return F(_composed)
    
    def __invert__(self):
        """
        重载 ~ 运算符，实现 Thread-First (F) 和 Thread-Last (F.R) 的瞬间翻转
        """
        # 创建一个继承当前所有参数的新 F 实例
        new_f = F(self.func, *self.args, **self.kwargs)
        # 将方向标志位取反
        new_f._is_right = not self._is_right
        return new_f
    
    @property
    def slash(self):
        """APL 副词 /：将一个二元函数转化为对整个列表的 Reduce 聚合算子"""
        import functools
        return F(lambda iterable: functools.reduce(self.func, iterable))
    
    @property
    def outer(self):
        """APL 连词 ∘.：计算二元函数的外积矩阵"""
        return F(lambda x, y: [[self.func(i, j) for j in y] for i in x])
      
class Slicer:
    """管道切片助手"""
    def __getitem__(self, item):
        # item 有可能是 slice 对象、整数、元组（多维），甚至是布尔数组
        # 我们把它原封不动地交给被管道传入的数据
        return F(lambda data: data[item])

# 实例化为一个简短的变量名 S
S = Slicer()
gets = lambda x: S[x]

def tee(branch_pipe, reference = False):
    """
    Bash 风格 tee 算子。
    允许传入一个完整的 F 管道（或普通函数），并在深拷贝的数据支流上执行它，而不影响主数据流。
    """
    def _tee_logic(data):
        if(reference == True):
            return data
        try:
            import copy
            branch_data = copy.deepcopy(data)
        except Exception:
            # 容错：如果遇到无法深拷贝的对象（如 socket 句柄），退化为普通引用
            branch_data = data

        branch_pipe(branch_data)

        # 3. 主干继续：原样返回原始数据
        return data

    # 返回一个新的 F 算子，完美融入主管道
    return F(_tee_logic)
  
def DefaultR(func, *default_args, **default_kwargs):
  """
  智能默认参数构造器：
  如果不加括号，直接使用 default_args；
  如果加了括号传入新参数，则完全丢弃默认参数，直接替换。
  """
  class _DefaultOperator(F):
      def __init__(self):
          # 初始化时，乖乖带上默认参数 (比如 "")
          super().__init__(func, *default_args, **default_kwargs)
          self._is_right = True  # 保持 APL 插入末尾的特性

      def __call__(self, *args, **kwargs):
          # 核心魔法：当用户执行 join(".") 时拦截它！
          # 我们丢弃之前的 default_args，用传入的 args 实例化一个【标准的】 F 对象
          new_f = F(self.func, *args, **kwargs)
          new_f._is_right = True
          return new_f
          
  return _DefaultOperator()

class Matched:
    """内部保护壳：标记数据已经匹配成功，短路后续所有 guard"""
    def __init__(self, value):
        self.value = value

def when(condition, action):
    """
    OCaml 风格的模式匹配守卫
    """
    def _route(data):
        # 1. 核心短路逻辑：如果上游已经匹配成功，原样放行保护壳，跳过判断！
        if isinstance(data, Matched):
            return data
        
        # 统一执行器（兼容常规函数和 F 管道）
        def _execute(pipe, val):
            if hasattr(pipe, '__ror__'):
                return pipe.__ror__(val)
            elif callable(pipe):
                return pipe(val)
            return pipe # 支持直接返回常量

        # 2. 判断当前条件 (类比 OCaml 的 when)
        if _execute(condition, data):
            # 匹配成功！执行动作，并套上保护壳
            return Matched(_execute(action, data))
        
        # 3. 匹配失败，让原始数据继续往下掉 (Fall-through)
        return data

    return F(_route)

default = F(lambda data: data.value if isinstance(data, Matched) else data)