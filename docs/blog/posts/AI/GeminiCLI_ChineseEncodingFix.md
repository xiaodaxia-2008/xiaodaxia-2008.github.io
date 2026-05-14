---
title: Gemini CLI Windows 11 中文乱码解决方案
date: 2026-05-14
description: 解决 Gemini CLI 在 Windows 11 环境下调用 shell 时出现中文乱码的问题。
tags:
  - Gemini-CLI
  - Windows
  - PowerShell
  - 编码
categories:
  - AI
  - 编程
---

在使用 Gemini CLI 时，对话界面通常显示正常，但在调用 
un_shell_command 执行涉及中文输出的命令时，控制台可能会出现乱码。这是由于工具的 UTF-8 输出与 PowerShell 默认的 GBK 编码不匹配导致的。

<!-- more -->

## 问题描述

在使用 Gemini CLI 的过程中，AI 生成的回复中文显示完美，但一旦让其调用 Shell 执行命令（例如查看目录、编译报错信息等），返回的内容就会变成无法辨认的乱码。对于在 Windows 环境下进行开发的同学，这是一个非常普遍的痛点。

## 原因分析

Windows 版本的 Gemini CLI 默认调用 powershell.exe 来执行系统命令。乱码的根源在于：
- **编码冲突**：Gemini CLI 及大多数现代开源工具均采用 **UTF-8** 编码。
- **默认环境限制**：Windows PowerShell (5.x) 或默认配置下的 PowerShell 7 在中文系统里通常沿用 **GBK (CP936)** 编码。
- **解析错位**：当 Shell 尝试用 GBK 逻辑去解析 UTF-8 的数据流时，就会产生乱码。

## 解决方案：配置 PowerShell Profile

通过修改 PowerShell 的配置文件（Profile），我们可以确保每次 Shell 启动时都自动切换到正确的编码环境。

### 1. 询问 Gemini CLI 使用的 PowerShell 版本
最直接的方法是让 Gemini CLI 帮你查询。在对话中输入：

```
你当前使用的是哪个 PowerShell 版本？运行 $PSVersionTable 告诉我结果。
```

它会调用 Shell 命令并返回类似如下信息：

```
Name                           Value
----                           -----
PSVersion                      5.1.22621.4249
PSCompatibleVersions           {1.0, 2.0, 3.0, 4.0...}
BuildVersion                   10.0.22621.4249
CLRVersion                     4.0.30319.42000
Platform                       Win32NT
PSComposition                  
PSWorkflowType                 
PSRemotingProtocolVersion      2.4
SerializationVersion           1.1.0.1
```

根据返回的 **PSVersion**，在本地打开一个相同版本的 PowerShell，然后在其中执行：

```
echo $PROFILE
```

这会直接输出当前版本的 Profile 配置文件路径。

### 2. 写入编码配置
使用你喜欢的编辑器（如 Notepad 或 VS Code）打开该文件：

```powershell
notepad $PROFILE
```
在文件末尾添加以下三行核心配置：

```powershell
# 强制指定控制台输入、输出以及全局输出编码为 UTF-8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
```
*注：对于 PowerShell 5.1 来说，最后一行 $OutputEncoding 是确保捕获外部命令输出不乱码的关键。*

## 验证效果

保存并关闭配置文件后，**重启 Gemini CLI** 或重新开启一个会话。执行一个带有中文输出的命令进行验证：

```powershell
dir | findstr "文档"
```

---

## 备选方案：系统级 UTF-8 (Beta)

如果上述 Profile 方案在某些极端情况下失效，可以尝试 Windows 提供的系统级支持：
1. 打开 **控制面板** > **区域**。
2. 切换至 **管理** 选项卡，点击 **更改系统区域设置**。
3. 勾选 **Beta: 使用 Unicode UTF-8 提供全球语言支持**。
4. 重启计算机以生效。

---
*2026-5-14*