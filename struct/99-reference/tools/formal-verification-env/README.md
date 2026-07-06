# 形式化验证自动化环境

> **定位**: 为 `struct/07-formal-verification` 中的 TLA+、Alloy、Coq/Isabelle 规约提供可复现的自动化验证环境
> **决策**: 按 `SUBSEQUENT_PLAN_2026.md` 决策 2A 建立 Docker 化环境，所有新增形式化规约必须通过本环境至少一种工具验证
> **版本**: 2026-06-06

---

## 1. 环境总览

| 工具 | 版本 | 用途 | 官方来源 |
|------|------|------|----------|
| TLA+ Toolbox | 1.7.x | TLC 模型检测、PlusCal 语法检查 | [TLA+ Home](https://lamport.azurewebsites.net/tla/tla.html) |
| Alloy Analyzer | 6.x | 关系逻辑约束求解 | [Alloy Tools](https://alloytools.org) |
| Coq | 8.19+ | 构造性定理证明 | [Coq](https://coq.inria.fr) |
| Isabelle/HOL | 2024 | 高阶逻辑定理证明 | [Isabelle](https://isabelle.in.tum.de) |

---

## 2. 快速启动（Docker Compose）

### 2.1 前置要求

- Docker Engine 24.0+
- Docker Compose 2.20+
- 至少 4GB 可用内存（Isabelle 启动需要）

### 2.2 启动全部服务

```bash
cd struct/99-reference/tools/formal-verification-env
docker compose up -d
```

### 2.3 验证容器健康状态

```bash
docker compose ps
docker compose logs -f tla-plus
```

### 2.4 进入交互式 Shell

```bash
# TLA+
docker compose exec tla-plus bash

# Alloy
docker compose exec alloy bash

# Coq
docker compose exec coq bash

# Isabelle
docker compose exec isabelle bash
```

---

## 3. 运行现有规约

### 3.1 TLA+ 案例

```bash
# 进入容器
docker compose exec tla-plus bash

# 运行 payment-service.tla 的 TLC 模型检测
cd /work/07-formal-verification/01-tla-plus
tlc payment-service.tla -deadlock

# 运行 MCP 能力协商规约
tlc mcp-capability-negotiation.tla -deadlock

# 运行 A2A Task 生命周期
tlc a2a-task-lifecycle.tla -deadlock
```

### 3.2 Alloy 案例

```bash
# 进入容器
docker compose exec alloy bash

# 运行组件依赖无环性验证
cd /work/07-formal-verification/02-alloy
alloy component-dependency.als

# 运行 MCP Tool 图验证
alloy mcp-tool-graph.als

# 运行跨层映射
alloy cross-layer-mapping.als

# 运行 ISA-95 层次一致性
alloy isa95-hierarchy.als
```

### 3.3 Coq/Isabelle（占位，等待 Phase 2 补充）

```bash
# Coq 交互式证明
docker compose exec coq bash
coqtop -l /work/07-formal-verification/03-coq-isabelle/example.v

# Isabelle 批处理
docker compose exec isabelle bash
isabelle build -D /work/07-formal-verification/03-coq-isabelle
```

---

## 4. 目录挂载

本环境将项目根目录挂载到容器的 `/work`，因此可以直接读写 `struct/07-formal-verification` 下的所有文件。

```yaml
volumes:
  - ../../../../:/work:rw
```

---

## 5. 新增规约的验收标准

任何提交到 `07-formal-verification` 的新规约必须满足：

1. **TLA+ 规约**: 必须通过 `tlc` 语法检查（SANY）和至少一个模型检测场景
2. **Alloy 模型**: 必须在 Alloy Analyzer 中可执行，且至少提供一个可运行的 `run` 或 `check` 命令
3. **Coq/Isabelle 证明**: 必须提供 `.v` 或 `.thy` 文件，且能通过 `coqc` 或 `isabelle build`
4. **文档**: 必须在同目录下提供 `.md` 说明文件，列出验证命令和预期结果

---

## 6. CI 集成建议

在 GitHub Actions / GitLab CI 中可添加以下步骤：

```yaml
- name: Run TLA+ specs
  run: |
    docker compose -f struct/99-reference/tools/formal-verification-env/docker-compose.yml up -d
    docker compose exec -T tla-plus bash -c "cd /work/07-formal-verification/01-tla-plus && tlc payment-service.tla -deadlock"
    docker compose down
```

---

## 7. 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| TLC 报 Java OOM | 状态空间过大 | 增加 Docker 内存限制或简化模型 |
| Alloy 无法启动 GUI | 容器无显示器 | 使用命令行 `alloy` 或导出 X11 |
| Isabelle 构建超时 | 首次编译依赖 | 预先生成 Heap 镜像 |
| Coq 版本不兼容 | 库依赖版本差异 | 锁定 `coq-8.19` 镜像标签 |

---

## 8. 参考链接

- Leslie Lamport. *Specifying Systems*. <https://lamport.azurewebsites.net/tla/book.html>
- Daniel Jackson. *Software Abstractions*. <https://softwareabstractions.org/>
- Coq Documentation. <https://coq.inria.fr/documentation>
- Isabelle Documentation. <https://isabelle.in.tum.de/documentation.html>

---

> 最后更新: 2026-06-06


---

## 补充说明：形式化验证自动化环境

## 概念定义

**定义**：参考层是结构化知识体系的“地图”，汇总权威来源、术语表、标准索引、课程对标与审计报告，为各主题提供可追溯的引用与一致性校验。

## 反例

**反例**：参考层链接长期不更新，术语表与正文定义冲突，读者无法确认内容准确性与时效性。

## 权威来源

> **权威来源**:
>
> - [ISO](https://www.iso.org)
> - [IEEE Standards](https://standards.ieee.org)
> - [NIST](https://www.nist.gov)
> - [CNCF](https://www.cncf.io)
> - 核查日期：2026-07-07
