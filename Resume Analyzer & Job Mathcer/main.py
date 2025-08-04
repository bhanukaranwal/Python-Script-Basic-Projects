import re

# Prototype job keyword/interests and sample job listings (expand as needed)
JOB_KEYWORDS = {
    'python': 10,
    'machine learning': 15,
    'data analysis': 12,
    'deep learning': 15,
    'nlp': 14,
    'sql': 10,
    'cloud': 8,
    'aws': 9,
    'java': 7,
    'c++': 7
}

JOB_LISTINGS = [
    {
        'title': 'Data Scientist',
        'keywords': ['python', 'machine learning', 'data analysis', 'sql'],
        'company': 'Tech Innovators'
    },
    {
        'title': 'Cloud Engineer',
        'keywords': ['cloud', 'aws', 'python'],
        'company': 'Cloudify'
    },
    {
        'title': 'Backend Developer',
        'keywords': ['java', 'sql', 'c++'],
        'company': 'CodeCraft'
    }
]

def score_resume(text):
    text = text.lower()
    score = 0
    matched_skills = []
    for skill, points in JOB_KEYWORDS.items():
        if skill in text:
            score += points
            matched_skills.append(skill)
    return score, matched_skills

def find_best_jobs(resume_text):
    scores = []
    for job in JOB_LISTINGS:
        job_score = 0
        for kw in job['keywords']:
            if kw in resume_text.lower():
                job_score += JOB_KEYWORDS.get(kw, 0)
        scores.append((job_score, job))
    scores.sort(reverse=True, key=lambda x: x[0])
    return scores

def resume_analyzer():
    print("\nWelcome to Resume Analyzer & Job Matcher!")
    resume_path = input("Enter path to your resume text file (txt): ")
    if not re.match(r'.+\\.txt$', resume_path):
        print("Currently only supports plain txt files.")
        return
    try:
        with open(resume_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print("Could not read the file:", e)
        return
    score, matched_skills = score_resume(text)
    print(f"\nYour resume matched these skills: {', '.join(matched_skills)}")
    print(f"Your overall skill score: {score}")
    print("\nTop job matches based on your resume:")
    best_jobs = find_best_jobs(text)
    for sc, job in best_jobs[:3]:
        print(f"{job['title']} at {job['company']} - Match Score: {sc}")

if __name__ == '__main__':
    resume_analyzer()
