import os
import log  # 复用你的日志模块


def is_file_exists(file_path: str, log_head: str = "文件校验") -> bool:
	"""
	独立的文件存在性判断函数（支持相对/绝对路径，跨平台兼容）
	:param file_path: 待校验的文件路径（字符串）
	:param log_head: 日志前缀（便于区分模块）
	:return: True=存在 / False=不存在
	"""
	# 防护1：空路径直接返回False
	if not file_path or not isinstance(file_path, str):
		log.log("error", f"[{log_head}]", f"文件路径为空/非字符串 | 传入路径:{file_path}", error=3)
		return False
	
	try:
		# 步骤1：标准化路径（处理跨平台分隔符、相对路径）
		normalized_path = os.path.normpath(file_path)
		# 步骤2：转换为绝对路径（避免当前工作目录影响）
		absolute_path = os.path.abspath(normalized_path)
		
		# 步骤3：判断文件是否存在（且是文件，不是文件夹）
		if os.path.exists(absolute_path) and os.path.isfile(absolute_path):
			log.log(f"{log_head}", f"文件存在", f"文件存在 | 原始路径:{file_path} → 绝对路径:{absolute_path}")
			return True
		else:
			log.log("error", f"[{log_head}]",
			        f"文件不存在/不是文件 | 原始路径:{file_path} → 绝对路径:{absolute_path}", error=5)
			return False
	
	except Exception as e:
		# 捕获路径解析异常（如非法字符、权限问题）
		log.log("error", f"[{log_head}]", f"文件路径校验失败 | 路径:{file_path} → 错误:{str(e)}", error=10)
		return False