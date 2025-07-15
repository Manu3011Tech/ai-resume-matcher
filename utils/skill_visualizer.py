import matplotlib.pyplot as plt
import os

def generate_skill_pie_chart(matched_skills, jd_keywords, save_path="assets/skill_chart.png"):
    matched = len(matched_skills)
    total = len(jd_keywords)
    missing = total - matched if total > matched else 0

    labels = ['Matched Skills', 'Missing Skills']
    sizes = [matched, missing]
    colors = ["#6BA7C9", "#631554"]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    ax.axis('equal')
    plt.tight_layout()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()

    return save_path
