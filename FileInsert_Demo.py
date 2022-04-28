# 在文档匹配到的位置插入字符，并写入新文件
import re
from abc import ABCMeta,abstractmethod

# 工厂接口
class InserPort(metaclass=ABCMeta):
    @abstractmethod
    def InsertStr(self,match,behind):
        pass

class FileInsert(InserPort):
    def InsertStr(self, match, behind):
        with open(r"./DataLoad/requirement.txt", 'r+', encoding='utf-8') as f:
            for line in f:
                if re.search(match, line) is not None:
                    m = re.search(match, line).span()[0]     # 取第1个匹配符的下标
                    li = list(line)
                    li.insert(m+1, behind)      # 在 m 后插入指定内容
                    S = ''.join(li)             # print(S)
                    # 重新生成一个txt，防止污染源文件
                    fb = open("./DataLoad/Require.txt", 'a+', encoding='utf-8')
                    fb.write(S);    fb.close()

if __name__ == '__main__':
    FileInsert().InsertStr(match='=', behind='*#000#*')

