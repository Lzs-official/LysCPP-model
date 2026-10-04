公共DPLM-2.1 Bit 650M预训练底座，用于LysCPP本地加载。

下载 `dplm2_bit_650m.7z.001` 和 `dplm2_bit_650m.7z.002`，放在同一文件夹，使用7-Zip打开 `.001` 解压。将解压得到的 `dplm2_bit_650m` 文件夹放入提交包 `models/pretrained/`。

原始权重保持不变；解压后不要再次解压 `pytorch_model.bin`。GitHub自动附带的Source code压缩包不包含模型权重。

来源：`airkingbd/dplm2_bit_650m`

固定版本：`40cf303d79335c4c8f1b13d08fbc3187e8ba9222`

原始权重SHA-256：`27d73fca4faf9ed5440ae8952c3711c366686d3e5ee49d188bb36cef9d94ff48`

`SHA256SUMS.txt` 是文件完整性校验清单，记录两个模型分卷的“指纹”（SHA-256校验值），用于核对下载文件是否完整、内容是否一致。`verification.json` 是发布时的打包与解压校验记录。

正常使用只需下载 `.001` 和 `.002` 两个分卷。以上两个辅助文件可选下载，不参与程序运行，也无需放入模型文件夹。

模型许可为Apache-2.0。
