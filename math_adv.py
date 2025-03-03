#!/usr/bin/env python3
# coding: utf-8

"""math prob generator"""

import secrets
import sys

#
N_MAX = 3
LOOP = 24

MIN_NUM = 2
MAX_NUM = 300
# OPRTR = ['+','-','*','/']
# OPRTR = ["+", "-"] + ["*"] * 40 + ["/"] * 80
# OPRTR = ['*']
OPRTR = ['*','/']

EQUAL_RATE = 20 #equal vs non-equal: n:1
FORCE_EQUAL = 1
DEBUG_MODE = 0

#


def calc(var0, var1, opr):
    """calculation"""

    if opr == "+":
        result = var0 + var1
    elif opr == "-":
        result = var0 - var1
    elif opr == "*":
        result = var0 * var1
    elif opr == "/":
        if var1 == 0:
            return None
        result = var0 // var1
        if result * var1 != var0:
            return None
    if result < MIN_NUM: # or MAX_NUM <= result:
        return None
    return result


#
def range_chk(n_len, n, opr):
    """check number range"""

    tmp = n[0]
    if MIN_NUM <= tmp <= MAX_NUM:
        valid = 1
    else:
        return None, 0

    if n_len == 1:
        # return tmp, valid
        pass
    elif n_len == 2:
        tmp = calc(tmp, n[1], opr[0])

        # if opr[0] == '+':
        # 	tmp = tmp + n[1]
        # elif opr[0] == '-':
        # 	tmp = tmp - n[1]
        # elif opr[0] == '*':
        # 	tmp = tmp * n[1]
        # elif opr[0] == '/':
        # 	if n[1] == 0 :
        # 		return None, 0
        # 	tmp2 = tmp // n[1]
        # 	if tmp2 * n[1] != tmp :
        # 		return None, 0
        # 	else:
        # 		tmp = tmp2

        if tmp is None:
            valid = 0
        # return tmp, valid
    else:
        # long equa
        idx_var2 = 2
        idx_opr1 = 0
        # idx_opr1 = idx_var2 -1
        tmp1 = n[1]

        while idx_var2 < n_len:
            if opr[idx_var2 - 1] in ["*", "/"] and opr[idx_opr1] in ["+", "-"]:
                tmp1 = calc(tmp1, n[idx_var2], opr[idx_var2 - 1])
                idx_var2 += 1
            else:
                tmp = calc(tmp, tmp1, opr[idx_opr1])
                idx_var2 += 1
                idx_opr1 += 1
                tmp1 = n[idx_var2 - 1]
            if tmp is None or tmp1 is None:
                return tmp, 0
        tmp = calc(tmp, tmp1, opr[idx_opr1])
        if tmp is None:
            valid = 0
    return tmp, valid


# DEF range_chk END

#


def equa_constr():
    """build equition"""

    n_len = secrets.randbelow(N_MAX - 1) + 1
    n = []
    for _ in range(n_len):
        n.append(secrets.randbelow(MAX_NUM + 1 - MIN_NUM) + MIN_NUM)
    #
    opr = []
    for _ in range(n_len - 1):
        opr.append(OPRTR[secrets.randbelow(len(OPRTR))])

    result, valid = range_chk(n_len, n, opr)

    return n_len, n, opr, result, valid


# DEF equa_constr END

#


def main(suffix):
    """MAIN"""

    q, test = 1, 0
    with open("./math_" + suffix + ".csv", "w", encoding="utf-8") as f, open(
        "./math_" + suffix + "_a.csv", "w", encoding="utf-8"
    ) as fa:
        while q <= LOOP:
            print("--------------------")
            test = test + 1
            print("[", q, "] :", "[", test, "]")

            flg_equa = secrets.randbelow(EQUAL_RATE) + FORCE_EQUAL

            while True:
                n_len_left, n_left, opr_left, result_left, valid_left = equa_constr()
                print("left:",n_len_left, n_left, opr_left, result_left, valid_left)
                if valid_left == 1:
                    break

            while True:
                n_len_right, n_right, opr_right, result_right, valid_right = equa_constr()
                print("right:",n_len_right, n_right, opr_right, result_right, valid_right)
                if valid_right == 1:
                    if flg_equa == 0 or result_right == result_left:
                        break

            if result_left < result_right:
                equa = "<"
            elif result_left > result_right:
                equa = ">"
            else:
                equa = "="

            print(n_len_left, n_left, opr_left)
            print(n_len_right, n_right, opr_right)

            if 2 < n_len_left + n_len_right:  # and n_len_left + n_len_right <= N_MAX:
                q_items = []
                q_items.append(n_left[0])
                for i_left in range(n_len_left - 1):
                    q_items.append(opr_left[i_left])
                    q_items.append(n_left[i_left + 1])

                q_items.append(equa)
                q_items.append(n_right[0])
                for i_right in range(n_len_right - 1):
                    q_items.append(opr_right[i_right])
                    q_items.append(n_right[i_right + 1])

                mask_pos = secrets.randbelow(len(q_items))

                # answer = q_items[mask_pos]
                # if answer in OPRTR:
                # 	answers = OPRTR
                # elif answer in ['<','=','>']:
                # 	answers = ['<','=','>']
                # else:
                # 	answers=[]
                # 	while True:
                # 		dummy = secrets.randbelow(MAX_NUM+1)
                # 		if dummy != answer and dummy not in answers:
                # 			answers.append(dummy)
                # 		if len(answers) == 4:
                # 			break
                # 	answers[secrets.randbelow(4)] = answer

                if DEBUG_MODE == 0:
                    answer = q_items[mask_pos]
                    q_items[mask_pos] = "(      )"

                if q % 2 == 0:
                    spliter = "\t"
                else:
                    spliter = ""

                print(
                    spliter, "[", str(q).zfill(2), "]", ":   ", sep="", end=" ", file=f
                )
                print(
                    spliter, "[", str(q).zfill(2), "]", ":   ", sep="", end=" ", file=fa
                )

                q_str = ""
                for i_item in q_items:
                    q_str += str(i_item) + " "
                # print("{:<60}".format(q_str), sep="", end=" ", file=f, flush=True)
                print(f"{q_str:<60}", sep="", end=" ", file=f, flush=True)
                # print("{:<60}".format(answer), sep="", end=" ", file=fa, flush=True)
                print(f"{answer:<60}", sep="", end=" ", file=fa, flush=True)

                if q % 2 == 0:
                    print("\n", file=f, flush=True)
                    print("\n", file=fa, flush=True)


				# print('         ', sep='', end='', file=f)
				# for i in range(len(answers)):
				# 	seq = chr(ord('A')+i)
				# 	print( seq, '. ', answers[i], sep = '', end = '    ', file=f )
				# print('\n\n',file=f,flush=True)


                q = q + 1
            print("--------------------", flush=True)


# DEF MAIN END


#
if __name__ == "__main__":
    try:
        SUFFIX = 1
        if len(sys.argv) > 1:
            SUFFIX = sys.argv[1]
            if not SUFFIX.isnumeric():
                SUFFIX = 1
        for i in range(int(SUFFIX)):
            main(str(i))
    except KeyboardInterrupt:
        print("closed!")

#########################################
