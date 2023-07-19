import os
import pandas as pd
#directory with jcl and procs
srch_directory=r'D:\Build'
#excel file with data to be replaced
parm_file=r'D:\Backup\replace_Input.xlsx'
dataframe1 = pd.read_excel(parm_file)
a=[]
for i in dataframe1:
    for m in dataframe1[i]:
        a.append(m)
input_string=[]
output_string=[]
#excel should have the coloumn header as below
input_string=(dataframe1["Mainframe PDS Name"].values.tolist())
output_string=(dataframe1["Raincode PDS name"].values.tolist())
for path, subdirs, files in os.walk(srch_directory):
    for name in files:
        extn=name.split(".")[-1]
        if extn.lower() == 'jcl' or extn.lower() == 'prc':
            source_filex=os.path.join(path,name)
            with open(source_filex,"rt") as file:
                data=file.readlines()
                data_out=[]
                file_tobe_updated=False
            for line in data:
                if line[:3] != '//*':
                #if any (word in line for word in input_string):
                    word_found = False
                    for word in input_string:
                        if word in line:
                            index=input_string.index(word)
                            start_pos=line.find(word)
                            input_len=len(word)
                            output_len=len(output_string[index])
                            first_space=line[start_pos+input_len:].find(" ")
                            diff_len=input_len-output_len
                            spaces_count=72-(start_pos+input_len+first_space)+diff_len
                            line1=''
                            #tag C090MIG is added from col 72
                            line1=line1+line[0:start_pos]+output_string[index]+line[start_pos+input_len:start_pos+input_len+first_space]+\
                            (' '*spaces_count)+'C090MIG'+line[79:]
                            print(source_filex)
                            print(line,end="")
                            print(line1,end="")
                            index_data=data.index(line)
                            word_found = True
                            file_tobe_updated=True
                    if word_found:
                        #tag C090MIG is added from col 72
                        data_out.append('//*' +line[3:72]+'C090MIG'+line[79:])
                        data_out.append(line1)
                    else:
                        data_out.append(line)
                else:
                    data_out.append(line)
            #replaced data written back to file
            if file_tobe_updated:
                with open(source_filex,"wt") as file:
                    file.writelines(data_out)
