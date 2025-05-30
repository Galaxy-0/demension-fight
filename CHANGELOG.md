# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 完善的 `.gitignore` 文件，包含以下忽略规则：
  - Python 开发相关文件（__pycache__, *.pyc, 虚拟环境等）
  - 游戏开发特定文件（资源文件、存档、配置等）
  - 开发工具和IDE文件（.vscode, .idea, .DS_Store等）
  - 包管理器文件（支持uv, pip, poetry等）
  - 测试和覆盖率报告文件
  - 系统临时文件和日志文件

### Fixed
- 修复音频文件加载错误：添加文件存在性检查，避免在音频文件不存在时抛出 FileNotFoundError
- 改进错误处理：当音频文件缺失时显示友好的信息提示而不是崩溃
- 修复中文字体显示问题：将所有游戏界面文本改为英文以解决字体渲染问题
- 完善国际化：修复"How to Play"界面、折叠按钮状态标签、重新开始提示等遗漏的中文文本

### Changed
- 将空的 `.gitignore` 文件更新为包含完整忽略规则的版本
- 在 main.py 中添加 os 模块导入以支持文件存在性检查
- 国际化改进：将游戏标题、菜单项、状态文本、按钮标签等全部改为英文
- 游戏窗口标题从"维度折叠棋"改为"Dimensional Folding Tic-Tac-Toe"

### Technical Details
- 针对 Python + Pygame 游戏项目优化
- 支持现代Python包管理工具（特别是uv）
- 包含游戏开发特定的文件类型忽略
- 遵循Python社区最佳实践
- 增强了游戏的健壮性，即使缺少音频资源也能正常运行 