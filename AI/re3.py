import sys; args = sys.argv[1:]
idx = int(args[0])-50

myRegexLst = [
  r"/\w*(\w)\w*\1\w*/i",
  r"/\w*(\w)(\w*\1){3}\w*/i",
  r"/^([01])([01]*\1)?$/",
  r"/\b(?=\w*cat)(\w){6}\b/i",
  r"/\b(?=\w*ing)(?=\w*bri)(\w){5,9}\b/i",
  r"/\b(?!\w*cat)(\w){6}\b/i",
  r"/\b(?!\w*(\w)\w*\1)\w+\b/i",
  r"/^(?![01]*10011)[01]*$/",
  r"/\w*(?!(.)\1)[aeiou]{2}\w*/i",
  r"/^(?![01]*1[01]1)[01]*$/", 
  ] 

if idx < len(myRegexLst):
  print(myRegexLst[idx])

# Vincent Trang, pd.4, 2023
