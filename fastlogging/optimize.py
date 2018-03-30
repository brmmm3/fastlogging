
import os
import time
import marshal
import py_compile
import ast
import inspect
from types import ModuleType

from . import LOG_DEBUG, LOG_INFO, LOG_WARNING, LOG_ERROR, LOG_FATAL


class OptimizeAst(ast.NodeTransformer):

    def __init__(self, id_, optimize, deoptimize = 0, remove = 0, const2value = False, value2const = False):
        self.id = id_
        self.__const2value = const2value
        self.__value2const = value2const
        self.__level2func = { "LOG_DEBUG" : "debug", "LOG_INFO" : "info", "LOG_WARNING" : "warning",
                              "LOG_ERROR" : "error", "LOG_FATAL" : "fatal" }
        self.__level2value = { "LOG_DEBUG" : LOG_DEBUG, "LOG_INFO" : LOG_INFO, "LOG_WARNING" : LOG_WARNING,
                               "LOG_ERROR" : LOG_ERROR, "LOG_FATAL" : LOG_FATAL }
        self.__value2level = { LOG_DEBUG : "LOG_DEBUG", LOG_INFO : "LOG_INFO", LOG_WARNING : "LOG_WARNING",
                               LOG_ERROR : "LOG_ERROR", LOG_FATAL : "LOG_FATAL" }
        self.__level2optimize = self.__level2dict(optimize)
        self.__level2unoptimize = self.__level2dict(deoptimize)
        self.__remove = set()
        self.__removeLevel = set()
        if remove >= LOG_DEBUG:
            self.__remove.add("debug")
            self.__removeLevel.add("LOG_DEBUG")
        if remove >= LOG_INFO:
            self.__remove.add("info")
            self.__removeLevel.add("LOG_INFO")
        if remove >= LOG_WARNING:
            self.__remove.add("warning")
            self.__removeLevel.add("LOG_WARNING")
        if remove >= LOG_ERROR:
            self.__remove.add("error")
            self.__removeLevel.add("LOG_ERROR")
        if remove >= LOG_FATAL:
            self.__remove.add("fatal")
            self.__remove.add("critical")
            self.__removeLevel.add("LOG_FATAL")

    def __level2dict(self, level):
        level2dict = {}
        if level >= LOG_FATAL:
            level2dict["fatal"] = "LOG_FATAL"
            self.__level2optimize["critical"] = "LOG_FATAL"
        if level >= LOG_ERROR:
            level2dict["error"] = "LOG_ERROR"
        if level >= LOG_WARNING:
            level2dict["warning"] = "LOG_WARNING"
        if level >= LOG_INFO:
            level2dict["info"] = "LOG_INFO"
        if level >= LOG_DEBUG:
            level2dict["debug"] = "LOG_DEBUG"
        return level2dict

    def __compare_args(self, levelName):
        if self.__const2value:
            levelNum = self.__level2value[levelName]
            return ast.Num(n = levelNum), ast.Num(n = levelNum)
        return ast.Name(id = levelName, ctx = ast.Load()), ast.Name(id = levelName, ctx = ast.Load())

    def __levelName_compare_args(self, args):
        try:
            levelName = args.id # e.g. LOG_INFO
            compare, args = self.__compare_args(levelName)
        except:
            levelNum = args.n
            levelName = self.__value2level[levelNum]
            if self.__value2const:
                compare = ast.Name(id = levelName, ctx = ast.Load())
                args = ast.Name(id = levelName, ctx = ast.Load())
            else:
                compare = ast.Num(n = levelNum)
                args = ast.Num(n = levelNum)
        return levelName, compare, args

    def __compare(self, compare):
        return ast.Compare(left = ast.Attribute(
                        value = ast.Name(id = self.id, ctx = ast.Load()),
                        attr = 'level', ctx = ast.Load()),
                    ops = [ ast.LtE() ],
                    comparators = [ compare ])

    def __expr(self, attr, args, body):
        return ast.Expr(value = ast.Call(
                    func = ast.Attribute(
                        value = ast.Name(id = self.id, ctx = ast.Load()),
                        attr = attr, ctx = ast.Load()),
                    args = args,
                    keywords = body.keywords,
                    starargs = body.starargs,
                    kwargs = body.kwargs))

    def visit_If(self, node):
        try:
            if (node.test.left.value.id != self.id) or (node.test.left.attr != "level"):
                return node
            if node.body[0].value.func.value.id != self.id:
                return node
        except Exception as exc:
            return node
        body = node.body[0].value
        attr = body.func.attr
        if attr in self.__remove:
            return None
        levelName, compare, args = self.__levelName_compare_args(node.test.comparators[0])
        if levelName in self.__removeLevel:
            return None
        if attr == "log":
            # if logger.level <= LOG_foo:
            #     logger.log(LOG_foo, ...)
            body_args = body.args[1:]
            level = self.__level2func[levelName] # e.g. LOG_ERROR -> error
            if level not in self.__level2optimize:
                if level in self.__level2unoptimize:
                    # Deoptimize -> remove 'if' and 'log' -> 'foo'
                    return ast.copy_location(self.__expr(level, body_args, body), node)
            # Optimize
            args = [ args ] + body_args
        else:
            # if logger.level <= LOG_foo:
            #     logger.foo(...)
            if attr not in self.__level2optimize:
                if attr in self.__level2unoptimize:
                    # Deoptimize
                    return ast.copy_location(self.__expr(attr, body.args, body), node)
                args = body.args
            else:
                attr = "log"
                args = [ args ] + body.args
        # Optimize
        return ast.copy_location(ast.If(
            test = self.__compare(compare),
            body = [ self.__expr(attr, args, body) ],
            orelse = []), node)

    def visit_Expr(self, node):
        func = node.value.func
        try:
            if func.value.id != self.id:
                return node
        except:
            return node
        attr = func.attr
        if attr in self.__remove:
            return None
        value = node.value
        if attr == "log":
            # logger.log(LOG_foo, ...)
            levelName, compare, args = self.__levelName_compare_args(value.args[0])
            if levelName in self.__removeLevel:
                return None
            value_args = value.args[1:]
            level = self.__level2func[levelName] # e.g. LOG_ERROR -> error
            if level not in self.__level2optimize:
                if level in self.__level2unoptimize:
                    # Deoptimize
                    return ast.copy_location(self.__expr(self.__level2func[levelName], value_args, value), node)
                return ast.copy_location(self.__expr(attr, [ args ] + value_args, value), node)
            # Optimize
            args = [ args ] + value_args
        else:
            # logger.foo(...)
            levelName = self.__level2optimize.get(attr)
            if levelName is None:
                # Deoptimize or unchanged
                return node
            # Optimize
            compare, args = self.__compare_args(levelName)
            attr = "log"
            args = [ args ] + value.args
        # Optimize
        return ast.copy_location(ast.If(
            test = self.__compare(compare),
            body = [ self.__expr(attr, args, value) ],
            orelse = []), node)


def optimize(id_, optimize, deoptimize = 0, remove = 0, const2value = False, value2const = False):

    def optimize_decorator(code):
        tree = OptimizeAst(id_, optimize, deoptimize, remove, const2value, value2const).visit(code)
        return compile(ast.fix_missing_locations(tree), filename = "<function>", mode = "exec")

    return optimize_decorator


def optimize_obj(obj, id_, optimize, deoptimize = 0, remove = 0, const2value = False, value2const = False):
    tree = ast.parse(inspect.getsource(obj))
    tree = OptimizeAst(id_, optimize, deoptimize, remove, const2value, value2const).visit(tree)
    if inspect.ismodule(obj):
        return compile(ast.fix_missing_locations(tree), filename = obj.__file__, mode = "exec")
    module = ModuleType("tempModule")
    module.__dict__.update(globals())
    exec(compile(ast.fix_missing_locations(tree), filename = obj.__name__, mode = "exec"), module.__dict__)
    return getattr(module, obj.__name__)


def optimize_module(obj, id_, optimize, deoptimize = 0, remove = 0, const2value = False, value2const = False):
    tree = ast.parse(inspect.getsource(obj))
    tree = OptimizeAst(id_, optimize, deoptimize, remove, const2value, value2const).visit(tree)
    if inspect.ismodule(obj):
        fileName = obj.__file__
    else:
        fileName = obj.__name__
    return compile(ast.fix_missing_locations(tree), filename = fileName, mode = "exec")


def optimize_file(fileName, id_, optimize, deoptimize = 0, remove = 0, const2value = False, value2const = False):
    tree = ast.parse(open(fileName).read())
    tree = OptimizeAst(id_, optimize, deoptimize, remove, const2value, value2const).visit(tree)
    return compile(ast.fix_missing_locations(tree), filename = module.__file__, mode = "exec")


def write_pyc_file(fileName, code):
    with open(os.path.splitext(fileName)[0] + ".pyc", 'wb') as F:
        F.write('\0\0\0\0')
        py_compile.wr_long(F, long(time.time()))
        marshal.dump(code, F)
        F.flush()
        F.seek(0, 0)
        F.write(py_compile.MAGIC)
