myset = {1,2,3}

z = len(myset)

for i in range(z):
	attempt = myset.pop()
	print(attempt)

	myset.add(attempt)

print(myset)