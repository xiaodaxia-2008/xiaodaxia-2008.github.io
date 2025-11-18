---
title: cereal 和 nlohmann-json 的奇怪冲突
authors:
  - Shawn
date: 2025-11-18T13:38:07
tags:
  - cpp
  - cereal
  - nlohmann_json
  - 序列化
categories:
  - 编程
---

# cereal 和 nlohmann-json 的奇怪冲突

## 问题描述

最近在处理一个对象同时支持 `cereal` 和 `nlohmann-json` 序列化时，遇到了一个奇怪的问题。具体来说，当定义了序列化函数，同时支持这两种序列化库时，程序会出现编译错误。

下面是简化后的代码示例：

```c++
#include <cereal/archives/binary.hpp>
#include <nlohmann/json.hpp>
#include <sstream>
#include <string>

struct Waypoint
{
    int id{0};

    // cereal 序列化函数
    void serialize(auto &ar, [[maybe_unused]] uint32_t version) { ar(id); }
};

// nlohmann-json 序列化函数
void to_json(nlohmann::json &j, const Waypoint &wp)
{
    j = nlohmann::json{wp.id};
}

void from_json(const nlohmann::json &j, Waypoint &wp) { wp.id = j.get<int>(); }

// cereal 与 nlohmann-json 的 save 和 load 函数
void save(auto &ar, const nlohmann::json &j) { ar(j.dump()); }

void load(auto &ar, nlohmann::json &j)
{
    std::string s;
    ar(s);
    j = nlohmann::json::parse(s);
}

int main()
{
    std::stringstream ss;
    Waypoint wp1{.id = 1};

    // 使用 cereal 序列化
    {
        cereal::BinaryOutputArchive oar{ss};
        oar(wp1);
    }

    Waypoint wp2;

    // 使用 cereal 反序列化
    {
        cereal::BinaryInputArchive iar{ss};
        iar(wp2);
    }
}
```


当编译上述代码时，你可能会遇到如下错误信息：

```
cereal found more than one compatible output serialization function for the provided type and archive combination...
```

通过对 `cereal` 源码的深入分析，逐步确定了问题所在。原因在于，`void save(auto &ar, const nlohmann::json &j)` 这个函数和 `Waypoint` 类内的 `serialize` 函数都可以被调用来序列化 `Waypoint`。具体来说，`Waypoint` 定义的 `to_json` 函数让其可以隐式转换为 `nlohmann::json`，而 `nlohmann::json` 又定义了一个 `cereal` 的 `save` 函数。由于这两个函数之间的重叠，`cereal` 序列化机制无法决定使用哪个函数，从而导致了编译错误。

## 解决方法

为了解决这个问题，可以通过偏特化模板来调整 `nlohmann::json` 的 `save` 和 `load` 函数，从而避免冲突，并且同时支持 `nlohmann::json` 和 `nlohmann::ordered_json` ：

```c++
template <template <typename...> class ObjectType>
void save(auto& ar, const nlohmann::basic_json<ObjectType>& j)
{  
    ar(j.dump());
}

template <template <typename...> class ObjectType>
void load(auto& ar, nlohmann::basic_json<ObjectType>& j)
{  
    std::string s;
    ar(s);
    j = nlohmann::basic_json<ObjectType>::parse(s);
}
```

通过这种方式，我们明确指定了如何序列化和反序列化 `nlohmann::json` 对象，避免了与 `Waypoint` 内部 `serialize` 函数的冲突。

## 总结

在处理同时支持 `cereal` 和 `nlohmann-json` 的序列化时，遇到的冲突通常是由于重载函数之间的不明确匹配导致的。通过模板偏特化，解决这个问题，并确保两者兼容共存。



*2025-11-18 13:38:07*