# my-skills

个人使用的 Agent Skills 仓库。

| Skill | 独立仓库 | 简介 |
|---|---|---|
| `blender-cli-modeling` | [Wonham/blender-cli-modeling](https://github.com/Wonham/blender-cli-modeling) | 通过 Blender CLI、`bpy` 与可选 MCP 创建、编辑和验证 Blender 场景 |
| `lumerical-ldf-reader` | [Wonham/lumerical-ldf-reader](https://github.com/Wonham/lumerical-ldf-reader) | 在未安装 Lumerical 的机器上读取和导出已验证的 `.ldf` D-card 数据 |
| `gemini-analyzer` | [Wonham/lumerical-ldf-reader](https://github.com/Wonham/lumerical-ldf-reader) | 在未安装 Lumerical 的机器上读取和导出已验证的 `.ldf` D-card 数据 |


## 仓库管理原则

- 可公开复用、需要长期维护的 Skill：迁移到独立公开仓库。
- 尚在探索或未完全成熟的自定义 Skill：暂存于本仓库。
- 已迁移的 Skill：这里只保留链接，不保留重复版本。
- 历史内容：仍可通过 Git 提交记录追溯。

## 安装

克隆本仓库中的孵化 Skill：

```zsh
git clone https://github.com/Wonham/my-skills.git
```

然后把所需 Skill 目录复制或链接到智能体平台的 Skills 目录。以 `gemini-analyzer` 为例：

```zsh
cp -R my-skills/gemini-analyzer ~/.claude/skills/
```

独立维护的 Skill 请使用上方表格中的仓库地址安装。不同智能体平台的注册方式可能不同，但 Skill 根目录应包含 `SKILL.md`。

更完整的个人环境说明见 [`SETUP.md`](./SETUP.md)。

## 当前结构

```text
my-skills/
├── gemini-analyzer/
│   └── SKILL.md
├── SETUP.md
├── LICENSE
└── README.md
```

## License

[MIT](./LICENSE)
