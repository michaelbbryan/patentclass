
def counttags(node):
    c = {}
    for child in node:
        c[child.tag] = c.get(child.tag, 0) + 1
    for i in c:
        print('\t' + i + '\t' + str(c[i]))

wkly = ['1225', '1218', '1211', '1204', '1127', '1120', '1113', '1106', '1030', '1023', '1016', '1009', '1002', '0925',
        '0918', '0911', '0904', '0828', '0821', '0814', '0807', '0731', '0724', '0717', '0710', '0703', '0626', '0619',
        '0612', '0605', '0529', '0522', '0515', '0508', '0501', '0424', '0417', '0410', '0403', '0327', '0320', '0313',
        '0306', '0227', '0220', '0213', '0206', '0130', '0123', '0116', '0109', '0102']

datadir = "D:/Projects/ipg"

with open("wksql.sql",'w') as s:
    for w in wkly:
        s.write(
            "load data local infile '"+datadir+\
            "/ipg18"+w+"/txt18"+w+\
            ".csv' into table txt fields terminated by ',' lines terminated by '\n' "+\
            "ignore 1 rows (pub,typ,dsc,abstr,clms) set wk = '"+w+"'; \n")
