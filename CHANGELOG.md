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

### Changed
- 将空的 `.gitignore` 文件更新为包含完整忽略规则的版本

### Technical Details
- 针对 Python + Pygame 游戏项目优化
- 支持现代Python包管理工具（特别是uv）
- 包含游戏开发特定的文件类型忽略
- 遵循Python社区最佳实践 