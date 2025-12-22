def decode_message(typed):
    result = []
    for i in range(len(typed)-1):
    	if typed[i] == typed[i+1]:
    		pass
    	elif typed[i] != typed[i+1]:
    		result.append(typed[i])	
    result.append(typed[-1])
    
    print(result)

    return ""

typed = input().strip()
print(decode_message(typed))
