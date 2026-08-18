# my-skills

Codex / Claude Code 自定义技能合集，用于保存和同步个人 AI 辅助开发工作流。

Personal Codex and Claude Code skills for a repeatable AI-assisted development workflow.

## Skills

| Skill | Description |
| --- | --- |
| [`gemini-analyzer`](./gemini-analyzer/SKILL.md) | 使用 Gemini CLI 的大上下文窗口分析大型文件与代码库 |
| [`blender-cli-modeling`](./blender-cli-modeling/SKILL.md) | 通过 Blender CLI 和 `bpy` 完成建模、渲染、导出与结果验证 |

## 安装 | Installation

```bash
git clone https://github.com/Wonham/my-skills.git
mkdir -p ~/.claude/skills
cp -R my-skills/gemini-analyzer ~/.claude/skills/

mkdir -p ~/.codex/skills
cp -R my-skills/blender-cli-modeling ~/.codex/skills/
```

重启对应的 Agent 应用后即可使用已安装的技能。新设备的完整配置步骤见 [`SETUP.md`](./SETUP.md)。

Restart the corresponding agent application after copying a skill. See [`SETUP.md`](./SETUP.md) for the complete workstation setup.

## 环境依赖 | Requirements

- [Codex](https://openai.com/codex/) (`blender-cli-modeling`)
- [Claude Code](https://github.com/anthropics/claude-code)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)（`gemini-analyzer` 需要）
- [Blender](https://www.blender.org/) 5.2 LTS（`blender-cli-modeling` 已验证版本）
- Node.js 18+

## Repository Structure

```text
my-skills/
├── gemini-analyzer/
│   ├── SKILL.md
│   └── evals/
├── blender-cli-modeling/
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   └── scripts/
├── SETUP.md
└── README.md
```

## License

[MIT](./LICENSE)
