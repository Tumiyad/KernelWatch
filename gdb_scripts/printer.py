#todo

#prompt
"""
python
帮我写一个Printer类，
类变量：
type_string：string类型，代表对应的类型
shorts：代表short模式print需要输出的字段
tests：代表test模式print需要输出的字段
value：代表要
type：gdb type类型
初始化：
接收一个gdb变量
方法：
print：参数：target 待打印对象； all 打印所有字段；short打印 shorts中包含字段；tests，打印tests中包含字段
"""




import gdb

class Printer:
    # 类变量
    type_string = ""  # 代表对应的类型
    shorts = []        # short模式print需要输出的字段
    tests = []         # test模式print需要输出的字段
    value = None       # 要打印的值
    type = None        # gdb type类型

    def __init__(self, gdb_variable):
        """
        初始化Printer对象，接收一个gdb变量
        """
        self.value = gdb_variable
        self.type = gdb_variable.type
        self.type_string = str(self.type)

        # 根据类型初始化 shorts 和 tests 字段
        if self.type.code in [gdb.TYPE_CODE_STRUCT, gdb.TYPE_CODE_UNION]:
            # 获取所有字段名
            fields = [field.name for field in self.type.fields()]
            # 这里可以根据实际需求设置 shorts 和 tests
            # 示例：假设 short 模式打印前两个字段，test 模式打印接下来的两个字段
            self.shorts = fields[:2] if len(fields) >= 2 else fields
            self.tests = fields[2:4] if len(fields) >= 4 else fields
        else:
            # 如果不是结构体或联合体，清空 shorts 和 tests
            self.shorts = []
            self.tests = []

    def print(self, target, all=False, short=False, tests=False):
        """
        打印方法
        参数：
            target: 待打印对象 (gdb.Value)
            all: 是否打印所有字段
            short: 是否打印 shorts 中包含的字段
            tests: 是否打印 tests 中包含的字段
        """
        if not isinstance(target, gdb.Value):
            print("目标对象必须是 gdb.Value 类型")
            return

        if all:
            self._print_all_fields(target)
        else:
            if short:
                self._print_fields(target, self.shorts, mode="short")
            if tests:
                self._print_fields(target, self.tests, mode="test")

    def _print_all_fields(self, target):
        """
        打印所有字段
        """
        if self.type.code not in [gdb.TYPE_CODE_STRUCT, gdb.TYPE_CODE_UNION]:
            print(target)
            return

        for field in self.type.fields():
            field_name = field.name
            field_value = target[field_name]
            print(f"{field_name}: {field_value}")

    def _print_fields(self, target, fields, mode=""):
        """
        打印指定的字段
        """
        if not fields:
            print(f"No fields defined for {mode} mode.")
            return

        print(f"--- {mode.capitalize()} Mode ---")
        for field_name in fields:
            try:
                field_value = target[field_name]
                print(f"{field_name}: {field_value}")
            except gdb.error as e:
                print(f"无法获取字段 '{field_name}': {e}")
        print("-------------------------")

# 示例用法
# 假设你在 GDB 中有一个变量 `my_struct`，你可以这样使用 Printer 类：

# (gdb) python
# my_var = gdb.parse_and_eval("my_struct")
# printer = Printer(my_var)
# printer.print(my_var, all=True)       # 打印所有字段
# printer.print(my_var, short=True)     # 打印 shorts 中的字段
# printer.print(my_var, tests=True)     # 打印 tests 中的字段
# end
