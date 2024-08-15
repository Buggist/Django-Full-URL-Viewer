import os


class RelationTree():
    def __init__(self):
        self.data = {}                                                          # 最终结果
        self.cache = {}                                                         # 缓存数据
    
    def _concat(self, dic1: dict, dic2: dict) -> dict:
        """获得将两个字典连接后的新字典并返回"""
        dic = dic1.copy()
        dic.update(dic2)
        return dic
    
    def add(self, father, value, son):                                          # 添加一条新的映射关系到关系链表
        """
        # father -> 当前文件路径
        # value  -> 当前文件行数
        # son    -> 当前行所指向的文件的路径
        """
        if father in self.cache:
            self.cache[son] = self._concat(self.cache[father], {father: value}) # 每次添加映射，都将所指向最新的路径设置为链表的键，用于下一次索引。
            
        else:
            self.cache[son] = {father: value}
    
    def add_final(self, father, value, son):                                    # 写入一条完整映射链到data
        """
        # father -> 当前文件路径
        # value  -> 当前文件行数
        # son    -> 最终链接到的数据
        """
        if father in self.cache:
            self.data[son] = self._concat(self.cache[father], {father: value})
            
        else:
            self.data[son] = {father: value}
    
      
    
class Writer():
    def __init__(self, filepath: str):
        if os.path.exists(filepath):
            self.file = open(filepath, "r+", encoding="utf=8")
        else:
            self.file = open(filepath, "w+", encoding="utf=8")
        self.indent_level = 0

    def define_var(self, 
        var_name: str,
        var_value: str,
    ) -> None:
        content = var_name + " = \"" + var_value + "\"\n"   
        self.file.writelines(" " * self.indent_level * 4)                       # 写入缩进
        self.file.writelines(content)                                           # 写入变量定义
        
    def define_dict(self,
        dict_name: str,
        dict_value: dict,
    ) -> None:
        def q(v: any) -> any:
            # 在写入前给字符串加引号，防止写入后引号丢失
            if type(v) is str:
                return "\"%s\"" % v
            else:
                return str(v)
        
        # 写入字典头
        content = dict_name + " = " + "{\n"
        self.file.writelines(" " * self.indent_level * 4)                       # 写入缩进
        self.file.writelines(content)                       
        self.indent_level += 1
        
        # 写入字典的键值对
        for k,v in dict_value.items():  
            content = q(k) + ": " + q(v) + ",\n"
            self.file.writelines(" " * self.indent_level * 4)                   # 写入缩进
            self.file.writelines(content)
        
        # 写入字典尾
        self.indent_level -= 1
        self.file.writelines(" " * self.indent_level * 4)                       # 写入缩进
        self.file.writelines("}\n")
        
    def define_list(self,
        list_name: str,
        list_value: str,
        has_name: bool = True,
        line_break: bool = True,
    ) -> None:
        """
        # ------------------参数说明--------------------
        # list_name  -> 列表变量的名称
        # list_value -> 列表变量的值
        # has_name   -> 列表是否有变量名，默认是。
        # line_break -> 列表的每个元素是否独占一行，默认是。
        # --------------------------------------------
        """
        def q(s: str) -> str:
            return "\"%s\"" % s
        
        # 判断是否有列表名 - 写入列表头
        if has_name:                                                            # 如果有列表名
            # 写入列表头
            if line_break:                                                          # 如果换行定义
                content = list_name + " = " + "[\n"
                self.file.writelines(" " * self.indent_level * 4)                       # 写入缩进
                self.file.writelines(content)                                           # 写入内容
                self.indent_level += 1
            else:                                                                   # 如果定义在同一行
                content = list_name + " = " + "["
                self.file.writelines(content)                                           # 写入内容
            
        else:                                                                   # 如果没有列表名
            # 写入列表头
            self.file.writelines(" " * self.indent_level * 4)                       # 写入缩进
            if line_break:                                                          # 如果换行定义
                content = "[\n"
                self.indent_level += 1
            else:                                                                   # 如果定义在同一行
                content = "["
            self.file.writelines(content)                                           # 写入内容
        
        # 写入列表元素
        for v in list_value:
            if type(v) is str:                                                  # 如果元素是字符串
                if line_break:                                                      # 如果换行定义
                    self.file.writelines(" " * self.indent_level * 4)                   # 写入缩进
                    self.file.writelines("%s,\n" % q(v))                                # 写入内容
                else:                                                               # 如果定义在同一行
                    self.file.writelines("%s, " % q(v))                                 # 写入内容
                    
            elif type(v) == list:                                               # 如果元素是列表
                self.define_list(None, v, has_name=False, line_break=False)         # 递归调用
                
            else:                                                               # 如果元素是其他类型
                if line_break:                                                      # 如果换行定义
                    self.file.writelines(" " * self.indent_level * 4)                   # 写入缩进
                    self.file.writelines("%s,\n" % v)                                   # 写入内容
                else:                                                               # 如果定义在同一行
                    self.file.writelines("%s, " % v)                                    # 写入内容
        
        # 写入字典尾
        if line_break:                                                          # 如果换行定义
            self.indent_level -= 1
            self.file.writelines(" " * self.indent_level * 4)                       # 写入缩进
        if has_name:                                                            # 如果有变量名
            self.file.writelines("]\n")                                             # 写入结尾
        else:                                                                   # 如果没有变量名
            self.file.writelines("],\n")                                            # 写入结尾
    
    def close(self) -> None:
        self.file.close()
        
        
class Reader():
    """
    # 此对象仅为Demo版本，仅提供对当前项目环境的支持。
    # 在读取urls.py时，不考虑完整的列表读取语法和注释处理，
    # 仅识别urlpatterns变量及其后以url开头的行中的数据。
    # 受限于脑容量，完整的urls.py语法支持将在后续以迭代更新的方式陆续添加。
    """
    def __init__(self, project_name):
        self.project_name = project_name
        self.main_urls = {}                                                     # 键为页面路由，值为文件路由与路由别名（可选）构成的元组。
        self.parent_urls = {}                                                   # 键为子路由urls.py文件的路径，值为该文件的父路由。
        self.current_dir = os.getcwd()                                          # 获取当前目录（路由管理器根目录）
        self.main_dir = os.path.dirname(self.current_dir)                       # 获取项目根目录
        self.relation_tree = RelationTree()                                     # 关系树字典，用于创建关系树文件，用于将对总路由表的修改自动逐一应用到所有分路由表。
        self.urls_path_list = []                                                # 所有urls.py文件的路径的列表
        
    def read_path(self, current_dir = None) -> None:
        if not current_dir:                                                     # 如果不传入读取的目录
            current_dir = self.main_dir                                             # 读取当前目录（根目录）
        items = os.listdir(current_dir)                                         # 获得当前目录的内容表
        
        # 1 - 读取项目主目录
        if self.project_name in items:
            main_path = os.path.join(current_dir, self.project_name)
            self.read_path(main_path)                                           # 读主目录，递归调用自身
            
        # 2 - 读取当前目录的urls.py
        if "urls.py" in items:
            urlspy_path = os.path.join(current_dir, "urls.py")
            self.read_file(urlspy_path)                                         # 读urls.py文件
            self.urls_path_list.append(urlspy_path)                             # 将文件路径写入urls_path_list，用于存储下来，将来反查该表以应用路由更改。
            
        # 3 - 寻找并读取子目录
        for item in items:
            item_path = os.path.join(current_dir, item)
            if os.path.isdir(item_path):                                        # 如果对象是子目录
                if item_path[-4:] == ".git":                                        # 忽略.git目录
                    continue
                self.read_path(item_path)                                           # 读对象目录，递归调用自身。
    
    def read_file(self, filepath) -> None:
        urls_file = open(filepath, "r+", encoding="utf=8")
        flag = True                                                             # flag用于在找到变量名后跳过对"urlpatterns"的识别，提高性能。
        line_count = 0                                                          # 记录当前读取的行号
        while content:= urls_file.readline():
            line_count += 1
            if flag:                                                            
                if "urlpatterns" in content.lstrip()[:11]:
                    flag = False
            elif "url" in content.lstrip()[:3]:
                self.read_line(content, filepath, line_count)
            else:
                continue
        
    def read_line(self, 
        content: str,
        src_file: str,
        line_count: str, 
    ) -> None:
        """
        # 此路由管理工具只对urls.py的内容以字符串形式进行读写
        # 因此该函数不需要解释文件中的各种对象、正则、方法。
        # 只需要识别urls.py数据行中的三个纯字符串内容--->目录路径、页面路径、页面别名。
        # ----------------------------------------------
        # 如果识别到完整页面路径，即页面路径不包含"include("，
        #   直接将三个内容编组写入总路由表self.main_urls。
        # 如果识别到不完整页面路径，即页面路径包含"include("，
        #   将这一行内容编组保存到中间路由表self.parent_urls，
        #   并在后续更深层的路由检索中将中间路由与子路由衔接。
        # 递归重复这一步骤直到完成整个项目的路由检索。输出完整的项目总路由表。
        """
        def translate_path(path: str) -> str:
            """
            # 将以.分割的路径转为以/分割的路径
            # 为urls添加.py后缀
            # 将py模块路径的path转为合法的文件路径
            """
            path = path.replace(".", "\\") + ".py"
            return path
            
        def extract(content: str, l="(", r=")") -> str:
            """
            # 取出字符串最外层括号内的内容
            # if判断是为了忽略content不包含右边界符号时的情况
            """
            content = content[content.find(l)+1:]                               # 提取第一个左括号后的内容，且忽略content不包含左边界符号时的情况
            if content.rfind(r) != -1:
                content = content[:content.rfind(r)]                            # 提取倒数第一个右括号前的内容
            return content
        
        def url_format(content: str) -> str:
            """
            # 将urls.py文件中的页面路由转换为显示在浏览器中的格式
            # 删除字符串头部连续的特殊字符，包括字符串前缀中的r。
            """
            index = 0
            has_r = 0
            for char in content:
                if char.isalpha() or char.isdigit():
                    if char == "r":
                        has_r = 1
                        continue
                    break
                else:
                    if has_r: has_r = 2
                    index += 1
            if has_r == 2:
                index += 1
            content = content[index:]
            
            # 删除字符串末尾的引号
            index = 0
            for char in content[::-1]:                                          # 反向遍历字符串
                if char == "'" or char == '"':
                    index += 1
                else:
                    break
            content = content[:-index]
            return content
        
        parent_url = ""
        if src_file in self.parent_urls:
            parent_url = self.parent_urls[src_file]
        content = extract(content)
        url_info = content.split(",")
        if len(url_info) <= 2: url_info.append(None)                            # 如果路由没有别名，则别名以None补齐列表长度。
        # url_info中的元素依次为url_page, url_file, <url_name>
        
        if url_info[1].lstrip()[:8] == "include(":                              # 如果为中间路由（即不指向视图文件，而是指向其它urls.py）。
            url_file = extract(url_info[1])                                         # 取出include()括号中的内容
            url_file = extract(url_file, '"', '"')                                  # 取出双引号内的内容（如果有双引号）
            url_file = extract(url_file, "'", "'")                                  # 取出单引号内的内容（如果有单引号）
            url_file_path = translate_path(url_file)
            url_file_path_abs = os.path.join(self.main_dir, url_file_path)          # 获取ulrs.py的绝对路径
            url_page_full = parent_url + url_format(url_info[0])                    # 包含了所有父路由的页面路由
            self.parent_urls[url_file_path_abs] = url_page_full                     # 将当前完整中间路由加入中间路由表
            
            self.relation_tree.add(src_file, line_count, url_file_path_abs)     # 更新关系树字典缓存
            
        else:                                                                   # 如果为终点路由（即指向视图函数）
            url_file = url_info[1]
            url_page_full = parent_url + url_format(url_info[0])                    # 包含了所有父路由的完整页面路由
            self.main_urls[url_page_full] = (url_file, url_info[2])                 # 将当前完整终点路由加入项目总路由表
            
            self.relation_tree.add_final(src_file, line_count, url_page_full)   # 写入关系树字典
            




if __name__ == "__main__":
    reader = Reader("kggroup")
    reader.read_path()
    
    writer = Writer("main_urls.py")
    writer.define_dict("main_urls", reader.main_urls)
    writer.define_dict("relation_tree", reader.relation_tree.data)
    writer.define_list("urls_path_list", reader.urls_path_list)
    writer.close()
    print("Done!")


