# 
## 

 # Minimum Edit Distance/Levenshtein
 # med.py - January 23, 2015
 # Timothy Kim
 
 # computes the minimum edit distance between two strings 
 # (target, source) supplied by command line at runtime
 # with insertions, deletions, or substitutions costing
 # 1,1, and 2 respectively
 # it then displays visually edits made with the target 
 # string above source
 # "_" on first line represents deletion from source
 # "-" on third line represents insertion in target
 # "|" on second line represents unchanged matched letter
 # " " on second line represents substitution 

##

#edits made stored in list
path = []

def distance(target, source, insertcost, deletecost, replacecost):
	n = len(target) + 1
	m = len(source) + 1
	#set up dist and initialize values
	dist = [[0 for j in range(m)] for i in range(n)]
	ptr = [[0 for j in range(m)] for i in range(n)] #backtrace matrix
	for i in range(1,n):
		dist[i][0] = dist[i-1][0] + insertcost
	for j in range(1,m):
		dist[0][j] = dist[0][j-1] + deletecost
	#align source and target strings
	for j in range(1,m):
		for i in range(1,n):
			inscost = insertcost + dist[i-1][j]
			delcost = deletecost + dist[i][j-1]
			if (source[j-1] == target[i-1]): add = 0
			else: add = replacecost
			substcost = add + dist[i-1][j-1]
			dist[i][j] = min(inscost, delcost, substcost)
			#keep track of where we came from
			if i>0 and j>0 and dist[i-1][j-1] == dist[i][j] and target[i-1] == source[j-1]:
				ptr[i][j] = "DIAGM"
			elif i>0 and j>0 and dist[i-1][j-1] + 2 == dist[i][j]:
				ptr[i][j] = "DIAGS"	
			elif j>0 and dist[i][j-1] + 1 == dist[i][j]:
				ptr[i][j] = "LEFT"
			elif i>0 and dist[i-1][j] + 1 == dist[i][j]:
				ptr[i][j] = "UP"		
				
	#function to backtrace for alignment	
	def backtrace(i,j):
		if ptr[i][j] == "LEFT":
			path.append("D")
			return backtrace(i, j-1)
		elif ptr[i][j] == "UP":
			path.append("I")
			return backtrace(i-1, j)
		elif ptr[i][j] == "DIAGS":
			path.append("S")
			return backtrace(i-1, j-1)
		elif ptr[i][j] == "DIAGM":
			path.append("M")
			return backtrace(i-1,j-1)
		else:
			if i > 0 and j == 0:
				path.append("I")
				return backtrace(i-1,j)
			if i == 0 and j > 0:
				path.append("D")
				return backtrace(i,j-1)
			return ""
			
	#function to print Minimum Edit Distance/Levenshtein matrix
	def pmatrix(i,j):
		for a in range(0, i+1):
			print dist[a]
		print ""	
		
	#pmatrix(n-1, m-1)
	backtrace(n-1, m-1)
	path.reverse()
	print path
	print "levenshtein distance =", dist[n-1][m-1]
	listlen = len(path)
	t = 0
	s = 0
	#prints visual alignment with target above the source
	for i in range(listlen):
		if path[i] == "D":
			print "_",
		elif path[i] == "I" or path[i] == "S" or path[i] == "M":
			print target[t],
			t += 1
	print ""
	for i in range(listlen):
		if path[i] == "D" or path[i] == "I" or path[i] == "S":
			print " ",
		elif path[i] == "M":
			print "|",
	print ""
	for i in range(listlen):
		if path[i] == "D" or path[i] == "S" or path[i] == "M":
			print source[s],
			s += 1
		elif path[i] == "I":
			print "_",
	print ""

#obtains command line arguments and runs function
if __name__=="__main__":
	from sys import argv
	if len(argv) > 2:
		distance(argv[1], argv[2], 1, 1, 2)



