<img src="https://i.loli.net/2020/04/11/YIQc1JMwU2LbSz5.png" align="right" width="100" height="100">

# 💬 Monologue

![](https://img.shields.io/badge/coverage-25%25-red?style=flat)
![](https://img.shields.io/badge/front-Vue.js-brightgreen?style=flat&logo=vue.js)
![](https://img.shields.io/badge/back-python-blue?style=flat&logo=python)

![main.png](https://i.loli.net/2020/04/11/CAD8nRzkWmxSFKU.png)

**Monologue** 是一个用于管理项目体验并对外展示的 Vue 程序，后端使用 Python 开发。Monologue 会合并先前 Oasis 的所有功能，并添加更多与项目管理方面的内容。

## 概述

关于 Oasis，因为一系列的原因，包括但不仅限于

- 突然需求的丢失，导致 Eulogy 的诞生；
- 内部代码过于杂乱，且没有使用 Typescript；
- PHP 在某些方面开发困难，导致难以维护，或者遭遇难以解决的瓶颈。

停止开发。而后，又因为有「将日志发布出来记录」的需求，Monologue 诞生了。起初 Monologue 只是被设计用来记录日志：

![](https://i.loli.net/2020/04/19/Z6lO7pRDrw8t9Mj.png)

后来我发现，这些功能其实都可以分为一类——项目管理。我们这里所说的管理并不是流程化，也不是更高级的其它，而是针对一个项目体验方面的一系列可能用到的功能：

- 投票
- 问卷
- 更新日志
- 等等

对于这些功能，我们可能常常会去使用不同的软件来实现。如果我们可以将这些功能整合到同一个平台上来使用，扩展性更高。例如，我们可以将问卷数据公开、支持投票数据的 get API，等等。当然，Monologue 并没有想要取代谁，因为还不够资格。

## 贡献

贡献时，前端仅需 `npm install` 即可安装所需依赖开始开发。但是需要注意的是，由于用到了 TypeScript，vue-material 的所有组件均无法正常使用，需要手动在每一个 `import` 前面加上 `// @ts-ignore` 来忽略。对于各种内置的接口目前并没有文档。

后端需要手动部署数据库。查看 `backend/mono-back/database.sql` 中的语句，复制到 MySQL 中执行。执行之后，需要使用位于 `backend/mono-back` 中的 `python.bat` 执行 `Test.py` 来完成基本账户的创建，因为目前还并没有写出注册功能。

```bash
# first, copy n paste the statements in database.sql and execute them in the mysql command prompt.
cd /backend/mono-back
./python.bat Test.py
```

> ⚠ 后端所有与 `python.exe` 或 `pip.exe` 相关的操作都必须使用位于 `/backend/mono-back` 下的两个批处理脚本完成，因为使用了虚拟环境。例：
```bash
cd /backend/mono-back
./pip.bat install flask
./python.bat App.py
# 实质上就是调用了 /backend/mono-back/Scripts 下的两个 exe
```

## 关于

![](https://i.loli.net/2020/04/22/HVgw5caiYed3Lxk.jpg)

这是制作过程中的一张照片。Monologue 的产生并不代表着一种新想法，而是为了节省时间做出的功能集合，通过某种概念让它们合理地组合在一起。

Monologue 的开发之路还有很长，短期之内也似乎无法做出很多功能来，但是并不会因为不可抗力外的原因停止开发，我们也欢迎所有人的贡献。

**Monologue 在 coverage 未达到 75% 之前无法保证不出现巨大破坏性的改动，因此请不要过早用于 production。**

## 协议

MIT
