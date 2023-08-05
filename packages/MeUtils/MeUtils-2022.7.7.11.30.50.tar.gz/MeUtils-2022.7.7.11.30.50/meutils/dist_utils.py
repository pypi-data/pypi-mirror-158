#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : dist_utils
# @Time         : 2020/12/9 3:13 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm https://github.com/yuanjie-ai/DNN/blob/master/8_NLP/0_utils/Levenshtein.md
# @Description  : 几何距离、编辑距离、语义距离等
"""

Levenshtein.distance(str1, str2) # 描述由一个字串转化成另一个字串最少的操作次数，在其中的操作包括插入、删除、替换。算法实现：动态规划
Levenshtein.hamming(str1, str2) # 要求str1和str2必须长度一致。是描述两个等长字串之间对应位置上不同字符的个数
Levenshtein.ratio(str1, str2) # r=(sum–ldist)/sum, sum=len(str1)+len(str2),ldist是类编辑距离。在类编辑距离中删除、插入依然+1，但是替换+2
Levenshtein.jaro(str1, str2) # Jaro Distance # 据说是用来判定健康记录上两个名字是否相同，也有说是是用于人口普查
Levenshtein.jaro_winkler(str1, str2) # 给予了起始部分就相同的字符串更高的分数

Levenshtein.seqratio(['newspaper', 'litter bin', 'tinny', 'antelope'], ['caribou', 'sausage', 'gorn', 'woody']) # like ratio()
Levenshtein.setratio(['newspaper', 'litter bin', 'tinny', 'antelope'], ['caribou', 'sausage', 'gorn', 'woody'])

"""