with open("program\code.txt",'r') as f:
    with open("program\compiled_code.txt",'w') as g:
        code = f.readlines()
        for instruction in code:
            if instruction[:3] == "adi":
                g.write("01\n" + instruction[4:])
            elif instruction[:3] == "sbi":
                g.write("02\n" + instruction[4:])
            elif instruction[:3] == "xri":
                g.write("03\n" + instruction[4:])
            elif instruction[:3] == "ani":
                g.write("04\n" + instruction[4:])
            elif instruction[:3] == "ori":
                g.write("05\n" + instruction[4:])
            elif instruction[:3] == "cmi":
                g.write("06\n" + instruction[4:])
            elif instruction == "stop":
                g.write("07")
            elif instruction[:3] == "ret":
                g.write("0\n")
                if instruction[4].lower() == "s": g.write("8\n")
                elif instruction[4].lower() == "z": g.write("9\n")
                elif instruction[4].lower() == "p": g.write("d\n")
                elif instruction[4].lower() == "c": g.write("f\n")
            elif instruction[:3] in ["add","sub","xor","and","or","cmp"]:
                if instruction[:3] == "add": g.write("1")
                elif instruction[:3] == "sub": g.write("2")
                elif instruction[:3] == "xor": g.write("3")
                elif instruction[:3] == "and": g.write("4")
                elif instruction[:3] == "or": g.write("5")
                elif instruction[:3] == "cmp": g.write("6")
                if int(instruction[4:])==0: g.write("0")
                elif int(instruction[4:])==1: g.write("1")
                elif int(instruction[4:])==2: g.write("2")
                elif int(instruction[4:])==3: g.write("3")
                elif int(instruction[4:])==4: g.write("4")
                elif int(instruction[4:])==5: g.write("5")
                elif int(instruction[4:])==6: g.write("6")
                elif int(instruction[4:])==7: g.write("7")
                elif int(instruction[4:])==8: g.write("8")
                elif int(instruction[4:])==9: g.write("9")
                elif int(instruction[4:])==10: g.write("a")
                elif int(instruction[4:])==11: g.write("b")
                elif int(instruction[4:])==12: g.write("c")
                elif int(instruction[4:])==13: g.write("d")
                elif int(instruction[4:])==14: g.write("e")
                elif int(instruction[4:])==15: g.write("f")
                g.write("\n")
            elif instruction[:3] == "mov":
                if instruction[3] == 's': g.write("7")
                elif instruction[3] == 'd': g.write("8")
                elif instruction[3] == 'i': g.write("9")
                if int(instruction[4])==0: g.write("0")
                elif int(instruction[4:6])==10: g.write("a")
                elif int(instruction[4:6])==11: g.write("b")
                elif int(instruction[4:6])==12: g.write("c")
                elif int(instruction[4:6])==13: g.write("d")
                elif int(instruction[4:6])==14: g.write("e")
                elif int(instruction[4:6])==15: g.write("f")
                elif int(instruction[4])==1: g.write("1")
                elif int(instruction[4])==2: g.write("2")
                elif int(instruction[4])==3: g.write("3")
                elif int(instruction[4])==4: g.write("4")
                elif int(instruction[4])==5: g.write("5")
                elif int(instruction[4])==6: g.write("6")
                elif int(instruction[4])==7: g.write("7")
                elif int(instruction[4])==8: g.write("8")
                elif int(instruction[4])==9: g.write("9")
                g.write("\n")
                if instruction[3] == 'i':
                    g.write(instruction[-3:])