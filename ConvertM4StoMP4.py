import os
import json
import re
import time

# 读取json文件
def readJson(fileName):
    f = open(fileName, encoding='utf-8')
    setting = json.load(f)
    title = setting['page_data']['download_subtitle']
    return title

# 获取文件列表
def getFileList(file_dir):
    #定义三个列表
    Title = []
    VideoPath = []
    AudioPath = []
    #遍历文件目录
    for root, dirs, files in os.walk(file_dir):
        if ('entry.json' in files):
            Tname = str(root) + '\\entry.json'
            Tname = readJson(Tname)
            Title.append(Tname)
        if ('video.m4s' in files and 'audio.m4s' in files):
            Vpath = str(root) + '\\video.m4s'
            Apath = str(root) + '\\audio.m4s'
            VideoPath.append(Vpath)
            AudioPath.append(Apath)
        if('0.blv' in files):
            Title.pop()
    return [Title, VideoPath, AudioPath]

# 输出mp4文件
def getMP4(title, video_path, audio_path):
    # 生成输出目录
    if not os.path.exists("./output"):
        os.mkdir("./output")
    #循环生成MP4文件
    for i in title:
        #规范文件名
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]") # 匹配不是中文、大小写、数字的其他字符
        reName = i
        reName = cop.sub('', reName)  # 将标题中匹配到的字符替换成空字符
        #开始生成MP4文件
        if not os.path.exists("./output/" + reName + ".mp4"):
            os.system(
                "ffmpeg -i " + video_path[title.index(i)] + " -i " + audio_path[title.index(i)] + " -codec copy ./output/" + reName + ".mp4")
            print("正在合成...")
            print("标题：" + i)
            print("视频源：" + video_path[title.index(i)])
            print("音频源：" + audio_path[title.index(i)])
            time.sleep(1)

print("欢迎使用批量合成M4S工具")
fileDir = str(input("请输入含M4S文件的目录:"))
f = getFileList(fileDir)
getMP4(f[0], f[1], f[2])
print("合成完毕")
