# CANFD-ID-Packer

CAN FD 29 位扩展帧 ID 组包与反解析工具。

这是一个基于 Python 和 PyQt6 开发的桌面小工具，用于将 CAN FD 29 位扩展帧 ID 按照用户自定义字段进行拆分、组包和反向解析。

## 功能特点

- 支持 CAN FD 29 位扩展帧 ID 自定义字段拆分
- 支持字段名称和位宽配置
- 支持 Hex 数值输入
- 自动生成完整 29 位扩展帧 ID
- 显示二进制排列结果
- 支持完整 Hex ID 反向解析为各个字段
- 支持 Windows exe 打包运行

## 默认字段配置

| 字段名称 | 位宽 |
|---|---:|
| Priority | 3 bit |
| Source | 8 bit |
| Target | 8 bit |
| Command | 10 bit |

总位宽为 29 bit。

## 运行源码

### 1. 安装依赖

```bash
pip install -r requirements.txt