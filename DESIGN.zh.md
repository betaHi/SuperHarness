# 🔱 Super Harness — 设计文档

## 为什么做 Super Harness？

### 问题

单 Agent 做复杂编码任务有三个致命缺陷：

1. **Context Anxiety** — Agent 的上下文窗口填满后会"焦虑"，开始草草收工、偷工减料。Anthropic 在 Sonnet 4.5 上明确观测到了这一现象。

2. **自评偏乐观** — 让 Agent 评价自己写的代码，它永远说"写得很好"。就像让学生给自己打分——没人会给自己不及格。Anthropic 的实验证实：Agent 自评时会"confidently praising the work—even when the quality is obviously mediocre"。

3. **长任务失控** — 超过一定复杂度后，单 Agent 会跑偏、丢功能、stub 实现。Anthropic 的对比实验：单 Agent $9/20min 产出的核心功能是坏的；三 Agent $125/4h 产出的功能完整可用。

### 解决方案

**分离角色，各司其职。**

借鉴 Anthropic 的 GAN 式架构（Generator + Evaluator 对抗），加上 Planner 做前期拆解，形成三 Agent 流水线。核心洞察：

> **"分离做和评"是最关键的杠杆。** 独立的 Evaluator 比 Generator 自评严格 10 倍，而且更容易校准。

## 架构设计

```
User: "Build X"
     │
     ▼
┌─────────────────────┐
│ Phase 1: Parse      │ ← 解析任务，判断复杂度
│ Phase 2: Setup      │ ← 创建 .harness/handoff/ 工作空间
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Phase 3: Planner    │ ← 扩展任务为 Spec（复杂任务）
│ 📋 spec.md          │   跳过（简单任务）
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Phase 4: Generator  │ ← Claude Code / Codex 写代码
│ 🐯 implementation.md│
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Phase 5: Evaluator  │ ← 独立 Review，严格评判
│ 🔱 review.md        │
└─────────┬───────────┘
          │
     PASS?├── YES → Phase 6: Report ✅
          │
          └── NO → 回到 Generator 修复
                   （最多 2 轮，然后上报人类）
```

## 为什么这样设计？

### 1. 文件通信（File-based Handoff）

**为什么不用 Agent 间直接对话？**

- 文件可追溯、可 debug —— 出了问题翻文件就知道哪个环节出错
- 文件是持久的 —— Agent 重启、context reset 后依然可用
- 文件是结构化的 —— 比自然语言对话更精确
- Anthropic 和 Claude Code 都用这个模式（"Communication was handled via files"）

```
.harness/handoff/
├── task.md              # 任务描述
├── spec.md              # 产品规格
├── implementation.md    # 实现说明
├── review.md            # 代码审查
└── sprint-N-brief.md    # Sprint 范围
```

### 2. 智能复杂度路由

**为什么不统一走完整流水线？**

- 简单任务（改 bug）走完整流水线是浪费 —— $125 修一个 typo？
- 复杂任务跳过 spec 会跑偏 —— Anthropic 证实"没有 planner 模型会 under-scope"

所以做动态判断：
- **Simple** → 跳过 Spec，直接写代码
- **Medium** → 生成 Spec，单 Sprint
- **Complex** → 生成 Spec，多 Sprint

### 3. 最多 2 轮重试

**为什么不无限重试直到通过？**

- 无限重试 = 无限烧钱
- Anthropic 的经验：2-3 轮后改进趋于平缓
- 如果 2 轮都改不好，说明问题超出 Agent 能力，应该交给人类
- **Fail fast, escalate early** —— 机器解决不了的，趁早告诉人

### 4. Evaluator 独立且严格

**为什么不让 Generator 自己检查？**

Anthropic 的原话：
> "agents tend to respond by confidently praising the work—even when, to a human observer, the quality is obviously mediocre"

分离后的好处：
- Evaluator 可以单独调教为"严格"模式
- Generator 有了外部压力，会认真对待反馈
- 类似 GAN 的对抗训练 —— Generator 和 Evaluator 互相推动进步

### 5. Spec 不写实现细节

**为什么 Planner 只写高层设计？**

Anthropic 踩过的坑：
> "if the planner tried to specify granular technical details upfront and got something wrong, the errors in the spec would cascade into the downstream implementation"

Spec 应该说 **做什么**，不说 **怎么做**。实现细节交给 Generator 自己决定。

### 6. Harness 要能简化

**为什么设计为可拆卸的模块？**

Anthropic 最重要的教训：
> "every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing"

- 4.5 时代需要 Sprint 拆分 → 4.6 不需要了
- 4.5 需要 Context Reset → 4.6 不需要了
- 今天的必要组件可能是明天的累赘

所以每个阶段都可以用 flag 跳过（`--no-spec`, `--no-review`），方便随模型升级而简化。

## 目标用户

1. **独立开发者** — 一个人干活但想要 Code Review 和质量保证
2. **小团队** — 用 Agent 替代缺少的角色（PM 写 spec、Senior 做 review）
3. **学习者** — 通过 Agent 生成的 spec 和 review 学习最佳实践

## 用途场景

| 场景 | 命令 | 走哪些阶段 |
|------|------|-----------|
| 修 Bug | `/super-harness "Fix null check in auth.ts" --no-spec` | Code → Review |
| 新功能 | `/super-harness "Add JWT authentication"` | Spec → Code → Review |
| 大重构 | `/super-harness "Refactor payment module to microservice" --sprint multi` | Spec → Multi-Sprint Code → Review |
| 只要设计 | `/super-harness "Design caching layer" --spec-only` | Spec only |
| 快速原型 | `/super-harness "Build a todo app" --no-review` | Spec → Code |

## Roadmap

| 版本 | 特性 | 状态 |
|------|------|------|
| V1 | Spec → Code → Review 基础流水线 | ✅ 当前 |
| V2 | 自动化测试 Agent（跑测试，不只看代码） | 🔧 计划中 |
| V3 | Playwright UI 验收（前端任务） | 🔧 计划中 |
| V4 | 动态 Agent 选择（根据任务类型选最合适的 Agent） | 💭 构想中 |
| V5 | Sprint 合同机制（Generator 和 Evaluator 先协商完成标准） | 💭 构想中 |

## 参考资料

- [Anthropic: Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) — 三 Agent 架构的理论基础
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — "find the simplest solution possible"
- [Claude Code Source Architecture](https://github.com/instructkr/claude-code) — coordinator/, AgentTool, TeamCreateTool 的工程实现
- [OpenClaw gh-issues Skill](https://github.com/openclaw/openclaw) — sub-agent 编排的实战参考
