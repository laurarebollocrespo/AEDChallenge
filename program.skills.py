def sort_skills(p1: Participant):
    # Initialize categories
    core_tech = []
    dev_platforms = []
    ai_data = []
    design = []
    
    for p in Participants:
        skills = p.programming_skills
        name = p.name
        
        # Sort each skill into appropriate category
        for skill in skills:
            if skill in ['Python', 'python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'Rust', 'Go', 'HTML/CSS', 'SQL', 'Git/GitHub']:
                if [name, skill, skills[skill]] not in core_tech:
                    core_tech.append([name, skill, skills[skill]])
                    
            elif skill in ['React', 'Flutter', 'Flask', 'iOS', 'iOS Development', 'Android', 'android', 'Docker', 'AWS/Azure/GCP', 'PostgreSQL', 'MongoDB', 'Blockchain', 'IoT']:
                if [name, skill, skills[skill]] not in dev_platforms:
                    dev_platforms.append([name, skill, skills[skill]])
                    
            elif skill in ['PyTorch', 'pytorch', 'TensorFlow', 'Machine Learning', 'Computer Vision', 'NLP', 'Data Analysis', 'Data Visualization']:
                if [name, skill, skills[skill]] not in ai_data:
                    ai_data.append([name, skill, skills[skill]])
                    
            elif skill in ['Figma', 'UI/UX', 'UI/UX Design', 'Design', 'Agile', 'Agile Methodology']:
                if [name, skill, skills[skill]] not in design:
                    design.append([name, skill, skills[skill]])
    