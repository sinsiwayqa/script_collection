BEGIN{
	isErr=0;
	sLine=0;
        i=0
        readFile="cat "infoFile
        while(readFile | getline tmp) {
                arr[i] = tmp
                i++
        }
        close(infoFile)
}

function printStack() {
	if(sLine > maxLine) {
		isErr=2
#	} else if(/^== Thread/ || /^Thread/ || /^No symbol table info available/) {
	} else if(/^== Thread/ || /^Thread/) {
		isErr=2
	} else if(isErr==1) {
		if(detail==1) {
			print $0
			sLine++
		} else {
			if(/^#/) {
				print $0
				sLine++
			}
		}
	}
}

function printInfo() {
	#if(match($0, "^Output") || match($0, "^terminate") || match($0, "^suffix") || match($0, "$SOHA_") || match($0, "^System") || match($0, "^Node") || match($0, "^Release") || match($0, "^Version") || match($0, "^Machine") || match($0, "^Username") || match($0, "^PID") || match($0, "^Image") || match($0, "^suffix")) {
	for(j in arr) {
		if(match($0, arr[j])) {
			print $0
		}
	}
}

{
	if(info==1) {
		printInfo()
	}

	# Find the line for "signal handler called"
	if(match($0, "signal handler called") || match($0, "terminate_handler")) {
		isErr=1
	}

	# Output up to the maximum number of rows
	printStack()
}

END {
	if(isErr==0) {
		print "Trace Empty"
	}
}
