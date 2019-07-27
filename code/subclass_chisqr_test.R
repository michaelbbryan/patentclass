classes <- read.csv(choose.files(),stringsAsFactors=FALSE)
group_means <- read.csv(choose.files(),stringsAsFactors=FALSE)
subclass_means <- read.csv(choose.files(),stringsAsFactors=FALSE)

chisq.test(group_means$freq, correct=FALSE)

one=0
pass=0
fail=0
for (sc in subclass_means$subclass)    {
  x <- group_means[group_means$subclass==sc,]$freq
  if(length(x)==1){one=one+1} else {
  c <- chisq.test(x, correct=FALSE)
  if(c$p.value > 0.05){pass=pass+1} else {fail=fail+1}}
}
print(one)
print(pass)
print(fail)

one=0
pass=0
fail=0
for (cl in classes$class)    {
  x <- group_means[substr(group_means$subclass,1,3)==cl,]$freq
  if(length(x)==1){one=one+1} else {
    c <- chisq.test(x, correct=FALSE)
    if(c$p.value > 0.05){pass=pass+1} else {fail=fail+1}}
}
print(one)
print(pass)
print(fail)

