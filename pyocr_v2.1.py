from aip import AipOcr #baiduSDK
from colorama import Fore, Back, Style
import re,time,os,pyperclip,requests,oss2,datetime,base64,sys,getopt
def initialization():
    APP_ID = 'YOUR APP ID OF BAIDU AI HERE'
    API_KEY = 'YOUR API KEY OF BAIDU AI HERE'
    SECRET_KEY = 'YOUR API SECERT OF BAIDU AI HERE'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    return client
def getclipboard():
    print("Checking your clipboard....") #
    clipboard = pyperclip.paste()
    print("Done.")
    urlflag = ifurl(clipboard)
    flag = True
    if urlflag:
        print("Found URL in your clipboard,starting OCR....")
        return flag,clipboard
    else:
        print("Didn't find URL or Path in your clipboard.")
        flag = False
        return flag,''
def ifurl(input_text):
    regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' 
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' 
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    flag = re.match(regex,input_text) is not None
    return flag
def input_url_path(num):
    if num == 1:
        key = 1
    elif num == 2:
        key = 2
    elif num == 3:
        key = 3
    else:
        key = input("URL:1\nPATH:2\nAutomatic mode:3\nPlease enter a number:")
        if key.isdigit() == False:
            print("Input invaild! Please enter a NUMBER! ('"+key+"' is not a NUMBER!)")
            (flag,localpath,osspath,filename) = input_url_path(4)
        key = int(key)
    if key == 1:
        url = input("Enter image URL here:")
        return True,url,'',''
    elif key == 2:
        localpath = input("Please enter your image path:")
        localpath = localpath.strip('"')
        if os.path.exists(localpath):
            filename = os.path.basename(localpath)
            print("img path:"+localpath)
            osspath = 'img/'+filename
            print("Filename:"+filename)
            if os.path.splitext(localpath)[1] not in ['.png','.jpg','.jpeg','.PNG','.JPG','.JPEG']:
                if os.path.splitext(localpath)[1].isalpha():
                    filetype = os.path.splitext(localpath)[1].upper()
                    pass
                else:
                    filetype = os.path.splitext(localpath)[1].upper()
                    pass
                print("Unsupported filetype(" + filetype + ")")
                (flag,localpath,osspath,filename)=input_url_path(2)
            flag = reask_er(False)
            if flag == False:
                (flag,localpath,osspath,filename)=input_url_path(2)
                return flag,localpath,osspath,filename
            elif flag:
                flag = False
                return flag,localpath,osspath,filename
        else:
            print("Path invaild,Please enter exist path")
            input_url_path(2)         
    elif key == 3:
        automatic_analyze()
    else:
        print("Input invaild,please try again")
        input_url_path(4)
def reask_er(flag):
    if flag == True:
        reask = input("Please type 'Y' for Yes or 'N'for No.:") 
        if reask == 'Y':
            return True
        elif reask == 'y':
            return True
        elif reask == 'N':
            return False
        elif reask == 'n':
            return False
        else:
            reask_er(True)
    else:
        tmp = input("Are they right? <Y/N>")
        if tmp == 'Y':
            return True
        elif tmp == 'y':
            return True
        elif tmp == 'N':
            return False
        elif tmp == 'n':
            return True
        else:
            reask_er(True)
def ocr(url,client):
    print("Starting OCR...")
    result = client.basicGeneralUrl(url)
    print("Done.")
    return result
def filename_generator():
    time_str = datetime.datetime.now().strftime('%F-%H-%M-%S')
    filename='C:\\result\\' + time_str + '.txt'
    return filename
def result_analyze(result,url,filename_export,retry=True):
    try:
        nummax = result['words_result_num']
        i = 0
        copytext = ""
        print("RESULT:")
        for i in range(0,nummax):
            copytext += result['words_result'][i]['words']
            print(result['words_result'][i]['words'])
            with open(filename_export,'w') as f:
                f.write(result['words_result'][i]['words'])
                f.write("\n")
                f.close
        return copytext,filename_export
    except KeyError as k:
        print(result['error_msg'])
        if result['error_msg'] == 'url download timeout':
            print(url)
            print("Trying another way...")
            command = "curl " + url + "--output .\\img_file.png"
            os.system(command)
            img_data = get_file_content('.\\img_file.img')
            APP_ID = '18817222'
            API_KEY = 'FkS19NB2a0vOYZMi0XGakn9K'
            SECRET_KEY = 'GWA0OuG8zkGxCkIMkVUUfUtzPXO7pGpX'
            client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
            result = client.basicAccurate(img_data)
            copytext=result_analyze(result=result,url=url,filename_export=filename_export)
            return copytext,filename_export
        else:
            print("An Error Occured")
            print(k)
            os._exit(0)
    finally:
        if os.path.exists('.\\Error.log'):
            os.remove('.\\Error.log')
def export_result(copytext,filename_export):
    copytext = str(copytext)
    pyperclip.copy(copytext)
    print("Result(s) is/are copyed to your clipboard\nIt's also saved as "+filename_export)
def oss_upload(osspath,localpath,filename):
    print("Uploading to OSS...")
    auth = oss2.Auth('YOUR OSS API KEY OF ALIYUN OSS', 'YOUR API SECRET OF ALIYUN OSS')
    bucket = oss2.Bucket(auth, 'YOUR LOCATION DOMIN', 'YOUR SUBDOMIN')
    bucket.put_object_from_file(osspath, localpath)
    img_url = 'YOUR OSS URL(REMOTE)' + filename
    print("Done.")
    return img_url
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
def automatic_analyze():
    APP_ID = 'YOUR APP ID OF BAIDU AI HERE'
    API_KEY = 'YOUR API KEY OF BAIDU AI HERE'
    SECRET_KEY = 'YOUR API SECERT OF BAIDU AI HERE'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    print("Automatic OCR started")
    filename_export = filename_generator()
    while True:
        try:
            clipboard = pyperclip.paste()
            flag = ifurl(clipboard)
            if flag:
                print("Found URL in your clipboard,starting OCR....")
                result = ocr(url = clipboard,client=client)   
                (analyzed_data,filename_export)= result_analyze(result=result,url=clipboard,filename_export=filename_export)
                export_result(analyzed_data,filename_export)
        except KeyboardInterrupt as e:
            print("***Got a Keyboard Interrupt,program is exiting...")
            e = str(e)
            with open("Error.log",'w') as f:
                f.write(e)
                f.close()
            os.system("pause")
            os._exit(0)#Kill this program
        finally:
            if os.path.exists('.\\Error.log'):
                os.remove('.\\Error.log')
        time.sleep(0.1)
def main():
    try:
        # argv_length = len(sys.argv)
        if os.path.exists('C:\\result\\') == False:
            os.system("mkdir C:\\result\\")
        filename_export = filename_generator()
        print("Initializing...")
        client = initialization()
        (if_clipboard_url,clipboard) = getclipboard()
        if if_clipboard_url:
            result = ocr(url=clipboard,client=client)
            img_url = clipboard
            analyzed_data = result_analyze(result=result,url=img_url,filename_export=filename_export)
            export_result(analyzed_data,filename_export)
        else:
            (isUrl,localpath_or_url,osspath,filename) = input_url_path(4)
            if isUrl:#URL
                while True:
                    result = ocr(url=localpath_or_url,client=client)
                    img_url = localpath_or_url
                    analyzed_data = result_analyze(result=result,url=img_url,filename_export=filename_export)
                    export_result(analyzed_data,filename_export)
                    (isUrl,localpath_or_url,osspath,filename) = input_url_path(1)
            else:#PATH
                while True:
                    img_url = oss_upload(osspath=osspath,localpath=localpath_or_url,filename=filename)
                    result = ocr(url = img_url,client = client)
                    analyzed_data = result_analyze(result=result,url=img_url,filename_export=filename_export)
                    export_result(analyzed_data,filename_export)
                    (isUrl,localpath_or_url,osspath,filename) = input_url_path(2)
        print("Done.")
        return 0
    except KeyboardInterrupt as ex:
        print("\n***Got a Keyboard Interrupt,program is exiting...")
        with open("Error.log",'w') as f:
                f.write(str(ex))
                f.close()
        os.system("pause")
        os._exit(0)#Kill this program
    # finally:
    #     os.remove('.\\Error.log')
if __name__ == "__main__":
    # main(sys.argv[1:])
    main()