# CANFD-ID-Packer

[中文](#中文说明) | [English](#english-description)

---

## 中文说明

CAN FD 29 位扩展帧 ID 组包与反解析工具。

这是一个基于 Python 和 PyQt6 开发的桌面小工具，用于将 CAN FD 29 位扩展帧 ID 按照用户自定义字段进行拆分、组包和反向解析。

不同于固定格式的 J1939 PGN 计算器，本工具支持用户自定义 29 位 CAN 扩展帧 ID 字段划分，更适合自定义 CAN/CAN FD 通讯协议调试。

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
```

### 2. 运行程序

```bash
python CANFD_Process.py
```

## 下载 Windows 可执行文件

如果不想安装 Python 环境，可以直接下载 Windows 版本。

进入本仓库的 [Releases](../../releases) 页面，下载最新版本的压缩包，解压后双击 `.exe` 文件运行。

## 使用说明

1. 在左侧配置字段名称和字段位宽。
2. 确保所有字段位宽总和为 29 bit。
3. 在右侧输入每个字段的 Hex 值。
4. 程序会自动生成完整的扩展帧 ID。
5. 也可以输入完整 Hex ID，反向解析出每个字段的值。

## 打包说明

本项目可以使用 PyInstaller 打包为 Windows 可执行文件。

示例命令：

```bash
pyinstaller --noconfirm --windowed --name CANFD_ID_Packer --icon logo.ico --add-data "logo.ico;." CANFD_Process.py
```

---

## English Description

CANFD-ID-Packer is a desktop tool for packing and parsing CAN FD 29-bit extended frame IDs.

It is developed with Python and PyQt6. The tool allows users to split a 29-bit CAN extended ID into custom fields, enter field values in hexadecimal format, and automatically generate the complete extended frame ID. It also supports reverse parsing from a complete Hex ID back into individual fields.

Unlike fixed-format J1939 PGN calculators, this tool supports fully customizable 29-bit CAN extended ID field layouts. It is useful for debugging custom CAN/CAN FD communication protocols.

## Features

- Customizable 29-bit CAN FD extended ID field layout
- Editable field names and bit lengths
- Hex value input for each field
- Automatic generation of complete 29-bit extended frame ID
- Binary layout display
- Reverse parsing from complete Hex ID to individual fields
- Windows executable support

## Default Field Layout

| Field Name | Bit Length |
|---|---:|
| Priority | 3 bit |
| Source | 8 bit |
| Target | 8 bit |
| Command | 10 bit |

Total length: 29 bit.

## Run from Source

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the program

```bash
python CANFD_Process.py
```

## Download Windows Executable

If you do not want to install Python, you can download the Windows executable version.

Go to the [Releases](../../releases) page, download the latest zip package, extract it, and run the `.exe` file.

## Usage

1. Configure field names and bit lengths on the left side.
2. Make sure the total bit length is 29 bit.
3. Enter the Hex value for each field on the right side.
4. The tool will automatically generate the complete extended frame ID.
5. You can also enter a complete Hex ID to reverse parse it into individual fields.

## Build Windows Executable

This project can be packaged as a Windows executable with PyInstaller.

Example command:

```bash
pyinstaller --noconfirm --windowed --name CANFD_ID_Packer --icon logo.ico --add-data "logo.ico;." CANFD_Process.py
```

## License

MIT License
