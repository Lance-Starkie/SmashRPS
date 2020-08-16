import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

def download_data():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
    client = gspread.authorize(creds)

    sheet = client.open('SmashRps').sheet1

    print("Downloading Data...")
    names = sheet.row_values(1)
    table = {names[i]:{
        names[j]: float((0,val)[val!='-']) for j, val in enumerate(sheet.row_values(i+2))
    } for i, name in enumerate(names)}

    print("Writing...")
    with open('table.json', 'w') as f:
        json.dump(table, f)

    print("Download Complete")

    return table

def load_data():
    print("Loading Data...")
    with open('table.json', 'r') as f:
        out = json.load(f)

    print("Load Complete")

    return out

def main(d = False):
    table = (load_data,download_data)[d]()

    bestscore = -float('inf')
    best = None
    total, total2 = (0, 0)

    print("Processing...")

    for char1 in table:
        for char2 in table:
            if char2!=char1:
                for char3 in table:
                    if not char3 in (char1,char2):
                        score = (
                            sum((
                                abs(table[char1][char2]),
                                abs(table[char2][char3]),
                                abs(table[char3][char1])
                            ))
                            /(abs(sum((
                                abs(table[char1][char2]-table[char2][char3]),
                                abs(table[char2][char3]-table[char3][char1]),
                                abs(table[char3][char1]-table[char1][char2])
                            )))+.5)
                        )
                        if score > bestscore:
                            best = ' vs. '.join((char1,char2,char3))
                            bestscores = (table[char1][char2],table[char2][char3],table[char3][char1])
                            bestscore = score

    print("Score: ",bestscore)
    print(best)
    print(bestscores)
    print("Complete")

def console_input():
    print("Would you like to update the data?(y/n) ")
    if input() in ('y','yes','Y','Yes'):
        main(d = True)
    else:
        main()

if __name__ == '__main__':
    console_input()
