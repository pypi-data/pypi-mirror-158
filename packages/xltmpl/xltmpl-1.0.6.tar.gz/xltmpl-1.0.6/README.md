## 功能
本模块基于openpyxl，通过自定义xls/xlsx模板，向模板写入数据，从而保留表格样式，适合固定格式报表导出。

## 安装

```
pip install xltmpl==1.0.6
```

## 快速开始
### 第一步、假设一个xls/xlsx模板的Sheet1设置如下：

| A   | B    | C    | D    | E   |
|-----|------|------|------|-----|
| 1   | name | age  | sex  |     |
| 2   | {{}} | {{}} | {{}} |     |
| 3   |      |      |      |     |
* 第一行是表头
* 第二行全部填充{{}}，然后设置{{}}单元格的格式(如字体、字号、文本颜色、边框、背景等等)，后面的单元格样式都使用该行的样式

### 第二步：往Excel写入数据，可以很方便的写入多种数据类型
```python
# -*- coding: utf-8 -*-
"""
演示xltmpl按模板导出数据
"""
import pandas as pd
from xltmpl.xltmpl import XlTemplate

xlpath_tmpl = 'xlsx_template.xlsx' # xls format is allowed
xlpath_save = 'save.xlsx'

# 指定模板位置，以及写入数据后的新表位置，然后向Excel模板写入数据
with XlTemplate(tmpl_path=xlpath_tmpl, xlpath_save=xlpath_save, place_holder='{{}}') as tmpl:
    # 往Sheet1添加一行数据
    row = ['apple', 'orange', 'banana']
    tmpl.append_row('Sheet1', row)
    
    # 往第一个Sheet天机多行数据
    rows = [
        ['Jason', 'M', 23],
        ['Rose', 'F', 19]]
    tmpl.append_rows(1, rows)
    
    # 往第二个Sheet添加一条记录，其中header_row指定表头位置，style_row指定样式在第几行
    # 添加record时，Excel中有的字段自动放到Sheet对应的列，不存在的字段自动舍弃
    record = {
        'name': 'Micheal',
        'age': 14,
        'sex': 'M',
        'other': '这个字段Sheet中不存在，不会写入Excel'
    }
    tmpl.append_dict(2, record, header_row=1, style_row=2)
    
    # 往第三个Sheet添加一个dataframe
    data = {
        'Name': ['Jason', 'Rose', 'Micheal'],
        'Age': [23, 19, 14],
    }
    df = pd.DataFrame(data)
    tmpl.append_dataframe(3, df)
```
### 关于Excel模板
* xltmpl支持xls和xlsx
* 表头可以不在第一行，不在第一行时，追加数据需指定header_row参数
* 模板最后一行全部填充{{}}
