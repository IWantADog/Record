# about poetry

## poetry use

- init
- new
- show
	- `--tree`
- add
	- git
- remove
- install
- shell
- update
	- `--lock`
- build
	- wheel
- export
	- requirement.txt
- config
	- virtualenvs.in-project: 在项目文件夹下的`.venv`创建虚拟环境

### 基本的概念

- 当不存在`poetry.lock`时`poetry install`会根据`pyproject.toml`安装所有的的依赖，并将安装后所有的依赖的版本写入`poetry.lock`
- 当已存在`poetry.lock`，`poetry install`会完全根据`poetry.lock`安装所有依赖
- `poetry.lock`应该被提交到版本管理工具中
- `poetry update`根据`pyproject.toml`更新可更新的依赖版本，并将新版本的信息写入`poetry.lock`

### dependency specification

- caret requirements: `^1.1.1`
- tilde requirements: `~1.1.1`
- wildcard requirements: `1.*`
- inequality requirements: `>= 1.1.1`
- exact requirements: `1.1.1`
- git dependencies:
	- requests = { git = "xxxxxx"}
		- branch
		- rev
		- tag