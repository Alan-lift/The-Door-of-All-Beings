import time
import random
import sys
sys.set_int_max_str_digits(10000)

def 提取(s: str) -> int:
	"""提取字符串中的所有数字并转换为整数"""
	numbers = ''.join(filter(str.isdigit, s))
	return int(numbers) if numbers else 0


def 设置随机种子(input_data: str):
	"""根据输入数据提取的数字设置随机种子"""
	种子数字 = 提取(input_data)
	
	# 如果没有数字，使用默认种子
	if 种子数字 == 0:
		种子数字 = 123456789
	
	# 设置随机种子
	random.seed(种子数字)
	return 种子数字


def 转换(input_data: str) -> str:
	"""
	多层固定混淆转换（增强随机版）
	使用输入字符串提取的数字作为随机种子
	"""
	# 设置随机种子
	原始种子 = 设置随机种子(input_data)
	
	# ========== 第一层：基础替换 ==========
	# 随机选择替换顺序
	基础替换表 = [
		("1", "#¸\\"),
		("2", "¸‰/"),
		(".", "5*/¸\\3"),
		("4", "¸n"),
		("0", "¸ò")
	]
	random.shuffle(基础替换表)
	
	for old, new in 基础替换表:
		input_data = input_data.replace(old, new)
	
	# ========== 第二层：数字扩展混淆 ==========
	num_replacements = {
		"3": ["δ∞π", "³∛∜", "③⓷❸"],
		"5": ["ξψω", "⁵√∛", "⑤⓹❺"],
		"6": ["∇∂∫", "⁶∛∜", "⑥⓺❻"],
		"7": ["∮≠≈", "⁷√∛", "⑦⓻❼"],
		"8": ["≡≤≥", "⁸∛∜", "⑧⓽❽"],
		"9": ["⊕⊗⊙", "⁹√∛", "⑨⓾❾"]
	}
	
	for num, replacements in num_replacements.items():
		# 随机选择一种替换
		replacement = random.choice(replacements)
		input_data = input_data.replace(num, replacement)
	
	# ========== 第三层：字母混淆（如果存在） ==========
	# 随机选择字母替换的版本
	letter_versions = [
		{  # 版本1：希腊字母为主
			"a": "α∀â", "b": "β∃b̃", "c": "γ∈ç", "d": "δ∉đ", "e": "ε∊ê",
			"f": "φ∴ƒ", "g": "η∵ĝ", "h": "θ∼ħ", "i": "ι↔î", "j": "κ⇔ĵ",
			"k": "λ∧ǩ", "l": "μ∨ł", "m": "ν¬m̃", "n": "ξ∩ñ", "o": "ο∪ô",
			"p": "π⊂ṕ", "q": "ρ⊃q̃", "r": "σ⊆ŕ", "s": "τ⊇ś", "t": "υ∈t̃",
			"u": "φ∋û", "v": "χ∅ṽ", "w": "ψ∇ŵ", "x": "ω∂x̂", "y": "ζ∫ŷ",
			"z": "θ∮ẑ", "A": "ΑÂÃ", "B": "ΒB̃B̄", "C": "ΓÇÇ", "D": "ΔÐĎ",
			"E": "ΕÊË", "F": "ΦF̃F̄", "G": "ΓĜĞ", "H": "ΗĤḨ", "I": "ΙÎÏ",
			"J": "ΘĴJ̃", "K": "ΚǨK̄", "L": "ΛĹĻ", "M": "ΜM̃M̄", "N": "ΝÑŃ",
			"O": "ΟÔÕ", "P": "ΠṔP̄", "Q": "ΞQ̃Q̄", "R": "ΡŔŖ", "S": "ΣŚŞ",
			"T": "ΤŢT̄", "U": "ΥÛŨ", "V": "ΦṼV̄", "W": "ΩŴW̃", "X": "ΞX̂X̄",
			"Y": "ΨŶŸ", "Z": "ΖẐZ̄"
		},
		{  # 版本2：数学符号为主
			"a": "∀αå", "b": "∃βß", "c": "∈γç", "d": "∂δđ", "e": "∃εê",
			"f": "ƒϕƒ", "g": "∇ηĝ", "h": "ℏθħ", "i": "∫ιî", "j": "∮ȷĵ",
			"k": "κκǩ", "l": "ℓλł", "m": "µμṃ", "n": "ηνñ", "o": "∅οô",
			"p": "ππṕ", "q": "√ρq̃", "r": "ρρŕ", "s": "σςś", "t": "ττṭ",
			"u": "∪υû", "v": "√νṽ", "w": "ωωŵ", "x": "×ξx̂", "y": "ψψŷ",
			"z": "ζζẑ", "A": "∀ÅĀ", "B": "ℬḄḆ", "C": "ℂÇĆ", "D": "ⅅÐĎ",
			"E": "∃ÊĒ", "F": "ℱḞḞ", "G": "ℊĜĞ", "H": "ℋĤḪ", "I": "ℐÎĪ",
			"J": "𝒥ĴJ̃", "K": "𝒦ǨḰ", "L": "ℒĹĻ", "M": "ℳṀṂ", "N": "ℕÑŃ",
			"O": "∅ÔŌ", "P": "ℙṔṖ", "Q": "ℚQ̃Ǫ", "R": "ℝŔŖ", "S": "𝕊ŚŞ",
			"T": "𝕋ŢṪ", "U": "⋃ÛŪ", "V": "√ṼṾ", "W": "𝒲ŴẂ", "X": "𝕏X̂Ẋ",
			"Y": "ΨŶŸ", "Z": "ℤẐŻ"
		},
		{  # 版本3：组合字符为主
			"a": "ãāă", "b": "b̃b̄b̆", "c": "c̃c̄c̆", "d": "d̃d̄d̆", "e": "ẽēĕ",
			"f": "f̃f̄f̆", "g": "g̃ḡğ", "h": "h̃h̄h̆", "i": "ĩīĭ", "j": "j̃j̄j̆",
			"k": "k̃k̄k̆", "l": "l̃l̄l̆", "m": "m̃m̄m̆", "n": "ñn̄n̆", "o": "õōŏ",
			"p": "p̃p̄p̆", "q": "q̃q̄q̆", "r": "r̃r̄r̆", "s": "s̃s̄s̆", "t": "t̃t̄t̆",
			"u": "ũūŭ", "v": "ṽv̄v̆", "w": "w̃w̄w̆", "x": "x̃x̄x̆", "y": "ỹȳy̆",
			"z": "z̃z̄z̆", "A": "ÃĀĂ", "B": "B̃B̄B̆", "C": "C̃C̄C̆", "D": "D̃D̄D̆",
			"E": "ẼĒĔ", "F": "F̃F̄F̆", "G": "G̃ḠĞ", "H": "H̃H̄H̆", "I": "ĨĪĬ",
			"J": "J̃J̄J̆", "K": "K̃K̄K̆", "L": "L̃L̄L̆", "M": "M̃M̄M̆", "N": "ÑN̄N̆",
			"O": "ÕŌŎ", "P": "P̃P̄P̆", "Q": "Q̃Q̄Q̆", "R": "R̃R̄R̆", "S": "S̃S̄S̆",
			"T": "T̃T̄T̆", "U": "ŨŪŬ", "V": "ṼV̄V̆", "W": "W̃W̄W̆", "X": "X̃X̄X̆",
			"Y": "ỸȲY̆", "Z": "Z̃Z̄Z̆"
		}
	]
	
	字母版本 = random.choice(letter_versions)
	for letter, replacement in 字母版本.items():
		input_data = input_data.replace(letter, replacement)
	
	# ========== 第四层：特殊符号扩展（随机版） ==========
	symbol_versions = [
		{  # 版本1
			"-": "–—−", "_": "‗_̲", "@": "＠@⃗", "/": "／⁄", "\\": "＼⧵",
			"|": "｜ǀ", ":": "：∶", ";": "；⁏", ",": "，‚", "?": "？¿",
			"!": "！¡", "(": "（〔", ")": "）〕", "[": "【〖", "]": "】〗",
			"{": "｛⦃", "}": "｝⦄", "<": "＜‹", ">": "＞›", "'": "＇´",
			'"': "＂¨", "`": "｀ˋ", "~": "～˜", "^": "＾ˆ", "&": "＆⅋",
			"*": "＊∗", "%": "％‰", "#": "＃♯", "+": "＋†", "=": "＝≂"
		},
		{  # 版本2
			"-": "‐‑‒", "_": "﹍﹎﹏", "@": "©®™", "/": "÷⁄∕", "\\": "﹨∖",
			"|": "‖∣∤", ":": "∶∷⁝", ";": "⁏⁏", ",": "‚„", "?": "¿⁇",
			"!": "¡‼⁉", "(": "〈〈", ")": "〉〉", "[": "⟦⟬", "]": "⟧⟭",
			"{": "⦃⦅", "}": "⦄⦆", "<": "≪⋘", ">": "≫⋙", "'": "ʻʼ",
			'"': "˝¨", "`": "ˋ˴", "~": "∼≈", "^": "ˆˇ", "&": "⅋⅋",
			"*": "∗∙", "%": "‰‱", "#": "♯♭", "+": "⊕⊞", "=": "≡≣"
		}
	]
	
	符号版本 = random.choice(symbol_versions)
	for symbol, replacement in 符号版本.items():
		input_data = input_data.replace(symbol, replacement)
	
	# ========== 第五层：位置变换混淆（随机参数） ==========
	chars = list(input_data)
	
	# 随机选择分组大小（3-6）
	分组大小 = random.choice([3, 4, 5, 6])
	for i in range(0, len(chars) - 分组大小 + 1, 分组大小):
		# 随机选择反转还是乱序
		if random.choice([True, False]):
			# 反转
			chars[i:i + 分组大小] = reversed(chars[i:i + 分组大小])
		else:
			# 随机打乱
			group = chars[i:i + 分组大小]
			random.shuffle(group)
			chars[i:i + 分组大小] = group
	
	input_data = ''.join(chars)
	
	# 随机选择变换方式
	变换方式 = random.choice([1, 2, 3])
	if 变换方式 == 1:
		# 奇偶位置分离再合并（先偶后奇）
		even_chars = [input_data[i] for i in range(0, len(input_data), 2)]
		odd_chars = [input_data[i] for i in range(1, len(input_data), 2)]
		input_data = ''.join(even_chars + odd_chars)
	elif 变换方式 == 2:
		# 反转整个字符串
		input_data = input_data[::-1]
	else:
		# 随机交换字符
		chars = list(input_data)
		for _ in range(len(chars) // 4):  # 交换次数
			i = random.randint(0, len(chars) - 1)
			j = random.randint(0, len(chars) - 1)
			chars[i], chars[j] = chars[j], chars[i]
		input_data = ''.join(chars)
	
	# 随机分段交换
	if len(input_data) >= 3:
		# 随机选择分段数（2-4段）
		段数 = random.choice([2, 3, 4])
		段长 = len(input_data) // 段数
		段列表 = []
		
		for i in range(段数):
			start = i * 段长
			end = (i + 1) * 段长 if i < 段数 - 1 else len(input_data)
			段列表.append(input_data[start:end])
		
		# 随机打乱段顺序
		random.shuffle(段列表)
		input_data = ''.join(段列表)
	
	# ========== 第六层：Unicode组合字符混淆（随机选择） ==========
	combining_sets = [
		["\u0300", "\u0301", "\u0302", "\u0303", "\u0304"],  # 声调
		["\u0306", "\u0307", "\u0308", "\u030a", "\u030b"],  # 变音符
		["\u030c", "\u0327", "\u0328", "\u0332", "\u0333"],  # 下加符
		["\u20d0", "\u20d1", "\u20d2", "\u20d3", "\u20d4"],  # 箭头
		["\u20d5", "\u20d6", "\u20d7", "\u20d8", "\u20d9"],  # 更多箭头
	]
	
	combining_chars = random.choice(combining_sets)
	
	# 随机选择插入频率（每隔n个字符）
	插入频率 = random.choice([2, 3, 4, 5])
	result_chars = []
	for i, char in enumerate(input_data):
		result_chars.append(char)
		if (i + 1) % 插入频率 == 0 and i < len(input_data) - 1:
			comb_char = random.choice(combining_chars)
			result_chars.append(comb_char)
	
	input_data = ''.join(result_chars)
	
	# ========== 第七层：零宽字符混淆（随机选择） ==========
	zw_sets = [
		["\u200b", "\u200c", "\u200d"],  # 基础零宽
		["\u200e", "\u200f", "\u2060"],  # 方向零宽
		["\u2061", "\u2062", "\u2063"],  # 数学零宽
		["\ufe0e", "\ufe0f"],  # 变体选择符
	]
	
	zw_chars = random.choice(zw_sets)
	
	if len(input_data) > 0:
		# 随机选择插入位置
		插入位置数 = random.randint(1, 5)
		for _ in range(插入位置数):
			pos = random.randint(0, len(input_data))
			zw_char = random.choice(zw_chars)
			input_data = input_data[:pos] + zw_char + input_data[pos:]
	
	# ========== 第八层：编码变换混淆（随机参数） ==========
	try:
		bytes_data = input_data.encode('utf-8')
		encoded_parts = []
		
		# 随机选择变换算法
		变换算法 = random.choice([1, 2, 3])
		
		for i, byte in enumerate(bytes_data):
			if 变换算法 == 1:
				# 加法变换
				变换值 = (byte + i + 原始种子) % 256
			elif 变换算法 == 2:
				# 异或变换
				变换值 = (byte ^ (i % 256) ^ (原始种子 % 256)) % 256
			else:
				# 乘法变换
				变换值 = (byte * (i % 128 + 1)) % 256
			
			encoded_parts.append(chr(变换值))
		
		input_data = ''.join(encoded_parts)
	except:
		pass
	
	# ========== 第九层：最终视觉混淆（随机选择） ==========
	final_replacement_sets = [
		{" ": "\u00a0\u2000\u2001", "-": "‐‑‒", ".": "．･・", ",": "‚¸"},
		{" ": "\u2002\u2003\u2004", "-": "–—―", ".": "︓︒", ",": "︐"},
	]
	
	final_replacements = random.choice(final_replacement_sets)
	for char, replacement in final_replacements.items():
		if char in input_data:
			# 随机替换几次
			替换次数 = random.randint(1, 3)
			input_data = input_data.replace(char, replacement[0], 替换次数)
	
	# ========== 第十层：长度标准化（随机参数） ==========
	# 随机选择目标长度倍数
	长度倍数 = random.choice([8, 16, 32])
	target_length = ((len(input_data) // 长度倍数) + 1) * 长度倍数
	
	if len(input_data) < target_length:
		# 随机选择填充字符集
		padding_sets = [
			"¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿",
			"①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳",
			"ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
			"ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ",
		]
		
		padding_chars = random.choice(padding_sets)
		padding_needed = target_length - len(input_data)
		padding = padding_chars * (padding_needed // len(padding_chars) + 1)
		input_data += padding[:padding_needed]
	elif len(input_data) > target_length:
		# 随机选择截断位置
		if random.choice([True, False]):
			# 从开头截断
			input_data = input_data[:target_length]
		else:
			# 从中间开始截断
			start = random.randint(0, len(input_data) - target_length)
			input_data = input_data[start:start + target_length]
	
	return input_data


def 加密(input_data: str) -> str:
	"""增强版加密函数，加入随机性"""
	# 设置随机种子
	种子数字 = 设置随机种子(input_data)
	
	output = ''
	output_ = ''
	input_data = 转换(input_data)
	
	# 随机选择处理顺序
	处理方式 = random.choice([1, 2, 3])
	
	if 处理方式 == 1:
		# 方式1：原始顺序
		for i in input_data:
			I_ = ord(i)
			i_ = str(I_)
			output = str(int(output + i_) + I_)
	elif 处理方式 == 2:
		# 方式2：先乘后加
		for i in input_data:
			I_ = ord(i)
			i_ = str(I_ * (种子数字 % 100 + 1))
			output = str(int(output + i_) + I_)
	else:
		# 方式3：异或处理
		for i in input_data:
			I_ = ord(i)
			i_ = str(I_ ^ (种子数字 % 256))
			output = str(int(output + i_) + I_)
	
	output = output[::-1]
	output = int(output)
	
	# 随机选择进制转换
	进制选择 = random.choice([8, 10, 16])
	if 进制选择 == 8:
		output = int(oct(output)[2::])
	elif 进制选择 == 16:
		output = int(hex(output)[2::], 16)
	# 10进制不变
	
	output = str(hex(output)[2::])
	
	# 第二个循环（随机变换）
	for i in output:
		I_ = ord(i)
		# 随机选择变换方式
		变换 = random.choice([1, 2, 3])
		if 变换 == 1:
			i_ = str(I_ + 种子数字 % 100)
		elif 变换 == 2:
			i_ = str(I_ * (种子数字 % 10 + 1))
		else:
			i_ = str(I_ ^ (种子数字 % 256))
		
		output_ = str(int(output_ + i_) + I_)
	
	output = output_
	output = output[::-1]
	output = int(output)
	output = int(oct(output)[2::])
	output = str(hex(output)[2::])
	
	# 第三个循环（更多随机性）
	for i in output:
		I_ = ord(i)
		# 使用位置相关的随机变换
		位置因子 = (种子数字 + ord(i)) % 100
		i_ = str(I_ + 位置因子)
		temp = int(output_ + i_)
		output_ = str(temp+ I_)[-1000:]
	
	output = output_
	output = output[::-1]
	output = int(output)
	
	# 随机切片参数
	切片开始 = random.randint(0, 10)
	切片结束 = random.randint(20, 40)
	切片步长 = random.choice([1, 2, 3])
	
	output = int(oct(output)[2::切片步长])
	output = str(hex(output)[2::])[切片开始:切片结束:切片步长]
	
	# 时间戳处理（加入随机性）
	timestamp = str(int(time.time()))
	# 随机选择时间戳部分
	时间戳部分1 = random.choice([0, 1, 2])
	时间戳部分2 = random.choice([1, 2, 3])
	
	output = (output +
			  timestamp[时间戳部分1:时间戳部分1 + 6:1] +
			  timestamp[::-1][时间戳部分2:时间戳部分2 + 6])
	
	return output


def 验证(input_data: str, outputed: str) -> bool:
	"""验证函数（需要与加密使用相同的随机种子）"""
	# 设置相同的随机种子
	种子数字 = 设置随机种子(input_data)
	
	# 重新加密
	新输出 = 加密(input_data)
	
	# 由于有随机性，我们需要验证核心部分
	# 提取时间戳之前的部分进行比较
	try:
		# 找到时间戳开始的位置（通常是数字部分）
		for i in range(len(新输出)):
			if 新输出[i:].isdigit() and len(新输出[i:]) >= 10:
				哈希部分 = 新输出[:i]
				break
		else:
			哈希部分 = 新输出
		
		# 同样处理待验证的输出
		for i in range(len(outputed)):
			if outputed[i:].isdigit() and len(outputed[i:]) >= 10:
				待验证哈希部分 = outputed[:i]
				break
		else:
			待验证哈希部分 = outputed
		
		# 比较哈希部分
		if 哈希部分 == 待验证哈希部分:
			return True
	except:
		pass
	
	return False

if __name__ == '__main__':
	__ = 加密("123.38.0.0")
	print(__)
	print(验证("123.38.0.0", __))
