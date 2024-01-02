import sys; args = sys.argv[1:]
idx = int(args[0])-40

myRegexLst = [
  r"/^[xX.Oo]{64}$/",
  r"/^[xXOo]*\.[xXOo]*$/",
  r"/^([xX]+[oO]*)?\.|\.([oO]*[xX]+)?$/",
  r"/^.(..)*$/s",
  r"/^(0|1[01])([01]{2})*$/",
  r"/\w*(a[eiou]|e[aoiu]|i[aoeu]|o[aieu]|u[aeio])\w*/i",
  r"/^(0|10)*1*$/",
  r"/^[bc]*([bc]|a[bc]*)$/",
  r"/^((a[bc]*){2}|[bc])+$/",
  r"/^((1[02]*){2}|20*)+$/", # even number of 1s
  ] 

if idx < len(myRegexLst):
  print(myRegexLst[idx])

# Vincent Trang, pd.4, 2023
