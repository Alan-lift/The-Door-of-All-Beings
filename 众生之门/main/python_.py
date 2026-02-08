import sys


def print(*args, sep=' ', end='\n', file=sys.stdout, flush=False, write=False):
	"""
	模拟Python内置print函数的实现
	:param write: 是否打印
	:param args: 要打印的任意数量参数
	:param sep: 参数之间的分隔符，默认空格
	:param end: 打印结束符，默认换行
	:param file: 输出流对象，默认标准输出
	:param flush: 是否强制刷新缓冲区，默认False
	"""
	str_args = [str(arg) for arg in args]
	# 2. 用分隔符拼接所有参数
	output = sep.join(str_args)
	# 3. 添加结束符
	output += end
	if write:
		try:
			# 4. 写入指定输出流
			file.write(output)
			# 5. 按需刷新缓冲区
			if flush:
				file.flush()
		except Exception as e:
			# 捕获并抛出与内置print一致的异常类型
			raise IOError(f"打印失败: {e}") from e

