import tkinter
import random
import numpy as np

# 生成随机数组
gameArr = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])


def ranNum():
    i = random.randrange(4)
    j = random.randrange(4)
    if random.randrange(10) < 8:
        num = 2
    else:
        num = 4
    if gameArr[i][j] == 0:
        gameArr[i][j] = num
    else:
        ranNum()


for x in range(2):
    ranNum()

print(gameArr)


# 滑动方法
def swap(var, arr):
    isColumn = False    # 判断是否是上下滑动
    if var == 2 or (var == -2):     # 如果为上下的，则转换var. 结果：上同左为1；下同右的为-1；并进行数组转置
        var = int(var / 2)
        arr = arr.transpose()
        isColumn = True

    def change(n):      # 转换索引数，var=-1的，n转成(n + 1) * -1，即右向左索引的数；var=1的，n不变
        if var == -1:
            n = (n + 1) * -1
        return n

    for i in range(4):
        tempArr = []
        for j in range(4):
            if arr[i][j]:
                tempArr.append(arr[i][j])       # 提取一行中不等于0的数，并组成新的一行数组
        for n in range(len(tempArr)):
            if n < len(tempArr) - 1:
                n = change(n)
                if tempArr[n] == tempArr[n + var]:    # 判断该数与右（左）边的数是否相等，相等则该数乘2，并删掉右（左）边的数
                    tempArr[n] = tempArr[n] * 2
                    del tempArr[n + var]
            else:
                break
        for l in range(4):      # 将处理后的4个tempArr重组gameArr
            if l <= len(tempArr) - 1:
                arr[i][change(l)] = tempArr[change(l)]
            else:
                arr[i][change(l)] = 0
    if isColumn:
        arr = arr.transpose()       # 上下的滑动的，转置转回


# 获取当前分数
def getMarks():
    marks = 0
    for i in range(4):
        for j in range(4):
            marks += gameArr[i][j]
    # 显示分数
    label_now.config(text="Goal:" + "\n%d" % (marks))
    return marks


# 获取最高分数
def theBestGoal(nowMarks):
    path = r'F:\Python Project\Hello World\BestGoal.txt'
    file = open(path, "r")
    maxMarks = max(int(file.read()), nowMarks)
    file.close()
    with open(path, "w+") as f:
        f.write("%d" % (maxMarks))
    # 显示最高分
    label_best.config(text="Best:" + "\n%d" % (maxMarks))


# 是否失败
def isFailed():
    n = 0
    global gameArr
    for i in [-1, 1, -2, 2]:    # 对gameArr进行预判，上下左右测试，如果都不发生变化，则失败
        copiedArr = gameArr.copy()
        swap(i, copiedArr)
        if np.array_equal(copiedArr, gameArr):
            n += 1
    if n == 4:
        # 失败后的方法
        gameArr = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        for x in range(2):
            ranNum()
        getMarks()
        label_notice.config(text="Game Over！", fg="red")
        return True
    return False


# 显示数组
def arrDisplay():
    showArr = "\n\n"
    for x in range(4):
        for y in range(4):
            showArr += "  %d  " % (gameArr[x][y])
        showArr += "\n\n"
    gameArea.config(text=showArr)


# 主方法
def func(var):
    # 清空失败提示信息
    label_notice.config(text="")
    # 滑动
    swap(var, gameArr)
    # 得到当前分数，并判断最高分数
    theBestGoal(getMarks())
    # 判断是否失败
    if not isFailed():
        # 未失败，则生成新数字
        ranNum()
    # 显示数组
    arrDisplay()


# 界面
win = tkinter.Tk()
win.title("2048")
win.geometry("500x500+400+200")

# 数组显示区
gameArea = tkinter.Label(win, height=10, width=20, font=("黑体", 20))
arrDisplay()
gameArea.place(x=50, y=50)

# 最高分显示
label_best = tkinter.Label(win, font=("黑体", 16), justify="left")
theBestGoal(0)
label_best.place(x=395, y=50)

# 得分显示
nowNum = '0'
label_now = tkinter.Label(win, text="Goal:" + "\n" + nowNum, font=("黑体", 16), justify="left")
label_now.place(x=395, y=120)

# 失败信息提示
label_notice = tkinter.Label(win, text="")
label_notice.place(x=395, y=200)

# 按键
buttonLeft = tkinter.Button(win, text="<—", command=lambda: func(1))
buttonLeft.place(x=145, y=360)

buttonUp = tkinter.Button(win, text=" /\\ ", command=lambda: func(2))
buttonUp.place(x=180, y=320)

buttonRight = tkinter.Button(win, text="—>", command=lambda: func(-1))
buttonRight.place(x=210, y=360)

buttonDown = tkinter.Button(win, text=" \\/ ", command=lambda: func(-2))
buttonDown.place(x=180, y=395)

win.mainloop()