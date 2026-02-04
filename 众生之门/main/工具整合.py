#------------------------- 导入 ---------------------------
import gc
import json
import os
import sys
import time
import traceback
from typing import *
from typing import Any, Optional, Dict, Union

import ursina
from ursina.shaders import lit_with_shadows_shader

#------------------------ 错误 ---------------------------
class ConfigPathNotError(Exception):
	"""配置文件无法读取异常"""
	pass


class FontFileIsForgetError(Exception):
	"""字体文件不存在异常"""
	pass


class UserConfigFileError(Exception):
	"""用户配置文件内容错误异常"""
	pass


class JsonParseError(Exception):
	"""JSON配置解析失败异常"""
	pass

# ---------------- 路径配置----------------------------
# 获取运行文件（主程序入口）的目录（所有相对路径都基于此）
RUN_FILE_PATH = sys.argv[0]  # 运行文件路径（如 main.py）
RUN_DIR = os.path.dirname(os.path.abspath(RUN_FILE_PATH))  # 运行文件所在目录

# 基于运行文件目录拼接配置路径（所有相对路径都以此为基准）
config = os.path.join(RUN_DIR, "./config/")
UserConfig = os.path.join(RUN_DIR, "./USERCONFIG/")

