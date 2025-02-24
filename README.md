# Timetable Scheduler

## Overview
This project is a **Timetable Scheduling System** for a **BTech program**, designed to generate optimized schedules for students and faculty using **Constraint Programming (CP) and Local Search (LS)** techniques. The algorithm ensures that hard constraints are strictly followed while optimizing soft constraints for efficiency.

## Features
- Uses **Constraint Programming (CP)** for hard constraints.
- Implements **Local Search (Simulated Annealing)** for optimization.
- Prioritizes morning slots before afternoon slots.
- Supports both **Theory and Lab** periods.
- Enforces **Minor & Elective courses** to be scheduled at fixed times.
- Ensures **no consecutive Theory classes**.
- Prevents **overlapping faculty schedules**.
- **MySQL Database Integration** for storing course and schedule data.

## Technologies Used
- **Python** (for the scheduling algorithm)
- **OR-Tools** (Google’s Optimization Tools for CP and LS)
- **MySQL** (for backend database storage)
- **HTML/CSS/JavaScript** (for the simple frontend interface)


## Constraints Implemented
### **Hard Constraints (Must be Followed)**
✅ Each course must be scheduled for the required hours.
✅ No overlapping classes for the same faculty.
✅ Lab sessions are exactly one 2-hour continuous block per week.
✅ Minor courses occur only on **Tuesdays & Thursdays (2:10-4:10 PM)**.
✅ Elective courses occur only on **Wednesdays (2:10-4:10 PM)**.
✅ The last class of the day is at **4:10 PM** (No 5:10 PM slot).
✅ No consecutive theory periods.

### **Soft Constraints (Optimized for Better Scheduling)**
🔹 Fill morning slots first before afternoon slots.
🔹 Minimize the total length of each day for students.
🔹 Ensure students don’t have only **one period on any day**.
🔹 Distribute faculty workload evenly across the week.

## Future Improvements
- Implement a **web dashboard** for easy timetable visualization.
- Add **faculty preference-based scheduling**.
- Enhance the Local Search optimization for better scheduling efficiency.

## Contributors
- **VISHVESH K SHRIVATSAV** - Developer & Maintainer
