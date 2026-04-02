# Claude Code 配置清单

用于在新设备上同步相同的 Claude Code 环境。

## 已启用的插件

这些是来自官方插件源的插件，通过 settings.json 启用：

| 插件名称 | 用途 |
|---------|------|
| `superpowers` | 高级开发工作流技能（调试、代码审查、测试驱动开发等） |
| `skill-creator` | 创建、编辑和测试 Claude Code skills |
| `frontend-design` | 创建高质量的前端界面和组件 |
| `claude-md-management` | 管理和改进 CLAUDE.md 文件 |
| `github` | GitHub 集成，通过 MCP 提供 GitHub 能力 |

## 自定义技能

| 技能名称 | 来源 | 用途 |
|---------|------|------|
| `gemini-analyzer` | [my-skills](https://github.com/Wonham/my-skills) | 使用 Gemini CLI 分析大型代码库（100KB+ 文件、完整目录分析） |

## 设置文件配置

`~/.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "你的API密钥",
    "ANTHROPIC_BASE_URL": "https://ark.cn-beijing.volces.com/api/coding",
    "ANTHROPIC_MODEL": "glm-4.7",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  },
  "enabledPlugins": {
    "frontend-design@claude-plugins-official": true,
    "claude-md-management@claude-plugins-official": true,
    "skill-creator@claude-plugins-official": true,
    "superpowers@claude-plugins-official": true,
    "github@claude-plugins-official": true
  }
}
```

## 在新设备上设置的步骤

### 1. 安装 Claude Code CLI
按照官方文档安装 Claude Code。

### 2. 配置 settings.json
将上述 `settings.json` 内容复制到 `~/.claude/settings.json`，并替换 `ANTHROPIC_AUTH_TOKEN` 为你的实际密钥。

### 3. 安装自定义技能
```bash
# 克隆配置仓库
git clone https://github.com/Wonham/my-skills ~/temp-skills

# 复制技能到 Claude 技能目录
cp -r ~/temp-skills/gemini-analyzer ~/.claude/skills/

# 清理临时文件
rm -rf ~/temp-skills
```

### 4. 验证配置
启动 Claude Code 并运行：
```bash
/技能列表
# 应该能看到所有启用的技能
```

## 环境依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| Node.js | >=18 | 某些插件运行需要 |
| gemini CLI | 最新版 | gemini-analyzer skill 需要 |
| git | 任意 | 版本控制 |

## 更新配置清单

当你添加新的插件或技能时，请更新此文件并提交到仓库。
