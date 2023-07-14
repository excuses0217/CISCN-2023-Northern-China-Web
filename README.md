# CISCN2023-Northern-China-Web
2023 国赛华北赛区线下赛 Web 题，使用Docker环境，欢迎补充

以下都是本人参加比赛从赛场顺走的第一手资料

在赛场上被各位师傅打的落荒而逃，只得回来慢慢研究赛题

![HackPanda](http://intro.suosuodrive.com/HackPanda.jpg)

## 快速开始

```bash
# 运行单个环境，请切换到相应题目目录
cd pysym/docker
# 使用 docker-compose 一键启动环境
docker-compose up -d

# 使用 docker-compose 一键构建所有题目环境镜像
docker-compose build
# 如果你只想构建某个赛题的镜像，你可以在 docker-compose build 命令后面加上题目名
docker-compose build pysym
# 自定义端口运行环境
docker run -d -p 8080:80 pysym:latest
```

## 题目目录

- pysym
- ExifT0ol
- ez_date
- filechecker
- ezruby
- dolphin_haihai（还未完成docker部署，仅上传源码）
