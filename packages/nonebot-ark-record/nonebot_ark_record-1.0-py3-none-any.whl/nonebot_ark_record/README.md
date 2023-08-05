# **nonebot_ark_record**
欢迎使用明日方舟抽卡分析nonebot插件 beta1.0

## **插件部署说明**
本插件基于python3.8开发，还未在pip上发布，主要依赖项包括：

- numpy
- matplotlib
- PIL
- sqlite3

本插件依赖于sqlite数据库，在Ubuntu环境下无需额外配置；在windows下，参考网络资源安装sqlite数据库后即可，无需配置数据库环境

如需修改数据库文件名称，可以修改 `ark/ark_setting.py` 中的 `arkgacha_db_path`项

当前版本不支持自动更新卡池信息及干员头像资源。如果有新增干员，可以在PRTS下载干员头像，参照`resource/profile`中的命名规则命名。如果没有可用头像，将以海猫头像代替

如果有新增限定卡池,需要修改`pool_info.json`文件

## **插件部署方法**
在bot.py文件夹下

`git clone https://github.com/zheuziihau/nonebot_arkgacha_record`


## 插件使用方法：

### **token设置**

每个用户第一次使用时，需要先设置token。

**token获取方法**：在官网登录后，复制以下网址中的内容

**token设置方法**：使用插件命令`方舟抽卡token 你的token`
或`方舟寻访token 你的token`进行设置
如：
此外，建议间隔较长时间使用时，再次使用上述命令设置token
### **寻访记录分析**

设置好token后，直接使用`方舟抽卡分析`或`方舟寻访分析`即可

还可以使用`方舟抽卡分析 数字`，分析最近一定抽数的寻访情况

如`方舟抽卡分析 100`分析最近100抽的情况

### **获取帮助**
使用`方舟寻访帮助`或`方舟抽卡帮助`命令，可以获取插件帮助

### **其他功能**
使用`随机干员`命令，随机给出一张干员头像

## **未来更新计划**

- 支持B服寻访记录分析
- 支持异步
- 自动更新卡池信息及资源
- 卡池记录导出

## **参考资料**
作图代码参考于

[nonebot-plugin-gachalogs](https://github.com/monsterxcn/nonebot-plugin-gachalogs)

[nonebot_plugin_gamedraw](https://github.com/HibiKier/nonebot_plugin_gamedraw)

## **开发人员信息**
本人

部分美术资源（待更新）及需求设计由[@Alnas1](https://github.com/Alnas1)提供