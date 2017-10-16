import os
import fnmatch
import re


# 参数 匹配模式，目标文件夹
# return 目标文件的全路径，
def log_find(filepat, top):
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)


# 参数 目标文件全路径list
# return open文件流
def log_opener(filenames):
    for filename in filenames:
        if filename.endswith(r".log"):
            f = open(filename, 'rt')
        if f is not None:
            yield f
    if f is not None:
        f.close()


# 参数 多个文件的open文件流list
# return 一行文本 （一个文件的open文件流 的迭代单位 一行文本）
def log_concatenate(iterators):
    # it 一个文件的open文件流
    for it in iterators:
        yield from it


# 参数 pattern 匹配模式，lines：所有的文本行list
# return 符合的目标行
def log_grep(pattern, lines):
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line


if __name__ == '__main__':
    lognames = log_find('iLNBScreen*', r'C:\temp\test')
    files = log_opener(lognames)
    lines = log_concatenate(files)
    versionlines = log_grep('iLNB: 01', lines)
    for line in versionlines:
        print(line)
