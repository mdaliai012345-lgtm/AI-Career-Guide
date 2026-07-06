from career_database import careerinfo
from ai_explanation import get_ai_advice

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

    if information["Interest"] in career["Interest"]:
        score += 1

    if information["Favorite Subject"] in career["Subject"]:
        score += 1

    if information["Education Level"] == career["Education Level"]:
        score += 1

    if information["Preferred Working Environment"] == career["Preferred Working Environment"]:
        score += 1

    if information["Percentage"] >= career["MINIMUM PERCENTAGE"]:
        score += 1

    for skill in information["Skills"]:
        if skill in career["SKILLS"]:
            score += 1
    career_score.append((career, score))
career_score.sort(key=lambda x: x[1], reverse=True)
print("\n==== Top 3 Career Matches ====\n")
for i, (career, score) in enumerate(career_score[:3], start=1):
    print(f"{i}. {career['CAREER']} (Score: {score})")

    your_interest = career["Interest"]
    skills_ = career["SKILLS"]
    sub = career["Subject"]
    ed = career["Education Level"]
    st = career["STREAM"]
    mark = career["MINIMUM PERCENTAGE"]
    work = career["Preferred Working Environment"]
    des = career["DESCRIPTION"]
    edu = career["AFTER 12TH DEGREE"]
       

   
    print("Description:", des)
    print("Your Interest:", your_interest)
    print("Skills you need to develop:", skills_)
    print("Subjects you need to focus on:", sub)
    print("Education Level Required:", ed)
    print("Education Level after 12th:",edu)
    print("Entrance Exams Required:", career["ENTRANCE EXAMS"])
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
        file.write(f"{i}. {career['CAREER']} (Score: {score})\n")
        file.write(f"Description: {career['DESCRIPTION']}\n")
        file.write(f"Your Interest: {career['Interest']}\n")
        file.write(f"Skills you need to develop: {career['SKILLS']}\n")
        file.write(f"Subjects you need to focus on: {career['Subject']}\n")
        file.write(f"Education Level Required: {career['Education Level']}\n")
        file.write(f"Education Level after 12th: {career['AFTER 12TH DEGREE']}\n")
        file.write(f"Entrance Exams Required: {career['ENTRANCE EXAMS']}\n")
        file.write(f"Stream Required: {career['STREAM']}\n")
        file.write(f"Minimum Percentage Required: {career['MINIMUM PERCENTAGE']}\n")
        file.write(f"Preferred Working Environment: {career['Preferred Working Environment']}\n")
        file.write("\n-----------------------------\n")
file.close()
best_career = career_score[0][0]
print("\n===== AI Career Advice =====")
advice = get_ai_advice(best_career["CAREER"])
print(advice)