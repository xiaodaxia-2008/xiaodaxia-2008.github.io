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

# 连接本地 http 服务

整体流程和上面相同，只是应用配置那里，选 http, 以及 本地端口号：

![](attachments/Pasted%20image%2020260424143059.png)

# 协议配置

cloudflared 默认使用 quic 协议，不可用时切换到 http2 协议。
国内复杂的网络环境下，quic 经常失败，这里手动将协议直接指定为HTTP2。



## Cloudflared 协议设置说明

cloudflared 与 Cloudflare Edge 之间的连接协议支持以下几种：

### 1. 默认行为

cloudflared 默认使用：

- QUIC（基于 UDP，HTTP/3）

如果 QUIC 不可用，会自动回退到：

- HTTP/2（基于 TCP）

---

### 2. 手动指定协议

可以通过参数或 config.yml 指定协议：

#### 方法一：命令行

```bash
cloudflared tunnel run <tunnel-name> --protocol http2
````

#### 方法二：config.yml

普通用户的话 `config.yml` 在 `~/.cloudflared/config.yml` 
以管理员身份安装服务的话，读取的是 `C:\Windows\System32\config\systemprofile\.cloudflared\config.yml`

```yaml
protocol: http2
```

---

### 3. 可选协议类型

|协议|说明|
|---|---|
|quic|默认协议，基于 UDP，延迟低|
|http2|基于 TCP，更稳定|
|auto|自动选择（默认行为）|

---

### 4. 使用建议

- 网络环境良好（低丢包）：
    
    - 使用 QUIC（默认）
        
- 网络受限（公司网络 / UDP 被禁）：
    
    - 使用 HTTP/2
        

---

### 5. 常见问题

#### QUIC 连接失败

表现：

- 连接不稳定
    
- Tunnel 频繁断开
    

解决：

```yaml
protocol: http2
```

---

### 6. 日志确认

成功连接后日志中会显示：

```text
protocol=http2
```

或：

```text
protocol=quic
```

---

## 🧠为什么用 更low的http2呢？

1. **UDP 容易被限速/丢包**
    
    - 运营商和网络设备对 UDP 不友好
        
    - QUIC（基于 UDP）更容易抖动或断连
        
2. **NAT / 防火墙不稳定**
    
    - UDP 连接状态容易丢失
        
    - 长连接更容易被中断
        
3. **跨境链路优化偏向 TCP**
    
    - HTTPS（HTTP/2）基于 TCP
        
    - 已被长期优化，更稳定
        
