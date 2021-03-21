# SuperManCheck
Maya Inside Virus Scanner and Fixer, Support Configure File, Scene File, Reference File and Batch.
It use ban_word_list to check file operation in script node (mel and python) to detect, you can add your own word by modify the ban_word_list in SuperManCheck.py

Since it loads all content inside Maya, better change viewport to content browser and close all node panel, so the viewport wont update and speed it up a bit.

Maya病毒扫描清理工具，支持本地配置文件扫描清理，安全打开Maya文件并设置好动画时间轴，指定目录批量扫描清理文件（MA，MB），包括自动修复Reference文件。
它是利用ban_word_list禁用的文件读写操作来检查script node (mel and python), 你也可以在ban_word_list里增加其他不常见词汇来拓展SuperManCheck.py

因为它是开Maya文件来检查的，所以最好把视窗和节点窗口都隐藏，这样起码开的时候稍微快点。

It supports 普天同庆，贼健康和其他mel python的读写病毒

![SuperManCheck_v1.9_en.png](notes/SuperManCheck_v1.9_en.png?raw=true)
![SuperManCheck_v1.9_cn.png](notes/SuperManCheck_v1.9_cn.png?raw=true)

# Install SuperManCheck

Drag the install.mel to Maya viewport to install it on the current shelf.

把install.mel文件拖入Maya视窗界面即可把它安装到当前工具栏，Language里切换语言

# Use Together with puTianTongQingScannFolderEN

puTianTongQingScannFolderEN supports faster MA file scan, but can't deal with reference file, it is best to use puTianTongQingScannFolderEN as a Root scanner for MA files. 

puTianTongQingScannFolderEN 配合使用，但puTianTongQingScannFolderEN不支持Reference文件和MB文件，只适合快速的MA根目录全屏扫描
https://github.com/shiningdesign/puTianTongQingScannFolderEN

# Update Notes:

v1.9: (2021.03.16)
  * better local config check

v1.6: (2021.03.09)
  * add method option
  * add preview method

v1.5: (2021.03.08)
  * add fix method choice

v1.0: (2021.03.08)
  * add virus fixer fix

v0.2: (2020.06.29)
  * add scriptNode, fopen,fclose,fprint keyword detection 
  * code standalonization

v0.1: (2020.06.27)
  * notes here
