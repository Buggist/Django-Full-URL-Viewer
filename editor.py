from dataclasses import dataclass

from main_urls import *


@dataclass
class AURL():
    """通过字符串提取的，Django - URL对象。"""
    page_url: str
    file_url: str
    name: str
    level_names: set = set()
    level_name_head: str = ""
    
    def __post_init__(self):
        cache = page_url.split("/")
        level_name_head = cache.pop(0)
        level_names = set(cache)


@dataclass
class URLManager():
    """
    路由操作器对象--
        读取"main_urls.py"
        -----------------
        1.修改路由层级名称 应用到整个项目
        2.修改指定页面路由的Django别名
    """
    main_urls: dict
    relation_tree: dict
    urls_path_list: list
    
    level_name_set: set = set()
    
    def __post_init__(self):
        self._get_level_name_list()
    
    def _get_level_name_list(self):
        for url in main_urls:
            level_name_set.update(url.split("/"))
            
    def _name_replacer(self, content: str, name: str) -> str:
        content.rstrip()
        content.rstrip(',')
        content = content.split(',')
        content[-1] = "new='%s'" % name
        
        return ','.join(content)
    
    def alter_level_name(self, original: str, new: str) -> None:
        """修改路由层级的名称，例如"grand/father/son/"中的grand、father和son。"""
        if original not in self.level_name_set:
            print("路由层级名称original不存在 - alter_level_name(self, original, new):")
            raise()
        else:
            for path in urls_path_list:
                with open(path, "r", "utf-8") as f:
                    content = f.read()
                    content.replace("/%s/" % original, "/%s/" % new)            # 当替换的层级名称不为根层级名称
                    content.replace("'%s/" % original, "'%s/" % new)            # 当替换的层级名称为根层级名称
                    content.replace('"%s/' % original, '"%s/' % new)            # 当替换的层级名称为根层级名称
                with open(path, "w", "utf-8") as f:
                    f.write(content)
    
    # 暂时废弃 - 本意图为实现对单页面路由的三项属性的自由修改
    # def alter_page_url(self, original: str, new: str) -> None:
        # for file_path, line_num in self.relation_tree[original].items():
            # with open(file_path, "r+", "utf-8") as file:
                # lines = file.readlines()
                # if line_num >= 0 and line_num < len(lines):
                    # lines[line_num] = new_content + "\n"
            
    def alter_url_name(self, page_url: str, name: str) -> None:
        """修改指定页面路由在Django中的别名"""
        path, line_num = self.relation_tree[pag_url].popitem()
        with open(path, "r+", "utf-8") as file:
            lines = file.readlines()
            if line_num >= 0 and line_num < len(lines):
                lines[line_num] = self._name_replacer(lines[line_num])
            else:
                print("不合法的行号:'%s'" % line_num)
                raise()
            file.seek(0)
            file.writelines(lines)
        
        
        
if __name__ == "__main__":
    
    manager = URLManager(main_urls, relation_tree, urls_path_list)
        
        
        
        
        
                    
            
