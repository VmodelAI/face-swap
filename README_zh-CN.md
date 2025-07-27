[English Version](README.md)

# Face Swap - 基于 Roop 和 GFPGAN 的高保真换脸工具

这是一个基于 `roop` 的开源人脸交换项目。它利用 `inswapper_128.onnx` 模型进行核心的换脸操作，并集成强大的 `GFPGANv1.4` 模型对生成的人脸进行细节增强和清晰度优化。

整个应用通过 `Cog` 进行容器化封装，确保了环境的一致性和可复现性，并可以一键部署到 [Replicate](https://replicate.com/) 平台，作为稳定、可扩展的 API 服务运行。

<img width="1600" height="900" alt="i" src="https://github.com/user-attachments/assets/c7a7eeea-c8b3-4d44-b9a1-99f03d36855f" />

*<p align="center">从左到右：源人脸图像，目标图像，换脸后图像</p>*

---

## 核心特性

* **精准换脸**: 采用 `insightface` 提供的 `inswapper_128.onnx` 模型，能够准确地识别和替换图像中的人脸。
* **画质增强**: 集成 `GFPGANv1.4`，一个先进的人脸修复算法，能够显著提升换脸后人脸的清晰度和真实感，修复模糊和伪影。
* **Cog 容器化**: 使用 `cog` 进行打包，将所有复杂的依赖（CUDA, Python库, 系统包）固化在容器中，彻底告别环境配置的烦恼。
* **一键部署**: 完美适配 `Replicate` 平台，只需一个命令即可将模型部署为生产级的 API 服务，无需关心服务器运维。

---

## ⚠️ 重要声明：使用限制与道德准则

### 1. 使用目的
本项目及其源代码**仅供学术研究和技术学习使用**。

### 2. 严格的非商业许可
本项目基于 `roop` 开发，因此继承了其**严格的非商业使用（Non-Commercial）**许可。严禁将此项目及其生成的任何内容用于商业目的。这包括但不限于：销售、集成到付费产品中、用于商业广告或营销材料等。

### 3. 道德与法律责任
用户在使用本技术时必须承担全部道德和法律责任。**严禁使用本工具创建任何形式的色情、暴力、诽谤、侵犯隐私或具有欺骗性的内容**。开发者对任何因滥用此工具而导致的负面后果概不负责。

---

## 技术栈

| 技术组件        | 角色     | 描述                                                                 |
| :-------------- | :------- | :------------------------------------------------------------------- |
| **`roop`** | 核心框架 | 提供了人脸交换的基础逻辑和流程。                                     |
| **`insightface`** | 换脸引擎 | 使用其 `inswapper_128.onnx` 模型，这是业界公认的高性能人脸分析库。 |
| **`GFPGAN`** | 画质增强 | 使用 `GFPGANv1.4.pth` 模型，一个强大的盲脸修复模型，用于提升输出人脸的质量。 |
| **`Cog`** | 模型打包 | 一个将机器学习模型打包成标准、可移植容器的工具，极大简化了部署流程。 |
| **`Replicate`** | 云端部署 | 一个让开发者可以轻松运行和分享机器学习模型的云平台。                 |

---

## 本地运行指南

### 1. 环境准备
在开始之前，请确保你的系统已经安装了以下软件：
* **NVIDIA 显卡驱动**
* **Docker**: Cog 依赖 Docker 来构建和运行容器。
* **Cog**: Replicate 官方的模型打包工具。

    ```bash
    # Linux / WSL
    sudo curl -o /usr/local/bin/cog -L "[https://github.com/replicate/cog/releases/latest/download/cog_$(uname](https://github.com/replicate/cog/releases/latest/download/cog_$(uname) -s)_$(uname -m)"
    sudo chmod +x /usr/local/bin/cog

    # macOS (Homebrew)
    brew install cog
    ```

### 2. 项目安装
克隆本项目代码库到你的本地机器。

```bash
git clone [https://github.com/VmodelAI/face-swap.git](https://github.com/VmodelAI/face-swap.git)
cd face-swap
```

### 3. 模型下载
你**无需手动下载**任何模型文件。项目中的 `model_manager.py` 脚本会在首次运行时自动检查 `inswapper_128.onnx` 和 `GFPGANv1.4.pth` 是否存在，如果不存在，会自动从网络下载到项目根目录。

### 4. 理解 `cog.yaml`
`cog.yaml` 是项目的配置文件，它告诉 Cog 如何构建运行环境。

```yaml
build:
  gpu: true
  cuda: "11.8"
  python_version: "3.9"
  python_packages:
    - "opencv-contrib-python==4.7.0.72"
    - "ftfy==6.1.1"
    - "scipy==1.9.3"
    - "Pillow==9.4.0"
    - "mediapipe"
    - "numpy==1.24.3"
    - "opencv-python==4.7.0.72"
    - "onnx==1.14.0"
    - "insightface==0.7.3"
    - "psutil==5.9.5"
    - "tensorflow>=2.0.0"
    - "opennsfw2==0.10.2"
    - "gfpgan==1.3.8"
    - "realesrgan"
    - "torchvision==0.12.0"
    - "onnxruntime-gpu==1.15.0"
  system_packages:
    - ffmpeg
    - libsm6
    - libxext6
predict: "predict.py:Predictor"
```

### 5. 执行本地预测
使用以下命令在本地进行一次完整的换脸预测。Cog 会自动在 Docker 容器中完成所有操作。

```bash
cog predict \
  -i source="https://vmodel.ai/data/model/vmodel/photo-face-swap-pro/target_image.png" \
  -i target="https://data.vmodel.ai/data/model-example/vmodel/photo-face-swap-pro/swap_image.png" \
  -i is_enhancer="True"
```
* `-i source`: 提供源人脸的图片 URL。
* `-i target`: 提供需要被换脸的目标图片 URL。
* `-i is_enhancer`: 是否启用 `GFPGAN` 进行画质增强，`"True"` 或 `"False"`。

预测成功后，结果图片将默认保存在当前目录下，命名为 `output.png`。

---

## 部署到 Replicate

将你的模型部署到 Replicate 非常简单，只需几个命令即可获得一个公开的 API。

1.  **登录 Replicate**
    ```bash
    cog login
    ```
    (根据提示粘贴你的 Replicate API Token)

2.  **推送模型**
    将模型推送到你在 Replicate 上创建的代码库。请将 `vmodelai/face-swap` 替换为你自己的用户名和模型名。

    ```bash
    cog push r8.im/vmodelai/face-swap
    ```
    Cog 会自动构建镜像并将其推送到 Replicate。完成后，你的模型就可以在线使用了！

---

## 性能对比：Face Swap vs. Face Swap Pro

<img width="1600" height="900" alt="face swap api" src="https://github.com/user-attachments/assets/070c0774-c8ea-4230-b56a-529be7c7a7a1" />


为了帮助用户做出正确的选择，我们将此开源项目与我们的另一款商业级模型 `Face Swap Pro` 进行对比。

| 特性       | Face Swap (本项目)         | Face Swap Pro (商业版)                                               |
| :--------- | :------------------------- | :------------------------------------------------------------------- |
| **核心技术** | 基于 `roop` 的开源方案     | 自主研发的先进商业算法                                               |
| **效果质量** | 良好，通过 GFPGAN 增强     | **更优**。照片级真实感，细节更丰富，伪影更少，且能更好地处理面部遮挡情况。 |
| **运行速度** | 中等                       | **更快**。针对商业应用优化，推理速度显著提升                         |
| **适用场景** | 学术研究、技术学习、个人项目 | 商业产品集成、大规模应用、专业内容创作                               |
| **许可协议** | **严格非商业** | **商业授权**，可用于盈利性产品                                       |

**总结**: 本项目 (`face-swap`) 是一个出色的学习和研究工具。如果你需要更高的效果、更快的速度，并计划用于商业用途，我们强烈推荐使用 [Face Swap Pro](https://vmodel.ai/models/vmodel/photo-face-swap-pro/)。

---

## 致谢

本项目的诞生离不开以下优秀的开源社区和项目：
* **roop**: 提供了项目的基础。
* **insightface**: 提供了强大的人脸分析模型。
* **TencentARC (GFPGAN)**: 提供了卓越的人脸修复算法。
* **Replicate (Cog)**: 提供了便捷的模型部署工具。
