# Vincent Trang
# 8-24-2022

def sleep_in(weekday, vacation):
    return not weekday or vacation

def monkey_trouble(a_smile, b_smile):
    return (a_smile == b_smile)

def sum_double(a, b):
    return (a+b)*(1+(a==b))

def diff21(n):
    return abs(n-21)*(1+(n>21))

def parrot_trouble(talking, hour):
    return talking and (hour<7 or hour>20)

def makes10(a, b):
    return a==10 or b==10 or a+b==10

def near_hundred(n):
    return abs(n-100) <= 10 or abs(n-200) <= 10

def pos_neg(a, b, negative):
    return (negative == False) and ((a > 0 and b < 0) or (a < 0 and b > 0)) or (negative == True and a < 0 and b < 0)

def hello_name(name):
    return "Hello "+name+"!"

def make_abba(a, b):
    return a+b+b+a

def make_tags(tag, word):
    return f"<{tag}>{word}</{tag}>"

def make_out_word(out, word):
    return out[:len(out)//2] + word + out[len(out)//2:]

def extra_end(st):
    return (st[-2:])*3
    
def first_two(st):
    return st[:min(2,len(st))]

def first_half(st):
    return st[:len(st)//2]

def without_end(st):
    return st[1:-1]

def first_last6(nums):
    return nums[0] == 6 or nums[-1] == 6

def same_first_last(nums):
    return len(nums) > 0 and nums[0] == nums[-1]

def make_pi(n):
    return list(map(int, list("31415926535897"[:n])))

def common_end(a, b):
    return a[0] == b[0] or a[-1] == b[-1]

def sum3(nums):
    return sum(nums)

def rotate_left3(nums):
    return nums and nums[1:] + [nums[0]]

def reverse3(nums):
    return list(reversed(nums))

def max_end3(nums):
    return [max(nums[0], nums[-1]) for i in nums]

def cigar_party(cigars, is_weekend):
    return 40<=cigars if is_weekend else 40<=cigars<=60

def date_fashion(you, date):
    return 0 if date<=2 or you<=2 else 2 if date>=8 or you>=8 else 1

def squirrel_play(temp, is_summer):
    return 60<=temp<=90+10*is_summer

def caught_speeding(speed, is_birthday):
    return (speed>60+5*is_birthday)+(speed>80+5*is_birthday)

def sorta_sum(a, b):
    return 20 if 10<=a+b<=19 else a+b

def alarm_clock(day, vacation):
    return ["7:00","10:00","off"][vacation+(day%6==0)]

def love6(a, b):
    return a==6 or b==6 or a+b==6 or abs(a-b)==6

def in1to10(n, outside_mode):
    return n<=1 or n>=10 if outside_mode else 1<=n<=10
