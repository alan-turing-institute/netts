library('orca')
data("karate")
count4(karate)

library("FNN")
nodes <- scan("schools-wiki-nodes.txt", what = "", sep = "\n")
edges <- read.table("schools-wiki-edges.txt")
