BEGIN {
	isErr=0
	sLine=0
	i=0
	readFile="cat "exceptFile
	while(readFile | getline tmp) {
		arr[i] = tmp
		i++
	}
	close(exceptFile)
}
{
	for(j in arr) {
		#if(match(arr[j], ":$")) {
		##if((match($0, arr[j]) && ! match($0, "start:$")) || (match($0, arr[j]) && ! match($0, "stop:$"))){
		if((match($0, arr[j]) && ! match($0, "start:$"))) {
			#print arr[j]
			isErr=1
			sLine=1
		}
		#} else if(match($0, arr[j])) {
		#	print "asdf", arr[j]
	#if(match($0, ":exception") || match($0, "exception:") || match($0, "failed:") || match($0, "failed.$") || (match($0, ":$") && ! match($0, "start:$"))) {
	#if(match($0, ":$") && ! match($0, "start:")) {
		#	isErr=1
		#	sLine=1
		#}
	}

	if(isErr==1) {
		if(sLine==1) {
			print FILENAME, NR, $0
			sLine=0
		} else if(match($0, ".cpp:") || match($0, ".h:") || match($0, "Exception")) {
			print FILENAME, NR, $0	
		} else {
			isErr=0
		}
	}
	
}
