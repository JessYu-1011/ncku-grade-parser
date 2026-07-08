import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def gpa_to_points(gpa):
    if gpa == 'A+':
        return 4.3
    elif gpa == 'A':
        return 4.0
    elif gpa == 'A-':
        return 3.7
    elif gpa == 'B+':
        return 3.3
    elif gpa == 'B':
        return 3.0
    elif gpa == 'B-':
        return 2.7
    elif gpa == 'C+':
        return 2.3
    elif gpa == 'C':
        return 2.0
    elif gpa == 'C-':
        return 1.7
    elif gpa == 'F':
        return 0

def process_each_semester():
    global total_weighted_scores, total_credits
    subjects_table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/table')))
    subject_rows = subjects_table.find_elements(By.TAG_NAME, 'tr')
    semester_credits = 0
    semester_weighted_scores = 0.0
    for subject in subject_rows:
        subject_tds = subject.find_elements(By.TAG_NAME, 'td')
        if len(subject_tds) < 9: continue
        course_type = subject_tds[6].text.strip()

        if course_type not in ["必修", "選修"]:
            continue
        credits_int = int(subject_tds[5].text)
        grades = subject_tds[7].text
        gpa = subject_tds[8].text
        if grades.isnumeric():
            gpa_points = gpa_to_points(gpa)
            semester_credits += credits_int
            semester_weighted_scores += gpa_points*credits_int
    
    total_credits += semester_credits
    total_weighted_scores += semester_weighted_scores
    print(f"Semester credits: {semester_credits}, weighted scores: {semester_weighted_scores:.2f} gpa: {(semester_weighted_scores/semester_credits):.2f}")

def calculate_semeseters(semester_table):
    every_semesters_buttons = semester_table.find_elements(By.TAG_NAME, 'input')
    return len(every_semesters_buttons)

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://qrys.ncku.edu.tw/ncku/qrys05.asp')
wait = WebDriverWait(driver, 30)
history_grades = wait.until(lambda d: d.find_element(By.LINK_TEXT, "歷年成績資料查詢"))
history_grades.click()
semester_table = driver.find_element(By.XPATH, '//*[@id="form1"]/table')
total_semesters = calculate_semeseters(semester_table)
print(f"Total semesters: {total_semesters}")
subject_grades = []

total_weighted_scores = 0
total_credits = 0


while total_semesters > 0:
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/table')))
        semester_table = driver.find_element(By.XPATH, '//*[@id="form1"]/table')
        every_semesters_buttons = semester_table.find_elements(By.TAG_NAME, 'input')
        button = every_semesters_buttons[total_semesters-1]
        print(button.get_attribute('value'))
        wait.until(EC.element_to_be_clickable(button))
        button.click()
        time.sleep(1)
        process_each_semester()
        time.sleep(1)
        driver.back()
        time.sleep(2)
        total_semesters = total_semesters - 1
    except Exception as e:
        print("點擊失敗: "+ str(e))
        time.sleep(2)


print(f"Total credits: {total_credits}  Total_weighted_scores:{total_weighted_scores:.2f}")
print(f"Overall GPA: {(total_weighted_scores/total_credits):.2f}")

driver.quit()