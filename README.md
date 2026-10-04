# LysCPP模型底座下载

本仓库分发LysCPP所用的公共DPLM预训练底座。模型来自[airkingbd/dplm2_bit_650m](https://huggingface.co/airkingbd/dplm2_bit_650m)，固定版本为 `40cf303d79335c4c8f1b13d08fbc3187e8ba9222`，按Apache-2.0许可分发。

这里不包含LysCPP的CPP微调、蒸馏或奖励优化权重，也不包含实验数据。

## 下载与放置

进入[模型下载页](https://github.com/Lzs-official/LysCPP-model/releases/tag/dplm2-bit650m-40cf303)，下载以下2个分卷：

- `dplm2_bit_650m.7z.001`
- `dplm2_bit_650m.7z.002`

将2个文件放在同一文件夹，保持文件名不变。使用[7-Zip](https://www.7-zip.org/)打开第1个文件（`.001`）并解压；第2个文件会自动参与解压。

将得到的 `dplm2_bit_650m` 文件夹放入LysCPP提交包的 `models/pretrained/` 目录。最终结构为：

```text
models/pretrained/dplm2_bit_650m/
├── pytorch_model.bin
├── config.json
├── vocab.txt
└── source.json
```

`pytorch_model.bin` 保持原样，由程序直接读取，不需要再次解压。GitHub的“Code → Download ZIP”只下载本仓库说明和配置，模型文件请从上面的下载页获取。

## 完整性

原始权重大小为2,616,587,562字节，SHA-256为：

```text
27d73fca4faf9ed5440ae8952c3711c366686d3e5ee49d188bb36cef9d94ff48
```

发布流程核对上游固定版本、分卷完整性和解压后文件校验值。下载页同时提供 `SHA256SUMS.txt` 和 `verification.json`。本仓库仅进行无损打包，模型参数不变。

模型来源与配置见[model/source.json](model/source.json)，上游项目见[bytedance/dplm](https://github.com/bytedance/dplm)。
