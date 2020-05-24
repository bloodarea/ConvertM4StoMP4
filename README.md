<h1 align = center>批量合成bilibili的m4s缓存文件为MP4格式</h1>
<font size = 4>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;众所周知，B站是一个学习网站，我常常在B站看一些教程视频，但是有时候没有网络就看不了了，于是我打算把教程都缓存下来看，不得不说，B站的缓存速度还是相当快的，缓存好以后，当我找到缓存目录的时候，发现缓存的文件音画是分离的，我尝试了用格式工厂的视频混流功能，虽然能够实现m4s文件合成为mp4文件，但是不能做到批量合成，需要一个个拖入音频和视频M4S文件，于是我就用python写了一个批量合成m4s文件的工具，通过循环调用ffmpeg中的命令合成MP4文件。</font>

首先需要安装ffmpeg
ffmpeg下载地址：[https://ffmpeg.zeranoe.com/builds/](https://ffmpeg.zeranoe.com/builds/)
解压好下载的压缩包后，再将bin目录加入Path环境变量中
按Win+R 运行 输入cmd 在弹出的框框中输入 ffmpeg ，如果没有出现既不是内部或外部命令之类的话就是安装成功了

先将手机上的缓存目录复制到电脑上
一般B站的缓存目录位于：/Android/data/tv.danmaku.bili/download

再打开工具将缓存目录的路径复制到工具中敲回车，将自动扫描下载目录，并将生成的mp4文件放在工具的同级的output目录下。

已编译的EXE可执行文件：[链接: https://pan.baidu.com/s/1zd0RZ5cYjYWo7v89fK1OPQ 提取码: quzw](https://pan.baidu.com/s/1zd0RZ5cYjYWo7v89fK1OPQ)

展示：
![展示](https://img-blog.csdnimg.cn/20200523224607601.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzI1OTY1MTY1,size_16,color_FFFFFF,t_70)
![展示](https://img-blog.csdnimg.cn/20200523224621937.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzI1OTY1MTY1,size_16,color_FFFFFF,t_70)

源码：
```python
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

```
