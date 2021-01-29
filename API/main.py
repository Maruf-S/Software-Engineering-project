from flask import  Flask, jsonify, request
import mechanize
from bs4 import BeautifulSoup

def get_result(page):
    read=page
    soup = BeautifulSoup(read,'html.parser')
    i_items = [["1"], ["2"], ["3"], ["4"], ["5"], ["6"], ["7"]]
    total_list = []
    clean_list = []
    for tx in soup.find_all('td'):
        total_list.append(list(tx.stripped_strings))
    if "Academic Year" in total_list:
        pass
    mesh_string = ""
    for i in total_list:
        if i == ['Assessment']:
            pass
        elif 'Academic Year' in (str(i)):
            clean_list.append(
                "---------------------------------------")
            clean_list.append(i)
            clean_list.append("---------------------------------------")
        elif "'Academic Status : " in (str(i)) and "SGPA" in (str(i)):
            x = (str(i).find("SGPA"))
            clean_list.append(''.join((str(i)[x:x + 11])))
            if "'Academic Status :" in (str(i)) and "CGPA" in (str(i)):
                x = (str(i).find("CGPA"))
                clean_list.append(''.join((str(i)[x:x + 11])))
                ass = (str(i).find("Academic Status :"))
                clean_list.append(''.join(i[ass:ass + 28]))
        elif "'Academic Status : failed" in (str(i)):
            clean_list.append(''.join("Academic Status : failed"))
        elif i in i_items:
            clean_list.append("---------------------------------------")
        else:
            clean_list.append(''.join(i))
    total_list = None
    for i in clean_list:
        mesh_string += ((str(i)) + "\n")
    return (mesh_string.replace("'",""))
def send_name(page):
    read = page
    soup=BeautifulSoup(read,'html.parser')
    total_list=[]
    clean_list=[]
    mesh_string=str()
    for tx in soup.find_all('td'):
        total_list.append(list(tx.stripped_strings))
    for i in total_list:
        clean_list.append(''.join(i))
    for i in clean_list:
        mesh_string+=(str(i)+"\n")
    return(mesh_string)


def Get_the_results(username,password):
    try:
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [("User-agent", "Mozilla/5.0")]
        gitbot = br.open("https://portal.aait.edu.et/")
        br.select_form(nr=0)
        br["UserName"] = username
        br["Password"] = password
        br.submit()
        rname=br.response().read()
        if ("before your account gets locked out" in str(rname)):
            ss = BeautifulSoup(rname, 'html.parser')
            check_text = ss.find('div', {'class': 'validation-summary-errors'}).find('li').text
            return jsonify(error=f"{check_text} ATTEMPTS BEFORE YOUR ACCOUNT GETS LOCKED OUT", code=2)
            print(f"{check_text} ATTEMPTS BEFORE YOUR ACCOUNT GETS LOCKED OUT")
            # context.bot.send_message(chat_id=id, text="<code>"+check_text+"</code>",parse_mode=telegram.ParseMode.HTML)
        elif ("Your account has been locked out" in str(rname)):#Send_Text('Your account has been locked out due to multiple failed login attempts.', id,request="<code>")
            print("You Fucked UP")
            return jsonify(error=f'You Fucked UP, this acc is no more')
            # context.bot.send_message(chat_id=id, text="<code>"+'Your account has been locked out due to multiple failed login attempts.'+"</code>",parse_mode=telegram.ParseMode.HTML)
        elif ("GradeReport" in str(rname)):#### it was an else before
            req = br.click_link(url="/Grade/GradeReport")
            br.open(req)
            content = (br.response().read())
            nemo=send_name(rname)
            con=(get_result(content))
            #Send_Text(nemo,id,request="<code>")
            #Send_Text(con, id,request="<code>")
            print("USERINFO:\n"+nemo)
            #2321321312@!3#!@32!!427uhdjqbl quogfu/jbgw quhnfkwj poqejmkelw bjmk,n
            return jsonify(data=nemo,gradereport=con)
            # context.bot.send_message(chat_id=id, text="<code>" + nemo + "</code>",
            #                          parse_mode=telegram.ParseMode.HTML)
            print("USERGRADEREPORT\n" + con)
            # if (len(con) <= 4100):
            #     context.bot.send_message(chat_id=id, text="<code>" + con + "</code>",parse_mode=telegram.ParseMode.HTML)
            # else:
            #     context.bot.send_message(chat_id=id, text="<code>" + con[:4000] + "</code>",
            #                              parse_mode=telegram.ParseMode.HTML)
            #     context.bot.send_message(chat_id=id, text="<code>" + con[4000:] + "</code>",
            #                              parse_mode=telegram.ParseMode.HTML)
        else:
            print("The username or the password is incorrect, Make sure you submitted both as for example \n Atr/2020/10,2020")
            return jsonify(code=3, error = "Invalid credentials! Make sure you submitted both as for example \n Atr/2020/10,2020")
            # context.bot.send_message(chat_id=id,
            #                          text="<code>" + "The username or the password is incorrect, Make sure you submitted both as for example \n Atr/2020/10,2020" + "</code>",
            #                          parse_mode=telegram.ParseMode.HTML)
    except Exception as e:
        print("An internal error has occurred please try again later.")
        print(e)
        raise Exception(e)
        return jsonify(code=4,error=f"{e}")
        # context.bot.send_message(chat_id=id,
        #                          text="<code>" + "An internal error has occurred please try again later." + "</code>",
        #                          parse_mode=telegram.ParseMode.HTML)
        #Send_Text("The username or the password is incorrect, Make sure you submitted both as for example \n Atr/2020/10,2020",id,request="<code>")
app = Flask(__name__)
app.config["DEBUG"] = True
@app.route("/",methods=['GET'])

def dummy_api():
    username = request.args.get("username")
    password = request.args.get("password")
    if(username and password):
        return Get_the_results(username,password),200
        return jsonify(data="Jello"+username+password)
    else:
        return  jsonify(error="404 not found",code=1), 404

if __name__ == "__main__":
    app.run()