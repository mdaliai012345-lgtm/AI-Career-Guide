import mysql.connector
from ai_explanation import get_ai_advice

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="blackroom",
    database="career_guidance"
)
cursor = db.cursor(dictionary=True)
cursor.execute("SELECT * FROM careers")
careerinfo = cursor.fetchall()


user = input("Enter your name: ").upper()
usered = input("Enter your Education level: ").upper()
if usered == "12TH" or usered == "10TH":
    percentage = float(input("Enter your percentage: "))
if usered == "12TH":
    stream = input("Enter your stream (Science/Commerce/Arts): ").upper()
interest = input("Enter your interest: ").upper()
favsub = input("Enter your favorite subject: ").upper()
skills = input("Enter your skills: ").upper()
prefernces = input("Enter your preferred working environment: ").upper()

   
information = {
    "Name": user ,
    "Education Level": usered ,
    "Percentage": percentage ,
    "Interest": interest ,
    "Favorite Subject": favsub ,
    "Skills": skills ,
    "Preferred Working Environment": prefernces 
}
print(information)

career_score = []

for career in careerinfo:
    score = 0

    if information["Interest"] in career["interest"]:
        score += 1

    if information["Favorite Subject"] in career["subject"]:
        score += 1

    if information["Education Level"] == career["education_level"]:
        score += 1

    if information["Preferred Working Environment"] == career["preferred_working_environment"]:
        score += 1

    if information["Percentage"] >= career["minimum_percentage"]:
        score += 1

    for skill in information["Skills"]:
        if skill in career["skills"]:
            score += 1
    career_score.append((career, score))
career_score.sort(key=lambda x: x[1], reverse=True)
print("\n==== Top 3 Career Matches ====\n")
for i, (career, score) in enumerate(career_score[:3], start=1):
    print(f"{i}. {career['career']} (Score: {score})")

    your_interest = career["interest"]
    skills_ = career["skills"]
    sub = career["subject"]
    ed = career["education_level"]
    st = career["stream"]
    mark = career["minimum_percentage"]
    work = career["preferred_working_environment"]
    des = career["description"]
    edu = career["after_12th_degree"]
       

   
    print("Description:", des)
    print("Your Interest:", your_interest)
    print("Skills you need to develop:", skills_)
    print("Subjects you need to focus on:", sub)
    print("Education Level Required:", ed)
    print("Education Level after 12th:",edu)
    print("Entrance Exams Required:", career["entrance_exams"])
    print("Stream Required:", st)
    print("Minimum Percentage Required:", mark)
    print("Preferred Working Environment:", work)
    print("\n-----------------------------\n")
    print("")

with open("career_report.txt", "w") as file:
    file.write("===== USER INFORMATION =====\n")
    file.write(f"Name: {information['Name']}\n")
    file.write(f"Education Level: {information['Education Level']}\n")
    file.write(f"Percentage: {information['Percentage']}\n")
    file.write(f"Interest: {information['Interest']}\n")
    file.write(f"Favorite Subject: {information['Favorite Subject']}\n")
    file.write(f"Skills: {information['Skills']}\n")
    file.write(f"Preferred Working Environment: {information['Preferred Working Environment']}\n")
    file.write("")
    file.write(f"\n==== Top 3 Career Matches ====\n")
    for i, (career, score) in enumerate(career_score[:3], start=1):
        file.write(f"{i}. {career['career']} (Score: {score})\n")
        file.write(f"Description: {career['description']}\n")
        file.write(f"Your Interest: {career['interest']}\n")
        file.write(f"Skills you need to develop: {career['skills']}\n")
        file.write(f"Subjects you need to focus on: {career['subject']}\n")
        file.write(f"Education Level Required: {career['education_level']}\n")
        file.write(f"Education Level after 12th: {career['after_12th_degree']}\n")
        file.write(f"Entrance Exams Required: {career['entrance_exams']}\n")
        file.write(f"Stream Required: {career['stream']}\n")
        file.write(f"Minimum Percentage Required: {career['minimum_percentage']}\n")
        file.write(f"Preferred Working Environment: {career['preferred_working_environment']}\n")
        file.write("\n-----------------------------\n")
file.close()
best_career = career_score[0][0]
print("\n===== AI Career Advice =====")
advice = get_ai_advice(best_career["career"])
print(advice)