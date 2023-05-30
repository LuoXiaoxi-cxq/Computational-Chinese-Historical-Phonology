# Computational-Chinese-Historical-Phonology
Use Convex Optimization to solve problems in Chinese Historical Phonology, especially reconstruction. At present, only the *Qie Yun* system (Middle Chinese) is modeled by Linear Programming. In the future, I will use stronger mathematical methods and expand the scope of research to the entire history of Chinese.  
本项目意在用凸优化方法研究汉语语音史。目前，我只用了线性规划给《切韵》音系建模（即version1文件夹），但后续会用更强的数学方法将研究范围扩大到整个汉语语音史。  

## Environment Requirement
Packages used in this project are as follows:  
`numpy==1.21.5`
`pandas==1.4.2`
`PuLP==2.6.0`
`tqdm==4.64.0`   
Moreover, a solver for linear programming called `Groubi` also needs to be installed. You can apply for its free academic version [here](https://coin-or.github.io/pulp/guides/how_to_configure_solvers.html).  
The environment configuration of this project is complicated. It took me a lot of time to figure out how to use the `GROUBI` solver with the `pulp` package (You may need to read [this](https://coin-or.github.io/pulp/guides/how_to_configure_solvers.html)), but I couldn't remember all the details since it has been a long time. 
## Code Structure
The structure of directory `./version1` is as follows:  
+ `./version1/data` contains the content of *Qie Yun*.
  + 《切韵》电子版来自[古音小镜](http://www.kaom.net/)。`廣韻字音表 poem(20170209).xls`是我从古音小镜拿到的原始文件。我去掉了其中用不上的列，得到了`《广韵》全_便于处理版.xlsx`。但《广韵》收字太多，不便计算，于是我取《平水韵》、魏晋南北朝诗歌和《广韵》的交集，得到`《广韵》简化版_平水韵_魏晋南北朝隋诗歌.xlsx`。这个简化版将字头数从三万多减少到了八千多。
+ `./version1/ori_result` contains the results I got before.
  + `202305简化_广韵建模1_建模结果_广韵反切_归部_韵图介音_异读.xlsx`是我运行`./version1/src/guangyun.py`得到的结果，包含每个字的声母、韵系、声调、等、开合的计算结果，以及这个字在《广韵》中的“标准答案”。该文件各列含义详见其“说明”sheet。
  + `202305结果分析_广韵反切_归部_韵图介音_异读.xlsx`是对上一文件（即计算结果）的分析。该文件各列、各sheet含义详见其“说明”sheet。
+ `./version1/src` contains source code.
  + `global_var.py`包含全局变量，定义了各字的声母、韵系、声调、等、开合变量及一些辅助变量。供其它模块引用。可以设置变量`global_jianhua`，若其为1，则使用简化版数据`《广韵》简化版_平水韵_魏晋南北朝隋诗歌.xlsx`，否则使用全部字头`《广韵》全_便于处理版.xlsx`，默认为1。如果使用简化版数据，只需要求解十分钟左右，否则需要四五个小时。
  + `guangyun.py`是计算各字音韵地位的主要代码，会将计算结果存到`./version1/result`。
  + `tool_funcion.py`包含辅助函数，供`guangyun.py`调用。
  + `result_analyze.py`用于分析`guangyun.py`的计算结果，并将分析结果存到`./version1/result`。

## How to Run the Code
只需先运行`guangyun.py`，得到计算结果，再运行`result_analyze.py`分析结果即可。
