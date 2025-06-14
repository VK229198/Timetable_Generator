import random
import copy
import pymysql

# ------------------------------
# CONSTANTS FROM DATABASE
# ------------------------------

con=pymysql.connect(host='localhost',user='root',password='Vishks31$',database='timetable')
cur=con.cursor()

#-----------------------
#SECTIONS FROM DATASABE
#------------------------

SECTIONS_BY_SEM={}
l2=[]
l4=[]
cur.execute("select*from sections;")
rows=cur.fetchall()
for i in range(len(rows)):
    if rows[i][1]=='Sem2':
        l2.append(rows[i][0])
    elif rows[i][1]=='Sem4':
        l4.append(rows[i][0])
SECTIONS_BY_SEM.update({'Sem2':l2,'Sem4':l4})

SECTIONS = SECTIONS_BY_SEM['Sem2'] + SECTIONS_BY_SEM['Sem4']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
PERIODS_PER_DAY = 7

#-------------------------------------------------------------------
# RULES TO CHEK WHETER OR NOT A SEMESTER HAS MINORS AND ELECTIVES
#---------------------------------------------------------------------

SEMESTER_RULES = {
    'Sem4': {
        'has_minor': True,
        'has_elective': True,
        'has_pelective': False
    },
    'Sem2': {
        'has_minor': False,
        'has_elective': False,
        'has_pelective': False
    },
    'Sem6': {
        'has_minor': False,
        'has_elective': False,
        'has_pelective': True
    }
}


# ----------------------------------
# FACULTY ASSIGNMENTS FROM DATABASE
# ----------------------------------

FACULTY_ASSIGNMENTS={}
cur.execute("select*from faculty_course_assignments;")
row=cur.fetchall()
for course,faculty,section in row:
    FACULTY_ASSIGNMENTS.setdefault(course, {}).setdefault(faculty, []).append(section)

#-------------------------------------
# COURSE ASSIGNMENTS FROM DATABASEEE<3
#-------------------------------------


cur.execute("select*from courses;")
rows=cur.fetchall()
COURSES={}
d2={}
d4={}
LAB_COURSES=[]

for i in range(len(rows)):
    if rows[i][4]=='Sem4':
        d4.update({rows[i][1]:{'hours_per_week':rows[i][2]}})
        if rows[i][3]==1:
            LAB_COURSES.append(rows[i][1])
    elif rows[i][4]=='Sem2':
        d2.update({rows[i][1]:{'hours_per_week':rows[i][2]}})
        if rows[i][3]==1:
            LAB_COURSES.append(rows[i][1])
COURSES.update({"Sem4":d4,"Sem2":d2})


#-----------------------
# CODE PART
#-----------------------

def create_empty_timetable():
    timetable = {}
    for section in SECTIONS:
        timetable[section] = {}
        for day in DAYS:
            timetable[section][day] = [None for _ in range(PERIODS_PER_DAY)]
    return timetable


def get_faculty_for_section(course, section):
    for faculty, sec_list in FACULTY_ASSIGNMENTS.get(course, {}).items():
        if section in sec_list:
            return faculty
    return None


def is_faculty_free(timetable, faculty, day, period):
    for sec in SECTIONS:
        for course, f in FACULTY_ASSIGNMENTS.items():
            for fac, fac_secs in f.items():
                if fac == faculty and sec in fac_secs:
                    if timetable[sec][day][period] is not None and faculty in timetable[sec][day][period]:
                        return False
    return True


def are_periods_free(periods_list, start_index, duration):
    return start_index + duration <= len(periods_list) and all(periods_list[start_index + i] is None for i in range(duration))


def fill_timetable_correctly(timetable):
    for section in SECTIONS:
        semester = 'Sem4' if section in SECTIONS_BY_SEM['Sem4'] else 'Sem2' if section in SECTIONS_BY_SEM['Sem2'] else 'Sem6'
        rules = SEMESTER_RULES.get(semester, {})
        course_hours_left = copy.deepcopy(COURSES[semester])

        if rules.get('has_minor'):
            for day in ['Tuesday', 'Thursday']:
                for p in [4, 5, 6]:
                    timetable[section][day][p] = 'Minor'

        if rules.get('has_elective'):
            for p in [4, 5, 6]:
                timetable[section]['Wednesday'][p] = 'Elective'

        if rules.get('has_pelective'):
          
            for day in ['Monday', 'Tuesday']:
                for p in [0, 1]:
                    timetable[section][day][p] = 'Professional Elective 04'
            for p in [2, 3]:
                timetable[section]['Wednesday'][p] = 'Professional Elective 03'
            for p in [0, 1]:
                timetable[section]['Friday'][p] = 'Professional Elective 03'

        for lab in LAB_COURSES:
            if lab not in course_hours_left:
                continue
            lab_hours = course_hours_left[lab]['hours_per_week']
            faculty = get_faculty_for_section(lab, section)
            attempts = 0

            while lab_hours > 0 and attempts < 200:
                day = random.choice(DAYS)
                periods = timetable[section][day]

                possible_starts = list(range(0, 5 - 1) if attempts < 100 else range(PERIODS_PER_DAY - 1))
                random.shuffle(possible_starts)

                for start in possible_starts:
                    if are_periods_free(periods, start, 2) and \
                       is_faculty_free(timetable, faculty, day, start) and \
                       is_faculty_free(timetable, faculty, day, start + 1):
                        periods[start] = f"{lab} ({faculty})"
                        periods[start + 1] = f"{lab} ({faculty})"
                        lab_hours -= 2
                        break
                attempts += 1

            if lab_hours > 0:
                print(f"Warning: Could not schedule all lab hours for {lab} in section {section}")

        for course, data in course_hours_left.items():
            if course in LAB_COURSES:
                continue
            hours_needed = data['hours_per_week']
            faculty = get_faculty_for_section(course, section)
            attempts = 0

            while hours_needed > 0 and attempts < 200:
                day = random.choice(DAYS)
                candidate_periods = list(range(5) if attempts < 100 else range(PERIODS_PER_DAY))
                random.shuffle(candidate_periods)

                for period_idx in candidate_periods:
                    if timetable[section][day][period_idx] is not None:
                        continue
                    if not is_faculty_free(timetable, faculty, day, period_idx):
                        continue

                    timetable[section][day][period_idx] = f"{course} ({faculty})"
                    hours_needed -= 1
                    break

                attempts += 1

            if hours_needed > 0:
                print(f"Warning: Could not schedule all theory hours for {course} in section {section}")

    return timetable


def print_nice_timetable(timetable):
    
    col_width = 22
    lunch_after_period = 3 
    for section, schedule in timetable.items():
        print(f"\nSection {section} Timetable:")
        header = "+-----------+"
        for i in range(PERIODS_PER_DAY):
            header += "-" * col_width + "+"
            if i == lunch_after_period:
                header += "-" * 11 + "+"
        titles = "| Day       |"
        for i in range(PERIODS_PER_DAY):
            titles += f" Period {i+1:<{col_width - 9}}" + "|"
            if i == lunch_after_period:
                titles += " Lunch   |"
        print(header)
        print(titles)
        print(header)
        for day in DAYS:
            row = f"| {day:<9} |"
            for i, period in enumerate(schedule[day]):
                cell = period if period is not None else "Free"
                cell_str = "/".join(cell.split('\n')) if isinstance(cell, str) else str(cell)
                row += f" {cell_str:<{col_width - 1}}|"
                if i == lunch_after_period:
                    row += "  LUNCH   |"
            print(row)
        print(header)




# ------------------------------
# RUN AND DISPLAY PART
# ------------------------------

if __name__ == '__main__':
    timetable = create_empty_timetable()
    filled_timetable = fill_timetable_correctly(timetable)
    print_nice_timetable(filled_timetable)
