# Pearl on SaladCloud

Linux AMD64 / NVIDIA GPU image with WildRig Multi **0.51.2**, downloaded from its upstream release and SHA-256 checked. Pool defaults to `pool.pearlhash.xyz:9000`.

## SaladCloud 设置

镜像地址：`ghcr.io/entropic-silence/pearl-salad:latest`。首次发布后必须将 GitHub Packages 中的包可见性设为 Public，方可免登录拉取；仓库公开不代表包自动公开。

1. Image Source 选 Public Registry，粘贴镜像地址；保留 Image Caching。
2. Replicas 先填 **1**。选择 NVIDIA RTX GPU，初测建议 RTX 3090 或 4090；2 vCPU、8 GiB RAM 作为初始资源设置，按实测调整。RTX 50 系列需要匹配 CUDA 12.8 的主机驱动，先验证单卡。
3. Environment Variables 添加 `WALLET=你的prl1开头钱包地址`。可选 `WORKER_PREFIX=salad`（只用字母、数字、连字符，最多10字符）。无需设置 WORKER。
4. Command/Arguments 留空，使用镜像入口。Networking/Container Gateway 关闭，健康探针先关闭。本程序仅向矿池发起出站连接，不提供 HTTP 服务。
5. 启动并看日志：确认钱包、矿池、矿工名正确，GPU 被识别且有 accepted shares。容器 Running 不能证明成功挖矿。用矿池钱包页面核对矿工和有效算力。
6. 单卡验证成功后，把同一组 Replicas 从 **1 改为 10**。每个副本使用独立 GPU；无需新建10组或改钱包。费用随运行副本数增加。

矿工名由前缀、机器ID摘要、96位随机后缀组成；即使同一机器运行多个组也极难重名。每次容器重启会生成新名称，矿池可能暂时保留旧离线矿工记录。内部断线重连保持名称。不要把10个副本设置为固定同名矿工。

## 参数

| 环境变量 | 默认值 | 说明 |
| --- | --- | --- |
| WALLET | 必填 | Pearl 收款地址，不是网址；不需要私钥 |
| POOL | pool.pearlhash.xyz:9000 | 出站矿池地址 |
| WORKER_PREFIX | salad | 可用于区分不同容器组 |
| DRY_RUN | 关闭 | 设为1仅打印参数并退出，实际部署不要设置 |

进程由 WildRig 接管 PID 1，容器停止信号直接到矿工。矿工自身重连；watchdog 触发退出后依赖平台重启容器。镜像不修改主机超频、风扇或功耗参数，不启动 CPU 挖矿。

## 构建验证

GitHub Actions 只构建镜像、运行参数测试、`--help` 和 dry-run，不挖矿。没有 GPU 的 CI 无法验证实际算力或矿池 accepted shares，须在首个 Salad GPU 实例上验证。下载固定版本，不在运行时自动升级。

如果出现 `libcuda`、OpenCL 或驱动错误，检查是否选择 NVIDIA GPU 并查看完整日志；CUDA 12.8 基础镜像需要兼容的宿主驱动。如无法连接矿池，检查日志中的 DNS/连接错误与矿池状态。高 rejected 比例时先停止扩容并排查版本、网络和 GPU。

上游矿工为第三方二进制，本仓库是容器封装；上游说明保存在镜像 `/opt/miner/readme.txt`。不承诺收益。

## 来源

- https://pearlhash.xyz/
- https://github.com/andru-kun/wildrig-multi/releases/tag/0.51.2
- https://docs.salad.com/container-engine/explanation/infrastructure-platform/networking
- https://docs.salad.com/container-engine/explanation/core-concepts/architectural-overview
