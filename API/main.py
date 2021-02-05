import mechanize

from flask import Flask, jsonify, request
from bs4 import BeautifulSoup


def get_result(page):
    read = page
    soup = BeautifulSoup(read, 'html.parser')
    i_items = [["1"], ["2"], ["3"], ["4"], ["5"], ["6"], ["7"]]
    total_list = []
    clean_list = []
    grade_dict = {}
    a = {}

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
                "|")
            clean_list.append(i)

        elif "'Academic Status : " in (str(i)) and "SGPA" in (str(i)):
            x = (str(i).find("SGPA"))
            clean_list.append("+"+''.join((str(i)[x:x + 11])))
            if "'Academic Status :" in (str(i)) and "CGPA" in (str(i)):
                x = (str(i).find("CGPA"))
                clean_list.append("+"+''.join((str(i)[x:x + 11])))
                ass = (str(i).find("Academic Status :"))
                clean_list.append("+"+''.join(i[ass:ass + 28]))
        elif "'Academic Status : failed" in (str(i)):
            clean_list.append(''.join("Academic Status : failed"))
        elif i in i_items:
            clean_list.append("--")
        else:
            clean_list.append("_"+''.join(i))

    total_list = None
    for i in clean_list:
        mesh_string += str(i)
    return (mesh_string.replace("'", ""))

# def send_name(page):
#     soup = BeautifulSoup(page, 'html.parser')
#     name_list = [tx.text.strip() for tx in soup.find_all(
#         'td') if len(tx.text) > 2]
#     return name_list


def send_details(page):
    soup = BeautifulSoup(page, 'html.parser')
    email = soup.find('input', {'id': 'Email'}).get('value')
    telephone = soup.find('input', {'id': 'Telephone'}).get('value')
    year = soup.find('input', {'id': 'Year'}).get('value')
    month = soup.find('input', {'id': 'Month'}).get('value')
    day = soup.find('input', {'id': 'Date'}).get('value')
    info = [tx.text.strip() for tx in soup.find_all(
        'td') if len(tx.text) > 2]

    details_obj = {
        "info": info,
        "email": email,
        "telephone": telephone,
        "birth": year + "/" + month + "/" + day
    }
    return details_obj


def Get_the_results(username, password):

    try:
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [("User-agent", "Mozilla/5.0")]
        gitbot = br.open("https://portal.aait.edu.et/")
        br.select_form(nr=0)
        br["UserName"] = username
        br["Password"] = password
        br.submit()
        rname = br.response().read()
        if ("before your account gets locked out" in str(rname)):
            ss = BeautifulSoup(rname, 'html.parser')
            check_text = ss.find(
                'div', {'class': 'validation-summary-errors'}).find('li').text
            return jsonify(error=f"{check_text} ATTEMPTS BEFORE YOUR ACCOUNT GETS LOCKED OUT", code=2)
            print(f"{check_text} ATTEMPTS BEFORE YOUR ACCOUNT GETS LOCKED OUT")

        elif ("Your account has been locked out" in str(rname)):
            print("You Fucked UP")
            return jsonify(error=f'You Fucked UP, this acc is no more')
        elif ("GradeReport" in str(rname)):  # it was an else before

            req = br.click_link(url="/Grade/GradeReport")
            br.open(req)
            content = (br.response().read())
            grade_string = (get_result(content))

            grade_string = grade_string.replace("[", "")
            grade_string = grade_string.replace("]", "")

            split_one = grade_string.split("|")
            cgpa = []
            sgpa = []
            m = [semester.split("--") for semester in split_one]
            d = {}

            details_pg = br.click_link(url='/StudentRecords/BasicInformation')
            br.open(details_pg)
            details = send_details(br.response().read())

            for j in range(len(m) - 1):
                courses = []
                for course in (m[j+1][1:]):
                    cl = course.split('_')
                    course_object = {
                        "couse_name": cl[1],
                        "course_id": cl[2],
                        "ects": cl[3],
                        "chr": cl[4],
                        "grade": cl[5][:2],
                    }
                    courses.append(course_object)
                # year x -- sem y
                d[(m[j+1][0][m[j+1][0].find("Year "): m[j+1][0].find("Year ") + 8]).replace(",", "").strip() + " -- semester " + (m[j+1][0][-3:])] = {
                    # ac y
                    m[j+1][0][:13]: m[j+1][0][17:24],
                    # year
                    "year": (m[j+1][0][m[j+1][0].find("Year "): m[j+1][0].find("Year ") + 8]).replace(",", "").strip(),
                    # semester
                    "semester " + (m[j+1][0][-3:]): {"courses": courses,

                                                     # finding cgpa with index
                                                     "cgpa": (m[j+1][-1][m[j+1][-1].find("CGPA") + 7: m[j+1][-1].find("CGPA") + 11]),
                                                     # sgpa
                                                     "sgpa": (m[j+1][-1][m[j+1][-1].find("SGPA") + 7: m[j+1][-1].find("SGPA") + 11]),

                                                     }

                }
                cgpa.append(
                    (m[j+1][-1][m[j+1][-1].find("CGPA") + 7: m[j+1][-1].find("CGPA") + 11]))
                sgpa.append(
                    (m[j+1][-1][m[j+1][-1].find("SGPA") + 7: m[j+1][-1].find("SGPA") + 11]))

            # creating person object with details result
            person = {"name": details["info"][1],
                      "id": details["info"][5],
                      "department": details["info"][3],
                      "year": details["info"][7],
                      "birth": details["birth"],
                      "mail": details["email"],
                      "telephone": details["telephone"],
                      "cgpa": cgpa,
                      "sgpa": sgpa
                      }

            return jsonify(data={"profile": person, "grade": d})

        else:
            print("The username or the password is incorrect, Make sure you submitted both as for example \n Atr/2020/10,2020")
            return jsonify(code=3, error="Invalid credentials! Make sure you submitted both as for example \n Atr/2020/10,2020")

    except Exception as e:
        print("An internal error has occurred please try again later.")
        print(e)
        raise Exception(e)
        return jsonify(code=4, error=f"{e}")


app = Flask(__name__)
app.config["DEBUG"] = True
@app.route("/", methods=['GET'])
def dummy_api():
    username = request.args.get("username")
    password = request.args.get("password")
    if(username and password):
        return Get_the_results(username, password), 200
    else:
        return jsonify(error="404 not found", code=1), 404


if __name__ == "__main__":
    app.run()
