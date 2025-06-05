# 个人博客网站


使用 mkdocs 生成静态网站，本地实时预览使用命令 `mkdocs serve`。

已经集成了github actions，提交代码后会自动部署到 github pages，同时配置了域名映射，可以直接通过域名 <https://myshanw.com> 或者 <https://xiaodaxia-2008.github.io> 访问。



# 本地运行

创建python虚拟环境

```shell
uv sync
```

激活虚拟环境

```shell
.venv/Scripts/activate
```

开启实时预览服务器

```bash
mkdocs serve
```

# 分支介绍

- main 和 master 分支是之前使用jekyll编译文档的遗留代码，现在已经不用，后面可能会删除
- **blog** 分支是当前用来编写新文档的主要分支，blog 上的内容会通过github actitons自动编译，然后将编译后的site产出，自动推送到gh-pages，gh-pages就是github pages的内容分支，可以通过 <https://xiaodaxia-2008.github.io> 访问，同时应为绑定了域名 <https://myshawn.com>，也可以通过它访问。
- 本站也可以通过 <https://blog.myshawn.com> 访问，这是通过 cloudflare pages 进行自动编译后生成的。