# TCM Career Perspective Skills

一组面向中医学博士职业决策的可运行 Codex Skills。仓库采用“人物视角独立保存 + 圆桌总控综合”的结构，避免把不同人物的判断混成一个模糊的万能顾问。

## Included Skills

| Skill | 主要用途 |
| --- | --- |
| `wang-qi-perspective` | 从临床差异、体质学、长期问题和个人学术体系审视方向 |
| `huang-luqi-perspective` | 审计战略问题、PI、平台资源、现代科学转译和青年独立性 |
| `zhang-boli-perspective` | 审视临床价值、守正创新、证据校正、任务闭环和平台建设 |
| `william-osler-perspective` | 守住患者接触、床旁判断、医生身份及临床科研教学循环 |
| `richard-hamming-perspective` | 判断重要且可攻的问题、优秀同行、问题所有权和长期独立性 |
| `tcm-phd-career-roundtable` | 用统一事实卡让五个视角独立判断，再汇总共识、分歧和条件式排序 |

`zhang-boli-perspective` 是内部终检分支规范化后的公开发行副本。早期实验分支不在本仓库发布，也不参与运行。

## Install

将需要的 Skill 文件夹复制到 Codex 的 skills 目录。若希望使用圆桌功能，建议安装全部六个文件夹。以下命令在未设置 `$env:CODEX_HOME` 时自动使用 `$HOME\.codex`：

```powershell
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$skillsHome = Join-Path $codexHome 'skills'
New-Item -ItemType Directory -Force -Path $skillsHome | Out-Null
Copy-Item -Recurse .\skills\wang-qi-perspective $skillsHome
Copy-Item -Recurse .\skills\huang-luqi-perspective $skillsHome
Copy-Item -Recurse .\skills\zhang-boli-perspective $skillsHome
Copy-Item -Recurse .\skills\william-osler-perspective $skillsHome
Copy-Item -Recurse .\skills\richard-hamming-perspective $skillsHome
Copy-Item -Recurse .\skills\tcm-phd-career-roundtable $skillsHome
```

也可以只安装单个人物 Skill，以获得更纯粹、可追溯的单视角建议。

## Usage

单视角示例：

```text
请用 Richard Hamming 视角比较这两个实验室。先区分已知事实、推断和未知项，再判断问题重要性、问题所有权、优秀同行密度与两年后可带走的资产。
```

圆桌示例：

```text
请使用 tcm-phd-career-roundtable。先把我的每个选项改写为具体 offer 包，列出缺失事实；再让五个视角基于同一事实卡独立判断，最后给出共识、关键分歧、否决条件、条件式排序和下一轮尽调问题。
```

## Design Principles

- 人物视角只提供公开材料可支持的思维框架，不声称代表人物本人或其私下意见。
- 事实层与价值判断层分开。岗位、PI、合同、签证、执业、基金和薪酬必须另行核验。
- 保留分歧，不用多数票制造虚假共识。
- 比较具体机会包，而不是比较“海外”“高校”“医院”等抽象标签。
- 结论应是带条件、触发器和退出机制的决策，而不是终身预言。

## Validation

```powershell
python .\scripts\validate_skills.py
```

校验会检查 Skill 目录结构、frontmatter、内部链接、安装元数据和公开仓库敏感信息。原始蒸馏测试记录因含本地路径及个案化场景，不在本仓库发布。

三项隔离前向测试及复现标准见 [docs/forward-tests.md](docs/forward-tests.md)。

## Status

建议先以私有仓库完成远端复核、来源抽查和前向测试，再由仓库所有者决定是否公开。实际发布状态以 GitHub 仓库可见性为准。

## License And Notice

本仓库原创内容采用 MIT License。女娲 Skill 生成框架的 MIT 归属保留在 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)；引用来源及人物姓名、著作、机构材料的权利仍归各自权利人所有。详见 [NOTICE.md](NOTICE.md)。
