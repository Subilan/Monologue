<img src="https://i.loli.net/2020/04/11/YIQc1JMwU2LbSz5.png" align="right" width="100" height="100">

# 💬 Monologue

![](https://img.shields.io/badge/coverage-45%25-green?style=flat)
![](https://img.shields.io/badge/front-Vue.js-brightgreen?style=flat&logo=vue.js)
![](https://img.shields.io/badge/back-python-blue?style=flat&logo=python)
[![](https://img.shields.io/badge/wiki-clickhere-009688?style=flat)](https://book.sotap.org/#/monologue/index)

![main-without-sotap.png](https://i.loli.net/2020/05/11/FbmTvcWoQfBGIkl.png)

**Monologue** 是一个用于管理项目体验并对外展示的 Vue 程序，后端使用 Python 开发。Monologue 会合并先前 Oasis 的所有功能，并添加更多与项目管理方面的内容。

## 概述

起初 Monologue 只是被设计用来记录日志。后来我发现，这些功能其实都可以分为一类——项目管理。我们这里所说的管理并不是流程化，也不是更高级的其它，而是针对一个项目体验方面的一系列可能用到的功能。

投票、问卷、更新日志，想想我们以往是如何满足这些需求的？我们有腾讯问卷，有 QQ 群内投票。对于时间线，有些人选择了 GitHub 的 README，还有的人选择了群公告。总之，有很多很多不同的办法来满足这些需求，但都不是统一的，大多数情况下我们也无法完全掌握数据。

Monologue 就是对这些功能的整合，是可部署的，扩展性更高。例如，我们可以选择是否开放 API、开放哪些 API，亦或者是把问卷的数据公开浏览，所有想象中能实现的都能实现。而所有的数据都会被存储在本地的数据库里，有了完全访问。当然，Monologue 并没有想要取代谁，因为不够资格。

![](https://i.loli.net/2020/04/19/Z6lO7pRDrw8t9Mj.png)

## 贡献或部署

贡献时，需要手动部署前端和后端。参阅 [Wiki](https://book.sotap.org/#/monologue/index)，我们编写了针对 production 和 development 的两种部署方式，按需选择。

## 关于

![](https://i.loli.net/2020/04/22/HVgw5caiYed3Lxk.jpg)

Monologue 的产生并不代表着一种新想法，而是为了节省时间做出的功能集合，通过某种概念让它们合理地组合在一起。Monologue 的开发之路还有很长，短期之内也似乎无法做出很多功能来，但是并不会因为不可抗力外的原因停止开发，我们也欢迎所有人的贡献。

**请注意：** 我们无法保证 Monologue 在 Coverage 75% 之前不做出破坏性的改动。

## 协议

Apache-2.0
