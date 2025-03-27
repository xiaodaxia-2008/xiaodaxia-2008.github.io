---
title: 使用cloudflare tunnels连接到本地主机的ssh服务
description: 如何使用cloudflare tunnel进行内网穿透，从互联网接入自己家中的内网设备
date: 2024-11-29T00:00:00
categories:
  - 网络技术
tags:
  - 网络
  - cloudflare
---

在cloudflare托管域名以后，可以使用cloudflare的Tunnels来实现内网穿透，将本地服务暴露到互联网。

<!-- more -->

假设我们托管的域名是 example.com 。

## 创建隧道

进入到 ZeroTrust/Networks/Tunnels 页面, 点击 `Create a tunnel`，根据提示一步步设置。

## 开启Public hostnames SSH服务

在Tunnel的Public hostnames，可以映射本地开启的服务，这里开启一个ssh服务：

- Subdomain: ssh
- Domain: example.com
- Path: 留空就行
- Type: 选择ssh
- URL: localhost:22

  其他设置可以不用修改。上面会将运行cloudflared隧道服务的个人本地电脑的 ssh 服务(默认端口是22) 映射到 ssh.example.com 这个域名。但是现在还不能直接通过 `https://ssh.example.com` 访问本地电脑的ssh服务。

## 添加 Browser rendering SSH 应用

进入 ZeroTrust/Access/Applications 页面，点击 `Add an application`

1. Select type, 选择 `Self-hosted`，点击下一步

2. Configure application
    - Application name: MySSHApp，随便起一个
    - Application domain:
      - Subdomain: ssh, 就是上一步Public hostnames里面设置的
      - Domain: example.com
    点击下一步。

3. Add policies
     - Policy name: 随便起一个，MyPolicy
     - Action: 选择 Allow
     - Configure rules/Include/Selector: 可以选择 Emails
     - Configure rules/Include/Value: 填写允许登录使用的邮箱，比如 <fuck@qq.com>
     填完了以后，点击一下 `Add include`，然后点击 `Next`，进入到 `Setup`。

4. Setup
     页面滚动到最下面，`Additional Settings/Browser rendering`，设置为 `SSH`，右下角点击 `Add application`。

大功告成，在浏览器地址栏中输入 `https://ssh.example.com` ，在页面中输入之前设置的允许访问的邮箱，在输入邮箱接收到的验证码，就可以通过浏览器登入本地电脑的ssh服务了。
