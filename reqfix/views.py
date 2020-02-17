from django.shortcuts import render
from .forms import SimpleForm
from re import search


def anonimizer(str):
    regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''

    if search(regex, str):
        return "127.0.0.1"

    else:
        if "http" in str:
            try:
                if ":" in str.split("://")[1]:
                    if search(regex, str.split("://")[1].split(":")[0]):
                        if "https" in str.split("://")[0]:
                            anonstr = "https://127.0.0.1"
                        elif "http" in str.split("://")[0]:
                            anonstr = "http://127.0.0.1"
                        if len(str.split("://")[1].split(":")) > 1:
                            anonstr += ":" + str.split("://")[1].split(":")[1]
                        return anonstr

                else:
                    if "https" in str.split("://")[0]:
                        anonstr = "https://127.0.0.1"
                    elif "http" in str.split("://")[0]:
                        anonstr = "http://127.0.0.1"
                    if len(str.split("://")[1].split(":")) > 1:
                        anonstr += ":" + str.split("://")[1].split(":")[1]
                    else:
                        if len(str.split("/")) > 3:
                            anonstr += "/" + str.split("://")[1].split("/")[1]
                            for strs in range(3, len(str.split("/"))):
                                anonstr += "/" + str.split("/")[strs]
                    return anonstr
            except:
                pass
        return str


def post_new(request):
    form = SimpleForm()
    data = request.POST.get('request')
    try:
        method = data.split("\r\n")[0].split(' ')[0]
        requesturi = anonimizer(data.split("\r\n")[0].split(' ')[1])
    except:
        headers = ""
        boddies = ""
        method = ""
        requesturi = ""
        return render(request, 'reqfix/post_edit.html',
                      {'headers': headers, 'boddies': boddies, 'method': method, 'requesturi': requesturi,
                       'form': form})

    headers = "["
    boddies = ""
    if method == "POST":
        try:
            for header in range(1, len(data.split("\r\n"))):
                if data.split("\r\n")[header].split(':')[0] == '':
                    flag = header
                    break

                else:
                    tmphead = '("' + anonimizer(data.split("\r\n")[header].split(':')[0]) + '",'

                    if len(data.split('\r\n')[header].split(':')) == 2:
                        tmphead += '"' + anonimizer(data.split("\r\n")[header].split(':')[1][1:]) + '"),'
                    else:
                        hds = anonimizer(data.split("\r\n")[header].split(':')[0])
                        tmphead += '"' + anonimizer(data.split("\r\n")[header].split(hds)[1][2:]) + '"),'

                    headers += tmphead

            headers = headers[:-1] + ']'

            for body in range(flag, len(data.split("\r\n"))):
                boddies += anonimizer(data.split("\r\n")[body])
        except:
            headers = "ERROR-POST "

    else:
        for header in range(1, len(data.split("\r\n"))):
            if data.split("\r\n")[header] == "":
                break
            try:
                if len(data.split("\r\n")[header].split(':')) == 2:
                    tmphead = '("' + anonimizer(data.split("\r\n")[header].split(':')[0]) + '",'
                    tmphead += '"' + anonimizer(data.split("\r\n")[header].split(':')[1][1:]) + '"),'
                else:
                    hds = data.split("\r\n")[header].split(':')[0]
                    if hds != "":
                        tmphead = '("' + anonimizer(data.split("\r\n")[header].split(':')[0]) + '",'
                        tmphead += '"' + anonimizer(data.split("\r\n")[header].split(hds)[1][2:]) + '"),'

                headers += tmphead
            except:
                headers = "ERROR-GET "
        headers = headers[:-1] + ']'

    return render(request, 'reqfix/post_edit.html', {'headers': headers, 'boddies': boddies, 'method': method, 'requesturi': requesturi, 'form': form})