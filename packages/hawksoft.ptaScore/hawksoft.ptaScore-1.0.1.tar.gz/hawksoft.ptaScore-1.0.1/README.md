# hawksoft.patScore command

针对pintia.cn网站教学，生成学生的多次作业成绩总表。

## Installation:

```
pip install hawksoft.patScore
```
## usage:
1. 首先“导出”学生的所有作业（或考试）成绩，并集中存放到一个目录下（这里是tests）.
2. 提供一个excel文件，为学生的点名册(这里是names.xlsx).
3. 调用如下命令，结果将会保存到指定的文件中（这里是scores.xlsx)
```
patScore -n names.xlsx -t tests -o scores.xlsx
```
