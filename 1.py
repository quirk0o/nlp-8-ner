import json, urllib2
import glob, os
import time

url = "http://ws.clarin-pl.eu/nlprest2/base"

in_path = 'data/test.txt'
out_path = 'out/'


def upload(file):
    with open(file, "r") as myfile:
        doc = myfile.read()
    return urllib2.urlopen(urllib2.Request(url + '/upload/', doc, {'Content-Type': 'binary/octet-stream'})).read()


def tool(lpmn, user):
    data = {}
    data['lpmn'] = lpmn
    data['user'] = user

    doc = json.dumps(data)
    taskid = urllib2.urlopen(urllib2.Request(url + '/startTask/', doc, {'Content-Type': 'application/json'})).read()
    time.sleep(0.1)
    resp = urllib2.urlopen(urllib2.Request(url + '/getStatus/' + taskid))
    data = json.load(resp)
    while data["status"] == "QUEUE" or data["status"] == "PROCESSING":
        time.sleep(0.1)
        resp = urllib2.urlopen(urllib2.Request(url + '/getStatus/' + taskid))
        data = json.load(resp)
    if data["status"] == "ERROR":
        print("Error " + data["value"])
        return None
    return data["value"]


def main():
    global_time = time.time()
    for afile in glob.glob(in_path):
        start_time = time.time()
        data = upload(afile)

        data = tool('file(' + data + ')|any2txt|wcrft2|liner2({\"model\":\"5nam\"})', 'adres e-mail')

        if data == None:
            continue
        data = data[0]["fileID"]
        content = urllib2.urlopen(urllib2.Request(url + '/download' + data)).read()
        with open(out_path + os.path.basename(afile) + '.ccl', "w") as outfile:
            outfile.write(content)
        print("--- %s seconds ---" % (time.time() - start_time))
    print("GLOBAL %s seconds ---" % (time.time() - global_time))


if __name__ == '__main__':
    main()
