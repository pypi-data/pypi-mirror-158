# /* Copyright (C) 2001
#  * Housemarque Oy
#  * http://www.housemarque.com
#  *
#  * Distributed under the Boost Software License, Version 1.0. (See
#  * accompanying file LICENSE_1_0.txt or copy at
#  * http://www.boost.org/LICENSE_1_0.txt)
#  */
#
# /* Revised by Paul Mensonides (2002) */
#
# /* See http://www.boost.org for most recent version. */
#
# ifndef MSGPACK_PREPROCESSOR_ARITHMETIC_DEC_HPP
# define MSGPACK_PREPROCESSOR_ARITHMETIC_DEC_HPP
#
# include <msgpack/preprocessor/config/config.hpp>
#
# /* MSGPACK_PP_DEC */
#
# if ~MSGPACK_PP_CONFIG_FLAGS() & MSGPACK_PP_CONFIG_MWCC()
#    define MSGPACK_PP_DEC(x) MSGPACK_PP_DEC_I(x)
# else
#    define MSGPACK_PP_DEC(x) MSGPACK_PP_DEC_OO((x))
#    define MSGPACK_PP_DEC_OO(par) MSGPACK_PP_DEC_I ## par
# endif
#
# define MSGPACK_PP_DEC_I(x) MSGPACK_PP_DEC_ ## x
#
# define MSGPACK_PP_DEC_0 0
# define MSGPACK_PP_DEC_1 0
# define MSGPACK_PP_DEC_2 1
# define MSGPACK_PP_DEC_3 2
# define MSGPACK_PP_DEC_4 3
# define MSGPACK_PP_DEC_5 4
# define MSGPACK_PP_DEC_6 5
# define MSGPACK_PP_DEC_7 6
# define MSGPACK_PP_DEC_8 7
# define MSGPACK_PP_DEC_9 8
# define MSGPACK_PP_DEC_10 9
# define MSGPACK_PP_DEC_11 10
# define MSGPACK_PP_DEC_12 11
# define MSGPACK_PP_DEC_13 12
# define MSGPACK_PP_DEC_14 13
# define MSGPACK_PP_DEC_15 14
# define MSGPACK_PP_DEC_16 15
# define MSGPACK_PP_DEC_17 16
# define MSGPACK_PP_DEC_18 17
# define MSGPACK_PP_DEC_19 18
# define MSGPACK_PP_DEC_20 19
# define MSGPACK_PP_DEC_21 20
# define MSGPACK_PP_DEC_22 21
# define MSGPACK_PP_DEC_23 22
# define MSGPACK_PP_DEC_24 23
# define MSGPACK_PP_DEC_25 24
# define MSGPACK_PP_DEC_26 25
# define MSGPACK_PP_DEC_27 26
# define MSGPACK_PP_DEC_28 27
# define MSGPACK_PP_DEC_29 28
# define MSGPACK_PP_DEC_30 29
# define MSGPACK_PP_DEC_31 30
# define MSGPACK_PP_DEC_32 31
# define MSGPACK_PP_DEC_33 32
# define MSGPACK_PP_DEC_34 33
# define MSGPACK_PP_DEC_35 34
# define MSGPACK_PP_DEC_36 35
# define MSGPACK_PP_DEC_37 36
# define MSGPACK_PP_DEC_38 37
# define MSGPACK_PP_DEC_39 38
# define MSGPACK_PP_DEC_40 39
# define MSGPACK_PP_DEC_41 40
# define MSGPACK_PP_DEC_42 41
# define MSGPACK_PP_DEC_43 42
# define MSGPACK_PP_DEC_44 43
# define MSGPACK_PP_DEC_45 44
# define MSGPACK_PP_DEC_46 45
# define MSGPACK_PP_DEC_47 46
# define MSGPACK_PP_DEC_48 47
# define MSGPACK_PP_DEC_49 48
# define MSGPACK_PP_DEC_50 49
# define MSGPACK_PP_DEC_51 50
# define MSGPACK_PP_DEC_52 51
# define MSGPACK_PP_DEC_53 52
# define MSGPACK_PP_DEC_54 53
# define MSGPACK_PP_DEC_55 54
# define MSGPACK_PP_DEC_56 55
# define MSGPACK_PP_DEC_57 56
# define MSGPACK_PP_DEC_58 57
# define MSGPACK_PP_DEC_59 58
# define MSGPACK_PP_DEC_60 59
# define MSGPACK_PP_DEC_61 60
# define MSGPACK_PP_DEC_62 61
# define MSGPACK_PP_DEC_63 62
# define MSGPACK_PP_DEC_64 63
# define MSGPACK_PP_DEC_65 64
# define MSGPACK_PP_DEC_66 65
# define MSGPACK_PP_DEC_67 66
# define MSGPACK_PP_DEC_68 67
# define MSGPACK_PP_DEC_69 68
# define MSGPACK_PP_DEC_70 69
# define MSGPACK_PP_DEC_71 70
# define MSGPACK_PP_DEC_72 71
# define MSGPACK_PP_DEC_73 72
# define MSGPACK_PP_DEC_74 73
# define MSGPACK_PP_DEC_75 74
# define MSGPACK_PP_DEC_76 75
# define MSGPACK_PP_DEC_77 76
# define MSGPACK_PP_DEC_78 77
# define MSGPACK_PP_DEC_79 78
# define MSGPACK_PP_DEC_80 79
# define MSGPACK_PP_DEC_81 80
# define MSGPACK_PP_DEC_82 81
# define MSGPACK_PP_DEC_83 82
# define MSGPACK_PP_DEC_84 83
# define MSGPACK_PP_DEC_85 84
# define MSGPACK_PP_DEC_86 85
# define MSGPACK_PP_DEC_87 86
# define MSGPACK_PP_DEC_88 87
# define MSGPACK_PP_DEC_89 88
# define MSGPACK_PP_DEC_90 89
# define MSGPACK_PP_DEC_91 90
# define MSGPACK_PP_DEC_92 91
# define MSGPACK_PP_DEC_93 92
# define MSGPACK_PP_DEC_94 93
# define MSGPACK_PP_DEC_95 94
# define MSGPACK_PP_DEC_96 95
# define MSGPACK_PP_DEC_97 96
# define MSGPACK_PP_DEC_98 97
# define MSGPACK_PP_DEC_99 98
# define MSGPACK_PP_DEC_100 99
# define MSGPACK_PP_DEC_101 100
# define MSGPACK_PP_DEC_102 101
# define MSGPACK_PP_DEC_103 102
# define MSGPACK_PP_DEC_104 103
# define MSGPACK_PP_DEC_105 104
# define MSGPACK_PP_DEC_106 105
# define MSGPACK_PP_DEC_107 106
# define MSGPACK_PP_DEC_108 107
# define MSGPACK_PP_DEC_109 108
# define MSGPACK_PP_DEC_110 109
# define MSGPACK_PP_DEC_111 110
# define MSGPACK_PP_DEC_112 111
# define MSGPACK_PP_DEC_113 112
# define MSGPACK_PP_DEC_114 113
# define MSGPACK_PP_DEC_115 114
# define MSGPACK_PP_DEC_116 115
# define MSGPACK_PP_DEC_117 116
# define MSGPACK_PP_DEC_118 117
# define MSGPACK_PP_DEC_119 118
# define MSGPACK_PP_DEC_120 119
# define MSGPACK_PP_DEC_121 120
# define MSGPACK_PP_DEC_122 121
# define MSGPACK_PP_DEC_123 122
# define MSGPACK_PP_DEC_124 123
# define MSGPACK_PP_DEC_125 124
# define MSGPACK_PP_DEC_126 125
# define MSGPACK_PP_DEC_127 126
# define MSGPACK_PP_DEC_128 127
# define MSGPACK_PP_DEC_129 128
# define MSGPACK_PP_DEC_130 129
# define MSGPACK_PP_DEC_131 130
# define MSGPACK_PP_DEC_132 131
# define MSGPACK_PP_DEC_133 132
# define MSGPACK_PP_DEC_134 133
# define MSGPACK_PP_DEC_135 134
# define MSGPACK_PP_DEC_136 135
# define MSGPACK_PP_DEC_137 136
# define MSGPACK_PP_DEC_138 137
# define MSGPACK_PP_DEC_139 138
# define MSGPACK_PP_DEC_140 139
# define MSGPACK_PP_DEC_141 140
# define MSGPACK_PP_DEC_142 141
# define MSGPACK_PP_DEC_143 142
# define MSGPACK_PP_DEC_144 143
# define MSGPACK_PP_DEC_145 144
# define MSGPACK_PP_DEC_146 145
# define MSGPACK_PP_DEC_147 146
# define MSGPACK_PP_DEC_148 147
# define MSGPACK_PP_DEC_149 148
# define MSGPACK_PP_DEC_150 149
# define MSGPACK_PP_DEC_151 150
# define MSGPACK_PP_DEC_152 151
# define MSGPACK_PP_DEC_153 152
# define MSGPACK_PP_DEC_154 153
# define MSGPACK_PP_DEC_155 154
# define MSGPACK_PP_DEC_156 155
# define MSGPACK_PP_DEC_157 156
# define MSGPACK_PP_DEC_158 157
# define MSGPACK_PP_DEC_159 158
# define MSGPACK_PP_DEC_160 159
# define MSGPACK_PP_DEC_161 160
# define MSGPACK_PP_DEC_162 161
# define MSGPACK_PP_DEC_163 162
# define MSGPACK_PP_DEC_164 163
# define MSGPACK_PP_DEC_165 164
# define MSGPACK_PP_DEC_166 165
# define MSGPACK_PP_DEC_167 166
# define MSGPACK_PP_DEC_168 167
# define MSGPACK_PP_DEC_169 168
# define MSGPACK_PP_DEC_170 169
# define MSGPACK_PP_DEC_171 170
# define MSGPACK_PP_DEC_172 171
# define MSGPACK_PP_DEC_173 172
# define MSGPACK_PP_DEC_174 173
# define MSGPACK_PP_DEC_175 174
# define MSGPACK_PP_DEC_176 175
# define MSGPACK_PP_DEC_177 176
# define MSGPACK_PP_DEC_178 177
# define MSGPACK_PP_DEC_179 178
# define MSGPACK_PP_DEC_180 179
# define MSGPACK_PP_DEC_181 180
# define MSGPACK_PP_DEC_182 181
# define MSGPACK_PP_DEC_183 182
# define MSGPACK_PP_DEC_184 183
# define MSGPACK_PP_DEC_185 184
# define MSGPACK_PP_DEC_186 185
# define MSGPACK_PP_DEC_187 186
# define MSGPACK_PP_DEC_188 187
# define MSGPACK_PP_DEC_189 188
# define MSGPACK_PP_DEC_190 189
# define MSGPACK_PP_DEC_191 190
# define MSGPACK_PP_DEC_192 191
# define MSGPACK_PP_DEC_193 192
# define MSGPACK_PP_DEC_194 193
# define MSGPACK_PP_DEC_195 194
# define MSGPACK_PP_DEC_196 195
# define MSGPACK_PP_DEC_197 196
# define MSGPACK_PP_DEC_198 197
# define MSGPACK_PP_DEC_199 198
# define MSGPACK_PP_DEC_200 199
# define MSGPACK_PP_DEC_201 200
# define MSGPACK_PP_DEC_202 201
# define MSGPACK_PP_DEC_203 202
# define MSGPACK_PP_DEC_204 203
# define MSGPACK_PP_DEC_205 204
# define MSGPACK_PP_DEC_206 205
# define MSGPACK_PP_DEC_207 206
# define MSGPACK_PP_DEC_208 207
# define MSGPACK_PP_DEC_209 208
# define MSGPACK_PP_DEC_210 209
# define MSGPACK_PP_DEC_211 210
# define MSGPACK_PP_DEC_212 211
# define MSGPACK_PP_DEC_213 212
# define MSGPACK_PP_DEC_214 213
# define MSGPACK_PP_DEC_215 214
# define MSGPACK_PP_DEC_216 215
# define MSGPACK_PP_DEC_217 216
# define MSGPACK_PP_DEC_218 217
# define MSGPACK_PP_DEC_219 218
# define MSGPACK_PP_DEC_220 219
# define MSGPACK_PP_DEC_221 220
# define MSGPACK_PP_DEC_222 221
# define MSGPACK_PP_DEC_223 222
# define MSGPACK_PP_DEC_224 223
# define MSGPACK_PP_DEC_225 224
# define MSGPACK_PP_DEC_226 225
# define MSGPACK_PP_DEC_227 226
# define MSGPACK_PP_DEC_228 227
# define MSGPACK_PP_DEC_229 228
# define MSGPACK_PP_DEC_230 229
# define MSGPACK_PP_DEC_231 230
# define MSGPACK_PP_DEC_232 231
# define MSGPACK_PP_DEC_233 232
# define MSGPACK_PP_DEC_234 233
# define MSGPACK_PP_DEC_235 234
# define MSGPACK_PP_DEC_236 235
# define MSGPACK_PP_DEC_237 236
# define MSGPACK_PP_DEC_238 237
# define MSGPACK_PP_DEC_239 238
# define MSGPACK_PP_DEC_240 239
# define MSGPACK_PP_DEC_241 240
# define MSGPACK_PP_DEC_242 241
# define MSGPACK_PP_DEC_243 242
# define MSGPACK_PP_DEC_244 243
# define MSGPACK_PP_DEC_245 244
# define MSGPACK_PP_DEC_246 245
# define MSGPACK_PP_DEC_247 246
# define MSGPACK_PP_DEC_248 247
# define MSGPACK_PP_DEC_249 248
# define MSGPACK_PP_DEC_250 249
# define MSGPACK_PP_DEC_251 250
# define MSGPACK_PP_DEC_252 251
# define MSGPACK_PP_DEC_253 252
# define MSGPACK_PP_DEC_254 253
# define MSGPACK_PP_DEC_255 254
# define MSGPACK_PP_DEC_256 255
# define MSGPACK_PP_DEC_257 256
#
# endif
