from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import mysql.connector
import time
import datetime

db = mysql.connector.connect(
    host="localhost",
    user="haryauyee",
    passwd="password",
    database="rakamin_mobil"
    )

mycursor = db.cursor(buffered=True)
selectvin = "select count(*) from mobil_null"
mycursor.execute(selectvin)

for row in mycursor:
    print(row)


selectvin = "select count(*) from mobil_null"


selectvin = ("select vin from vin_null order by vin limit 1000000 offset %s")
mycursor.execute(selectvin, row)

x = list()
for v in mycursor:
    print(v[0])
    x.append(v[0])

print(x)

path = "C:\Program Files\Microsoft Office\msedgedriver.exe"
web = webdriver.Edge(path)
# path = "C:\Program Files (x86)\Google\Chrome\chromedriver.exe"
# web = webdriver.Chrome(path)
web.get ('https://epicvin.com/vin-decoder')
time.sleep(3)

row = int(row[0])
print("Starting Row:", row)

for vin in x: 
    try:
        assert(web.service.process.poll() == None) #Returns an int if dead and None if alive
        web.service.assert_process_still_running() #Throws a WebDriverException if dead
        web.find_element(By.TAG_NAME, 'html') #Throws a NoSuchElementException if dead
        print('The driver appears to be alive')
    except:
        print('The driver appears to be dead')
        web = webdriver.Edge(path)
        web.get ('https://epicvin.com/vin-decoder')
        time.sleep(3)

    try:
        vinfill = web.find_element('xpath', '/html/body/div[2]/main/article/div[1]/div/div[1]/form/input')
        vinfill.clear()
        vinfill.send_keys(vin)

        button = web.find_element('xpath', '/html/body/div[2]/main/article/div[1]/div/div[1]/form/button')
        button.click()
        time.sleep(0.5)
        try:
            WebDriverWait(web, 900).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[2]/main/article/div[5]/div/div')))
        except TimeoutException:
            print("TIMEOUT ! ! !")

        make = web.find_element(By.XPATH, '/html/body/div[2]/main/article/div[2]/div/div[2]/div[1]/div/div[1]/div/div[2]/div[2]/h5')
        make = str(make.text)
        print("Make:", make)
        model = web.find_element(By.XPATH, '/html/body/div[2]/main/article/div[2]/div/div[2]/div[1]/div/div[1]/div/div[2]/div[3]/h5')
        model = str(model.text)
        print("Model:", model)
        trim = web.find_element(By.XPATH, '/html/body/div[2]/main/article/div[2]/div/div[2]/div[1]/div/div[1]/div/div[2]/div[4]/h5')
        trim = str(trim.text)
        print("Trim:", trim)
        bodyclass = web.find_element(By.XPATH,'/html/body/div[2]/main/article/div[2]/div/div[2]/div[1]/div/div[1]/div/div[2]/div[11]/h5')
        bodyclass = str(bodyclass.text)
        print("Body:", bodyclass)
        transmission = web.find_element(By.XPATH, '/html/body/div[2]/main/article/div[2]/div/div[2]/div[1]/div/div[1]/div/div[2]/div[7]/h5')
        transmission = str(transmission.text)
        print("Transmission:", transmission)

        sql = ("INSERT INTO mobil_null"
                "(make, model, trim, body, transmission, vin)"
                "VALUES (%s, %s, %s, %s, %s, %s)")
        val = (make, model, trim, bodyclass, transmission, vin)
        mycursor.execute("use rakamin_mobil")
        mycursor.execute(sql, val)
        time.sleep(0.5)
        db.commit()
        web.find_element('xpath', '/html/body/div[2]/main/article/div[1]/div/div[1]/form/input').clear()

        print("Row Number:", row)
        row += 1
        print("TIME:", datetime.datetime.now(), "VIN:", vin, "OKE!!! \n\n")
    except NoSuchElementException:
        print("TIME:", datetime.datetime.now(), "NO DATA ! ! ! \n\n")
        row += 1
        continue

web.quit()