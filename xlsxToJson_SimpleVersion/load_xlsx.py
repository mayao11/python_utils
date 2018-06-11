import os, sys

from openpyxl import Workbook, load_workbook
import json

xlsx_path = "."

def LoadExcel( file_path, file_name ):
    path = os.path.join( xlsx_path, file_path, file_name )
    wb = load_workbook( path )
    return wb

def ReadLines( work_book ):
    ws = work_book.worksheets[0]
    rows = ws.rows
    # 第一行：类型描述行
    desc_row = next(rows)
    # 第二行：列的名称
    name_row = next(rows)

    # 一个表格的所有信息最终保存在output_all里面
    output_all = {}
    # i是行，j是列
    for row in rows:
        # 一行的信息保存在output_row中，最后把它加入到output_all中
        output_row = {}
        for j in range( len(desc_row) ):
            # desc就是类型描述
            desc = desc_row[j].value
            if desc==None or len(desc.strip())==0:
                continue
            desc = desc.strip().lower()

            # col_name是列名称
            col_name = name_row[j].value
            if col_name == None or len(col_name.strip())==0:
                continue
            col_name = col_name.strip()

            # 取出i行j列的数据
            data = row[j].value

            # 根据类型分别处理，注意值为None的情况
            if desc == "int":
                if data == None:
                    output_row[ col_name ] = 0
                else:
                    output_row[ col_name ] = int(data)
            elif desc == "text" or desc == "string":
                if data == None:
                    output_row[ col_name ] = ""
                else:
                    output_row[ col_name ] = data
            elif desc == "float":
                if data == None:
                    output_row[ col_name ] = 0.0
                else:
                    output_row[ col_name ] = float(data)

        # 每行必须有一列叫做id
        _id = int(output_row["id"])
        output_all[ _id ] = output_row

    return output_all

work_book = LoadExcel( ".", sys.argv[1] )
output_all = ReadLines( work_book )

json_text = json.dumps( output_all, indent=4, ensure_ascii=False)
# 到此为止json_text就是我们要的json内容了
# 可以利用重定向，将json写入文件，也可以在这里做一个写入文件的操作

output_name = sys.argv[1].split(".")[0]
output_file = open(output_name+".json", "w", encoding="utf-8")
output_file.write(json_text)
output_file.close()


