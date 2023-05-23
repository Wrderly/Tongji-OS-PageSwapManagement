# Tongji-OS-PageSwapManagement

同济大学操作系统课内存管理项目-请求调页存储管理方式模拟

## 项目需求

### 基本任务

  假设每个页面可存放10条指令，分配给一个作业的内存块为4。模拟一个作业的执行过程，该作业有320条指令，即它的地址空间为32页，目前所有页还没有调入内存。

### 模拟过程

  在模拟过程中，如果所访问指令在内存中，则显示其物理地址，并转到下一条指令；如果没有在内存中，则发生缺页，此时需要记录缺页次数，并将其调入内存。如果4个内存块中已装入作业，则需进行页面置换。
  所有320条指令执行完成后，计算并显示作业执行过程中发生的缺页率。

## 项目实现

  本项目基于python3.10完成，使用pyqt5完成程序的界面。界面的设计使用qt designer完成。

## 项目展示

  项目界面如下

<img src="file:///C:/Users/asus/AppData/Roaming/marktext/images/2023-05-23-17-57-18-image.png" title="" alt="" width="390">

  在开始执行一次模拟之前，用户可以设定作业的总指令数与采用的页面置换算法。置换算法包括FIFO与LRU。

  设定仅在一次模拟开始前生效，模拟过程中更改设定并不会生效。

  当用户点击单步执行或连续执行后，一次模拟即开始，直到执行完设定的指令总数或者用户按下重置按钮后，一次模拟结束。



    界面的左边分别展示分配给作业的四个页，每个页存储10条指令，竖向的十个按钮为一组，表示内存中的一页。每个按钮上显示该按钮存放的指令的地址(即0到作业总指令数减1)，每组按钮的上方显示该内存页存放的指令是作业的哪一页。四组按钮的下方显示当前发生缺页情况的次数与当前的缺页率

  每次执行指令后，以红色高亮按钮，显示本次执行的指令在内存中的位置。

  界面的右侧包含一个文本框。其中主要打印指令的执行状况，如本次执行的指令的地址、是否发生缺页、换出页与换入页等。

<img src="file:///C:/Users/asus/AppData/Roaming/marktext/images/2023-05-23-18-01-57-image.png" title="" alt="" width="394">
