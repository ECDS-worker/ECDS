import xlrd

path = "E:"
file = 'test.xlsx'

# 打开文件
data = xlrd.open_workbook(path + '/' + file)
# 获取表格数目
nums = len(data.sheets())
# for i in range(nums):
#
#     # 根据sheet顺序打开sheet
#     sheet1 = data.sheets()[i]

# 根据sheet名称获取
sheet2 = data.sheet_by_name('test')
nrows = sheet2.nrows   # 行
ncols = sheet2.ncols   # 列
print(nrows, ncols)

# 循环行列表数据
for i in range(nrows):
    print(sheet2.row_values(i))

# 获取单元格数据
# 1.cell（单元格）获取
cell_A1 = sheet2.cell(0, 0).value
print(cell_A1)
# 2.使用行列索引
cell_A2 = sheet2.row(0)[1].value
print(cell_A2)
