---
title: Clash 分流规则
authors:
  - Shawn
date: 2025-11-11T21:36:15
tags:
  - clash
  - vpn
---
## 常用的几个clash客户端

有关科学上网的知识及工具。


<!-- more -->


### 桌面

[GitHub - clash-verge-rev/clash-verge-rev: A modern GUI client based on Tauri, designed to run in Windows, macOS and Linux for tailored proxy experience](https://github.com/clash-verge-rev/clash-verge-rev)

[GitHub - mihomo-party-org/clash-party: :electron: Another Mihomo GUI.](https://github.com/mihomo-party-org/clash-party)

[GitHub - libnyanpasu/clash-nyanpasu: Clash Nyanpasu～(∠・ω\< )⌒☆​](https://github.com/libnyanpasu/clash-nyanpasu)

## 移动端

下面几个基本都是基于 `flutter` 的全平台客户端，包括 iOS/Android/Windows/MacOS/Linux


[GitHub - KaringX/karing: Simple & Powerful proxy utility, Support routing rules for clash/sing-box](https://github.com/KaringX/karing.git)

[GitHub - hiddify/hiddify-app: Multi-platform auto-proxy client, supporting Sing-box, X-ray, TUIC, Hysteria, Reality, Trojan, SSH etc. It’s an open-source, secure and ad-free.](https://github.com/hiddify/hiddify-app)

[GitHub - chen08209/FlClash: A multi-platform proxy client based on ClashMeta,simple and easy to use, open-source and ad-free.](https://github.com/chen08209/FlClash)

这个是专门针对 Andorid 平台
[GitHub - MetaCubeX/ClashMetaForAndroid: A rule-based tunnel for Android.](https://github.com/MetaCubeX/ClashMetaForAndroid)



## Clash 中自定义分流规则

定义一个全局脚本，基本内容是：
- 根据正则表达式对各个节点进行分组
- 从[GitHub - zt6/github\_blackmatrix7\_ios\_rule\_script](https://github.com/zt6/github_blackmatrix7_ios_rule_script)获取一些域名分组
- 对不同的规则组使用不同的节点分组

```js
// Define main function (script entry)

function main(params) {
  const USGroupName = addProxyGroup(params, "美国节点", /美国|US|United States|America|🇺🇸/);
  const JPGroupName = addProxyGroup(params, "日本节点", /日本|JP|Japan|🇯🇵/);
  const SGGroupName = addProxyGroup(params, "新加坡节点", /新加坡|狮城|SG|Singapore|🇸🇬/);
  const HKGroupName = addProxyGroup(params, "香港节点", /香港|HK|Hong Kong|HongKong|🇭🇰/);
  const IndiaGroupName = addProxyGroup(params, "印度节点", /印度|India|🇮🇳/);


  addGPTProxyGroup(params, [USGroupName, JPGroupName, SGGroupName, IndiaGroupName]);
  // 添加规则
  addRules(params);
  // 添加 rule-providers
  addRuleProviders(params);

  return params;
}

function addProxyGroup(params, groupName, regex) {
  // 判断是否已经存在某个代理组（如"美国节点"）的名称
  const group = params["proxy-groups"].find((e) => regex.test(e.name) || e.name === groupName);
  if (group === undefined) {
    const proxiesByRegex = params.proxies.filter((e) => regex.test(e.name)).map((e) => e.name);
    // 判断proxiesByRegex是否为空数组
    if (proxiesByRegex.length === 0) {
      return null; // 没有匹配的代理，直接返回
    }
    params["proxy-groups"].push({
      name: groupName,
      type: "url-test",
      url: "http://www.gstatic.com/generate_204",
      interval: 86400,
      proxies: proxiesByRegex,
    });
    return groupName; // 没有的话就创建一个新的代理组
  }
  // 有了的话直接返回这个代理组的名称
  return group.name;
}

function addGPTProxyGroup(params, groups){
  // 创建一个名为"MyGPT"的代理组
  params["proxy-groups"].push({
    name: "MyGPT",
    type: "select",
    proxies: groups,
  });
}

function addRuleProviders(params) {
  // 如果 params 中没有 rule-providers，则创建它
  if (!params["rule-providers"]) {
    params["rule-providers"] = {};
  }

  // 添加 OpenAI rule provider
  params["rule-providers"]["OpenAI"] = {
    type: "http",
    behavior: "classical",
    url: "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/OpenAI/OpenAI.yaml",
    path: "./ruleset/OpenAI.yaml",
    interval: 86400
  };

  params["rule-providers"]["Google"] = {
    type: "http",
    behavior: "classical",
    url: "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Google/Google.yaml",
    path: "./ruleset/Google.yaml",
    interval: 86400
  };
}

function addRules(params) {
  // 设置openai用哪个节点访问
  const proxyGroup = "MyGPT";
  const USGroupName = "美国节点";

  // 创建一个规则数组
  const rules = [
    // 微软中国
    "GEOSITE,microsoft@cn,DIRECT",

    // openai
    "GEOSITE,openai," + proxyGroup,
    "RULE-SET,OpenAI," + proxyGroup,

    // google
    "GEOSITE,google," + proxyGroup,
    "RULE-SET,Google," + proxyGroup,

    // claude
    "DOMAIN,servd-anthropic-website.b-cdn.net," + USGroupName,
    "DOMAIN,cdn.usefathom.com," + USGroupName,
    "DOMAIN-SUFFIX,anthropic.com," + USGroupName,
    "DOMAIN-SUFFIX,claude.ai," + USGroupName,
    // gemini api
    "DOMAIN-SUFFIX,generativelanguage.googleapis.com," + USGroupName,

    // linux.do
    "DOMAIN-SUFFIX,linux.do,DIRECT",
    // fuclaude.com
    "DOMAIN-SUFFIX,fuclaude.com,DIRECT",
    // oaifree
    "DOMAIN-SUFFIX,oaifree.com,DIRECT",

  ];

  // 把rules中的规则全部添加到params.rules中
  params["rules"] = rules.concat(params["rules"]);
}
```



*2025-11-11 21:36:15*