## CJK Textwrap

`cjk-textwrap`是Python 3.6`textwrap`模块的[中日韩字符](https://en.wikipedia.org/wiki/CJK_characters)兼容版本。此外，它提供了灵活的接口以便用户自定义分词器（如[结巴分词](https://github.com/fxsjy/jieba)）。

`cjk-textwrap` is a [CJK characters](https://en.wikipedia.org/wiki/CJK_characters) compatible version of Python 3.6's `textwrap` module. Moreover, it provides flexible interfaces which allows users to define their own text segmentation for text wrapping like [jieba](https://github.com/fxsjy/jieba).

### Installation 安装

pip:

```bash
pip install cjk-textwrap
```

poetry:

```bash
poetry add cjk-textwrap
```

### Feature 功能特性

Although user can get various language support by adding their custom splitter, `cjk-textwrap` provides built-in `English-Chinese` mixed text phrase wrapping support.

虽然可以通过自定义分词器添加各种语言的支持，但是`cjk-textwrap`提供了原生的*中-英文*混合句支持。

- [x] Chinese Support 中文支持
- [ ] Japanese Support 日文支持
- [ ] Korean Support 韩文支持

### LICENSE 协议许可

This project is licensed under MIT.
