import pandas as pd
import glob

# This will calculate the participation grades for each student in the Canvas gradebook.  
# Here are steps to use it:
#  1.  Download the full Canvas gradebook.  Modify it by removing the blank line and "points possible line" 
#      and re-save as "from_canvas.csv"
#  2.  Download your roster from MyOntarioTech (we need the email addresses from it).  Edit the name below 
#      to match what your file is saved as 
#  3.  Change the "assessment_name" variable to match your assignment name in Canvas
#  4.  Run!

# We need a Canvas file for a list of students
dfc = pd.read_csv("from_canvas.csv")

# delete the students who are not in my sections
dfc = dfc[~dfc.Section.str.contains('PHY-1010U-003')]
dfc = dfc[~dfc.Section.str.contains('PHY-1010U-004')] 

# rename student ID column
dfc = dfc.rename(columns = {'SIS Login ID': 'Student ID'})
 
# new!  Now we have to add the students' email address
dfe = pd.read_csv("roster_all_my_sections.csv")

# now need to merge the emails into the dfc
dfc = pd.merge(dfc, dfe[['Student ID', 'Email']], on='Student ID', how='left')

# this is the name of the assignment on Canvas that will hold the participation grades
assessment_name = 'Participation - Section 1, 2, and 48 (Dr. MacMillan) (206149)'

# now get a list of all excel files in this directory
all_files = glob.glob('*.xlsx')
# read each of the files into pandas dataframes
sheets_list = []
for f in all_files:
	sheets_list.append(pd.read_excel(f, sheet_name='Voters', skiprows = 2))

# now loop over all students in the canvas file and count if they were participating in each topic
for i in range(0, len(dfc)):
	student = dfc.loc[i]
	
	count = 0
	grade = 0
	for sheet in sheets_list:
		# this column is what I called the mentimeter poll that asks for student numbers
		if (sheet["Email"] == student["Email"]).any():
			count += 1
	
	# let the students have three missed lectures (there are 12 topics with data)
	grade = min(count/9.0 * 5.0, 5.0)
	print(f"{student['Student']}({student['Student ID']}) attended {count} lectures for a grade of {grade}")
	dfc.loc[i, assessment_name] = grade
	
# keep only the columns we really need to upload to Canvas
dfc = dfc[['Student', 'ID', 'Student ID', 'Section', assessment_name]]
			
# save file as csv
dfc = dfc.rename(columns = {'Student ID' : 'SIS Login ID'})
dfc.to_csv('out.csv', index=False)
