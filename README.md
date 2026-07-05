# my-skills

Claude Code 自定义技能合集，用于保存和同步个人 AI 辅助开发工作流。

Personal Claude Code skills for a repeatable AI-assisted development workflow.

## Skills

| Skill | Description |
| --- | --- |
| [`gemini-analyzer`](./gemini-analyzer/SKILL.md) | 使用 Gemini CLI 的大上下文窗口分析大型文件与代码库 |

## 安装 | Installation

```bash
git clone https://github.com/Wonham/my-skills.git
mkdir -p ~/.claude/skills
cp -R my-skills/gemini-analyzer ~/.claude/skills/
```

重启 Claude Code 后即可使用已安装的技能。新设备的完整配置步骤见 [`SETUP.md`](./SETUP.md)。

Restart Claude Code after copying the skill. See [`SETUP.md`](./SETUP.md) for the complete workstation setup.

## 环境依赖 | Requirements

- [Claude Code](https://github.com/anthropics/claude-code)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)（`gemini-analyzer` 需要）
- Node.js 18+

## Repository Structure

```text
my-skills/
├── gemini-analyzer/
│   ├── SKILL.md
│   └── evals/
├── SETUP.md
└── README.md
```

## License

[MIT](./LICENSE)
