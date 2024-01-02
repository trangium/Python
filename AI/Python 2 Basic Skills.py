# Vincent Trang
# 8-24-2022

def string_times(st, n): return st*n

def front_times(st, n): return st[:3]*n

def string_bits(st): return st[::2]

def string_splosion(st): return st and string_splosion(st[:-1])+st

def last2(st): return len(st)//3 and(st[:2]==st[-2:])+last2(st[1:])  

def array_count9(nums): return nums.count(9)

def array_front9(nums): return 9 in nums[:4]

def array123(nums): return any(nums[i:i+3]==[1,2,3] for i in range(len(nums)))

def string_match(a, b): return sum(a[i:i+2]==b[i:i+2] for i in range(len(b)-1))

def double_char(st): return ''.join([x*2 for x in st])

def count_hi(st): return st.count("hi")

def cat_dog(st): return st.count("cat") == st.count("dog")

def count_code(st): return sum(tuple("coe")==i for i in zip(st,st[1:],st[3:]))

def end_other(a,b): return (c:=a.lower()).endswith(d:=b.lower())or d.endswith(c)

def xyz_there(st): return "xyz" in st.replace(".x",".")

def count_evens(nums): return sum(map(lambda x: ~x&1, nums))

def big_diff(nums): return max(nums)-min(nums)

def centered_average(nums): return(sum(nums)-min(nums)-max(nums))//(len(nums)-2)

def sum13(nums): return len(nums) and (13 not in nums[-2:])*nums[-1]+sum13(nums[:-1])

def sum67(n): return (m:=1)*sum((m:=m&(x!=6))*x+0*(m:=m|(x==7)) for x in n)

def has22(nums): return any((2,2)==x for x in zip(nums,nums[1:]))

def make_bricks(small, big, goal): return goal-5*min(big, goal//5) <= small

def lone_sum(a, b, c): return(a==b==c)*a+2*sum({a,b,c})-a-b-c

def lucky_sum(a, b, c): return (a!=13)*(a+(b!=13)*(b+(c!=13)*c))

def no_teen_sum(a, b, c): return sum(map(lambda x: x-x*(x-10 in [3,4,7,8,9]), [a,b,c]))

def round_sum(a, b, c): return ((a+5)//10+(b+5)//10+(c+5)//10)*10

def close_far(a, b, c): return(((d:=sorted([a,b,c]))[2]-d[1])<2)^((d[1]-d[0])<2)

def make_chocolate(small, big, goal): return((a:=goal-5*min(big, goal//5))<=small and a+1)-1

# Vincent Trang 2 2023
