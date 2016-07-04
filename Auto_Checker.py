# @Author GWYOG
# @Title Script for auto-checking minecraft mods 

import os
import sys
import zipfile
import time

def initialize_folders():
    if not os.path.isdir("config"):
        os.mkdir("config")
    if not os.path.isdir("input"):
        os.mkdir("input")
    if not os.path.isdir("output"):
        os.mkdir("output")
    if not os.path.isdir("logs"):
        os.mkdir("logs")
    
def initialize_config():
    if not os.path.isfile("config/warning_keywords.cfg"):
        f = open("config/warning_keywords.cfg",'w')
        f.write("Keyword list = func_71033_a,GameType.CREATIVE\n")
        f.close()
    if not os.path.isfile("config/warning_extensions.cfg"):
        f = open("config/warning_extensions.cfg",'w')
        f.write("Extension list= .bat,.exe\n")
        f.close()
    if not os.path.isfile("config/checkmode.cfg"):
        f = open("config/checkmode.cfg",'w')
        f.write("Check mode(white namelist/black namelist) = white namelist\n")
        f.write("Filter(extension) = .java,.scala\n")

def load_config(log,file_name):
    ret = []
    try:
        f = open("config/" + file_name,'r')
        if file_name=="warning_keywords.cfg" or file_name=="warning_extensions.cfg":
            for line in f:
                if(line.find('=')!=-1):
                    value = line.split('=',1)[1].split(',')
                    for item in value:
                         ret.append(item.strip(' \n'))
        elif file_name=="checkmode.cfg":
            for line in f:
                if line.find('=')!=-1:
                    line_split = line.split('=',1)
                    if line_split[0].find("mode")!=-1:
                        checkmode = line_split[1].strip(' \n')
                    else:
                        value = line_split[1].split(',')
                        for item in value:
                            ret.append(item.strip(' \n'))
            ret = [checkmode,ret]
        f.close()
    except:
        print_log(log,"Fail to load config/" + file_name)
        print_log(log,"Script ends with -1")
        sys.exit(-1)
    return ret

def print_log(f,text):
    print(text)
    f.write(text+"\n")

def main():
    #time start
    start_time = time.time()
    #initialization
    initialize_folders()
    initialize_config()
    #open log file
    log = open("logs/" + time.strftime("%Y-%m-%d %H.%M.%S",time.localtime()) + ".log",'w')
    #load the configs
    black_extension_namelist = load_config(log,"warning_extensions.cfg")
    black_keywords = load_config(log,"warning_keywords.cfg")
    [checkmode_string,check_namelist] = load_config(log,"checkmode.cfg")
    checkmode = 0 if checkmode_string.find("white")!=-1 else 1
    #initialize variables
    warning_extension_count = 0
    warning_keywords_count = 0
    #get the input files
    inputdir_list = os.listdir("input")
    input_list = []
    #start decompiling
    print_log(log,"[Starting decompiling...]")
    for file_name in inputdir_list:
        if file_name.find('.')!=-1 and file_name.rsplit('.',1)[1]=="jar":
            status = os.system("java -jar fernflower-2.0-SNAPSHOT.jar " + file_name + " ./output")
            if status!=0:
                print_log("Error: Failed to decomile " + file_name)
                print_log("Script ends with -1")
                sys.exit(-1)
            else:
                input_list.append(file_name)
                print_log(log,"Successfully decompile " + file_name)
    print_log(log,"[Finish decompiling]")
    #finish decompiling
    #start auto-checking
    if len(input_list)!=0:
        print_log(log,"[Start auto-checking...]")
        for jar_file_name in input_list:
            warning_extension = []
            warning_keywords = []
            print_log(log,"[Start auto-checking " + jar_file_name + "]")
            zf = zipfile.ZipFile("output/" + jar_file_name)
            for name in zf.namelist():
                name_adjusted = name.replace('\\','/')
                file_name = ""
                extension = ""
                #judge if the directory is valid
                if name.find('/')!=-1:
                    file_name = name_adjusted.rsplit('/',1)[1]
                    #judge if the file_name is a valid file name
                    if file_name.find('.')!=-1:
                        extension = '.' + name.rsplit('.',1)[1]
                else:
                    if name.find('.')!=-1:
                        extension = '.' + name.rsplit('.',1)[1]
                #judge if the extension is in the black namelist
                if extension!="" and extension in black_extension_namelist:
                    warning_extension.append([jar_file_name,name])
                #judge if the file should be checked for key words and then check it if it should do so
                if file_name=="" or extension=="":
                    continue
                elif checkmode==0 and not extension in check_namelist:
                    continue
                elif checkmode==1 and extension in check_namelist:
                    continue
                else:
                    file_all = zf.read(name)
                    file_lines = str(file_all).split('\\n')
                    for i in range(1,len(file_lines)+1):
                        for keywords in black_keywords:
                            if file_lines[i-1].find(keywords)!=-1:
                                warning_keywords.append([keywords,jar_file_name,name,i])
            print_log(log,"[Logging warning extensions for " + jar_file_name + "]")        
            for warning in warning_extension:
                print_log(log,"Warning extension: " + warning[0] + ": " + warning[1])
            print_log(log,"[Finish logging warning extensions for " + jar_file_name + "]")
            print_log(log,"[Logging warning key words for " + jar_file_name + "]")
            for i in range(0,len(warning_keywords)):
                print_log(log,"Warning key word: Find \"" + warning_keywords[i][0] + "\" in " + warning_keywords[i][1] + ": " + warning_keywords[i][2] +" Line: " + str(warning_keywords[i][3]))
            print_log(log,"[Finish logging key words for " + jar_file_name + "]")
            print_log(log,"[Finish auto-checking " + jar_file_name + "]")
            warning_extension_count+= len(warning_extension)
            warning_keywords_count+= len(warning_keywords)
        print_log(log,"[Finish all the auto-checking]")
    #time end
    end_time = time.time()
    #last information
    print_log(log,"Find " + str(warning_extension_count) + " warning extensions and " + str(warning_keywords_count) + " warning keywords.")
    print_log(log,"Script ends with 0 in " + str(round(end_time - start_time,2)) + " seconds")
    log.close()

if __name__ == '__main__':
    main()
