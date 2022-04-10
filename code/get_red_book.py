"""
Data set preparation for Penn State study using machine learning
and natural language processing methods to classify patents

Data published by USPTO Bulk Data Storage System
Red Book, Patent Grant Full Text Data (No Images), Weekly, 2018

https://www.wipo.int/export/sites/www/standards/en/pdf/03-36-01.pdf

https://www.uspto.gov/sites/default/files/products/43AIACPCXML-Documentation-508version.pdf

"""

"""
IMPORTS
"""

import xml.etree.ElementTree as ET
import csv
import string
import urllib.request
import os
import zipfile


"""
PROCEDURES
"""

def download_wklys(wkly, datadir):
    # Download the weekly publication files
    for w in wkly:
        print("Downloading",w)
        geturl = 'https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2021/ipg' + w + '.zip'
        urllib.request.urlretrieve(geturl, datadir + "/ipg" + w + ".zip")
    return

def unzip_wklys(wkly, datadir):
    # Unzip them, creating subdirectories for each
    os.chdir(datadir)
    for w in wkly:
        # mute = os.system('c:/"Program Files"/7-zip/7z.exe x ipg' + w + '.zip -oipg' + w)
        print("Unzipping",w)
        with zipfile.ZipFile(datadir + '/ipg' + w + '.zip', 'r') as z:
                z.extractall(datadir + '/ipg' + w)
    return

def fix_xml(wkly, datadir):
    # Restructure the xml, removing <?xml> <!DOCTYPE> and wrapping a <rootnode>
    for w in wkly:
        print("Fixing",w)
        with open(datadir + "/ipg" + w + "/ipg" + w + ".fix", 'w') as new_file:
            with open(datadir + "/ipg" + w + "/ipg" + w + ".xml") as old_file:
                mute = new_file.write("<rootnode>\n")
                for line in old_file:
                    if ("<?xml " not in line) and ("DOCTYPE" not in line):
                        mute = new_file.write(line)
                mute = new_file.write("</rootnode>")
    return

for w in wkly:
    print("Extracting fields for",w)
    print(datetime.now().strftime("%H:%M:%S"))
    with open(datadir + "/ipg" + w + "/txt" + w + ".csv", 'w', newline='') as txt_file:
        with open(datadir + "/ipg" + w + "/ipc" + w + ".csv", 'w', newline='') as ipc_file:
            write_txt = csv.DictWriter(txt_file, fieldnames=txt_fields)
            write_txt.writeheader()
            write_ipc = csv.DictWriter(ipc_file, fieldnames=ipc_fields)
            write_ipc.writeheader()
            e = ET.parse(datadir + "/ipg" + w + "/ipg" + w + ".fix").getroot()
            for child in e:
                if child.tag == 'us-patent-grant':
                    pub = child.find('us-bibliographic-data-grant').find('publication-reference').find(
                        'document-id').find(
                        'doc-number').text
                    ver = ''
                    lev = ''
                    sec = ''
                    cla = ''
                    subc = ''
                    grp = ''
                    subg = ''
                    pos = ''
                    cv = ''
                    act = ''
                    gen = ''
                    sta = ''
                    src = ''
                    a = ''
                    c = ''
                    d = ''
                    try:
                        natctry = child.find('us-bibliographic-data-grant').find('classification-national').find(
                            'country').text
                        natcla = child.find('us-bibliographic-data-grant').find('classification-national').find(
                            'main-classification').text
                    except:
                        a = [elem.text for elem in child.find('abstract').iter()]
                        a = " ".join(x for x in a if x is not None)
                        a = "".join(x for x in a if x in string.printable)
                        c = [elem.text for elem in child.find('claims').iter()]
                        c = " ".join(x for x in c if x is not None)
                        c = "".join(x for x in c if x in string.printable)
                        d = [elem.text for elem in child.find('description').iter()]
                        d = " ".join(x for x in d if x is not None)
                        d = "".join(x for x in d if x in string.printable)
                        cpc = child.find('us-bibliographic-data-grant').find('classifications-cpc').find('main-cpc').find('classification-cpc').find('section').text+child.find('us-bibliographic-data-grant').find('classifications-cpc').find('main-cpc').find('classification-cpc').find('class').text
                        typ = child.find('us-bibliographic-data-grant').find('application-reference').get('appl-type')
                        mute = write_txt.writerow({'pub': pub,
                                                   'typ': typ,
                                                   'cpc': re.sub(r'[\x00-\x1F]',' ', unidecode(cpc)),
                                                   'desc': re.sub(r'[\x00-\x1F]',' ', unidecode(d)),
                                                   'abstract': re.sub(r'[\x00-\x1F]',' ', unidecode(a)),
                                                   'claims': re.sub(r'[\x00-\x1F]',' ', unidecode(c))
                                                   })
                        for c in child.find('us-bibliographic-data-grant').find('classifications-ipcr').findall(
                                    'classification-ipcr'):
                            ver = c.find('ipc-version-indicator').text
                            lev = c.find('classification-level').text
                            sec = c.find('section').text
                            cla = c.find('class').text
                            subc = c.find('subclass').text
                            grp = c.find('main-group').text
                            subg = c.find('subgroup').text
                            pos = c.find('symbol-position').text
                            cv = c.find('classification-value').text
                            act = c.find('action-date').text
                            gen = c.find('generating-office').text
                            sta = c.find('classification-status').text
                            src = c.find('classification-data-source').text
                            mute = write_ipc.writerow({'pub': pub,
                                                       'tri': sec + cla + subc,
                                                       'ver': ver,
                                                       'lev': lev,
                                                       'sec': sec,
                                                       'cla': cla,
                                                       'subc': subc,
                                                       'grp': grp,
                                                       'subg': subg,
                                                       'pos': pos,
                                                       'cv': cv,
                                                       'act': act,
                                                       'gen': gen,
                                                       'sta': sta,
                                                       'src': src
                                                       })

def zip_wklys(wkly, datadir):
    # zip the ipc files
    os.chdir(datadir)
    for w in wkly:
        mute = os.system('c:/"Program Files"/7-zip/7z.exe a ipc18' + w + '.zip ./ipg18' + w + '/ipc18' + w + '.csv')
    # zip the txt files
    os.chdir(datadir)
    for w in wkly:
        mute = os.system('c:/"Program Files"/7-zip/7z.exe a txt18' + w + '.zip ./ipg18' + w + '/txt18' + w + '.csv')
    return


"""
MAIN
"""


def main():

    # 2018 pull
    datadir = "D:/Projects/patentclass"

    wkly = ['1225', '1218', '1211', '1204', '1127', '1120', '1113', '1106', '1030', '1023', '1016', '1009', '1002', '0925',
            '0918', '0911', '0904', '0828', '0821', '0814', '0807', '0731', '0724', '0717', '0710', '0703', '0626', '0619',
            '0612', '0605', '0529', '0522', '0515', '0508', '0501', '0424', '0417', '0410', '0403', '0327', '0320', '0313',
            '0306', '0227', '0220', '0213', '0206', '0130', '0123', '0116', '0109', '0102']

    ipc_fields = ['pub','tri','ver','lev','sec','cla','subc','grp','subg','pos','cv','act','gen','sta','src']

    txt_fields = ['pub', 'typ', 'desc', 'abstract', 'claims']

    # 2021 pull
    datadir = "D:/Projects/patents"
    wkly = ['210105', '210112', '210119', '210126', '210202', '210209', '210216', '210223', '210302', '210309',
            '210316', '210323', '210330', '210406', '210413', '210420', '210427', '210504', '210511', '210518',
            '210525', '210601', '210608', '210615', '210622', '210629', '210706', '210713', '210720', '210727',
            '210803', '210810', '210817', '210824', '210831', '210907', '210914', '210921', '210928', '211005',
            '211012', '211019', '211026', '211102', '211109', '211116', '211123', '211130', '211207', '211214',
            '211221', '211228']
    ipc_fields = ['pub', 'tri', 'ver', 'lev', 'sec', 'cla', 'subc', 'grp', 'subg', 'pos', 'cv', 'act', 'gen', 'sta',
                  'src']
    txt_fields = ['pub', 'typ', 'desc', 'abstract', 'claims']

    download_wklys(wkly, datadir)
    unzip_wklys(wkly, datadir)
    fix_xml(wkly, datadir)
    pull_csv(wkly, datadir, txt_fields, ipc_fields)
    zip_wklys(wkly, datadir)
    return


if __name__ == '__main__':
    main()
