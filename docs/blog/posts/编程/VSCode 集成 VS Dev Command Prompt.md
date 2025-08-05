---
title: VSCode 集成 VS Dev Command Prompt
authors:
  - Shawn
date: 2025-07-24T22:45:13
---
记录一下如何在VSCode中添加MSVC的Dev环境。

<!-- more -->

1. 按Ctrl+P打开命令面板，搜索 "Open User Settings (Json)"，打开json配置文件
2. 添加如下代码：

```json
 "terminal.integrated.profiles.windows": {
    "VS Dev Command Prompt": {
      "overrideName": true,
      "path": [
        "pwsh.exe"
      ],
      "args": [
        "-NoExit",
        "-Command",
        "& {Import-Module 'C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\Tools\\Microsoft.VisualStudio.DevShell.dll'; Enter-VsDevShell bcb9ea00 -SkipAutomaticLocation -DevCmdArguments '-arch=x64 -host_arch=x64'}"
      ],
      "icon": "terminal",
      "env": {}
    }
  },
```

引号什么的搞了好久，木乱。



*2025-07-24 22:45:13*