# Description: Calculates statistics and a makes pivot table for the citation analysis in the article, "The
# International Criminal Court and the Justice Cascade," using citation data taken from States of Justice.
#
# Author: Barry Hashimoto
# Date: July 25, 2023

# Libraries
import os
import re
import sys
import pandas as pd

# Function for separating information printed to the terminal with a long line.
def makelines(file = None):
    N = 100
    if file is None:
        print('-' * N + '\n')
    else:
        print('-' * N + '\n', file = file)

# Initialize a list to hold aggregate citation data.
data = []

# Function to calculate aggregate statistics from text files containing citation data for chapters.
def citestats(path, title):

    # Declare the `data` object as a global object.
    global data

    # Check validity of arguments.
    if any([
        not isinstance(path, str), 
        not isinstance(title, str), 
        '.txt' not in path
        ]):
        print('\nError: Invalid arguments were supplied. Nothing printed for this chapter.\n')
        return

    # Print a title to the terminal indicating the chapter being described.
    print(title)

    # Open the file and create tables.
    with open(path, 'r') as file:

        # Read in the text file of source citations for a particular chapter of the book.
        file_contents = file.read()

        # Make a list of all the citation entries, which should be one per line.
        entries = file_contents.splitlines()

        # Make a list of the unique citation entries.
        unique_entries = set(entries)

        # Save the number of unique sources cited.
        number_sources = len(unique_entries)

        # Make and print a sorted table of unique entries with citation counts.
        print('\n1. Sources and citation counts:\n')
        for entry in sorted(unique_entries, key = lambda x: entries.count(x), reverse = True):
            count = entries.count(entry)
            print(entry, count)

        # Replace existing labels in the citation entries with generic category labels.
        for i in range(len(entries)):

            # Author's field interviews
            if 'interview' in entries[i]: entries[i] = "source: Author's field interviews"

            # Memoirs and biographies
            if 'biography' in entries[i]: entries[i] = "source: Biographies"

            # State acts and documents
            state_docs = ['government document', 'government file', 'state document', 'state file']
            if any(item in entries[i] for item in state_docs):
                entries[i] = 'source: State acts and documents'

            # Materials from the ICC that not formally part of ICC legal proceedings
            icc_other_materials = ['ICC press release', 'ICC web page', 'ICC speech', 
                                     'ICC Agreed Minutes', 'ICC OTP Statement', 'ICC Diplomatic Briefing']
            if any(item in entries[i] for item in icc_other_materials):
                entries[i] = 'source: ICC statements'

            # Materials formally part of ICC legal proceedings
            icc_case_materials = ['ICC Transcript', 'ICC Pre-Trial Chamber', 'ICC Trial Chamber', 
                                  'ICC Appeals Chamber', 'ICC defense counsel document']
            if any(item in entries[i] for item in icc_case_materials):
                entries[i] = 'source: ICC case law'

            # Rome Statute of the ICC
            if 'Rome Statute' in entries[i]: entries[i] = 'source: Rome Statute'

            # Documents of other international organizations
            internationalorgs = ['ICJ', 'OHCHR', "African Union", "UNSC", 'Secretary-General',
                'UN News', 'ECHR', 'EU EOM']
            if any(item in entries[i] for item in internationalorgs):
                entries[i] = 'source: International organization documents'
            
            # Newspapers and magazines articles
            newspapers = ['New Humanitarian', 'New Vision', 'Sudan Tribune', 'Reuters', 
                'Associated Press', 'NPR', 'Jollof News', 'Aljazeera', 'Guardian', 'AFP', 
                'France 24', 'Fraternite Matin', 'Foreign Policy', 'Kenya Today', 'LA Times',
                'New York Times', 'BBC', 'Liberation', 'Time Magazine', 'Washington Post']
            if any(newspaper in entries[i] for newspaper in newspapers):
                entries[i] = 'source: Newspaper and magazine articles'
            
            # NGO publications
            ngos = ['NGO', 'Human Rights Watch', 'HRW', 'Amnesty International', 'Crisis Group', 
                'FIDH', 'CSIS', 'Carter Center', 'ICTJ', 'IJM', 'IHEJ', "Chatham House",
                'Polity IV', 'The New Visions', 'Kenya Human Rights Commission',
                'African Arguments', 'ISITA', 'ACSSS', "ISS Today", 'Freedom House']
            if any(ngo in entries[i] for ngo in ngos):
                entries[i] = 'source: NGO publications'

            # Blogs
            if 'blog' in entries[i]: entries[i] = 'source: Blog posts'
            if 'Blog' in entries[i]: entries[i] = 'source: Blog posts'

            # Peer-reviewed secondary sources
            if 'source' not in entries[i]:
                entries[i] = 'Peer-reviewed articles and books'

            # Now that `source: ` has served its role as a way to identify secondary sources, erase it.
            if 'source: ' in entries[i]:
                entries[i] = entries[i].replace("source: ", "")

        # Make a sorted table of unique entries with citation counts.
        print('\n2. Citation counts to primary and secondary sources, by category:\n')
        unique_entries = set(entries)
        for entry in sorted(unique_entries, key = lambda x: entries.count(x), reverse = True):
            count = entries.count(entry)
            print(entry, count)

        # Print summary data to enable quick calculations by hand.
        print('\nTotal number of citations', len(entries))
        print('Number of unique sources cited', number_sources)

        # Print a divider line to mark the end of this section.
        makelines()

        # Append chapter-specific aggregate citation statistics as dictionaries in the global list, `data`.
        for entry in unique_entries:
            count = entries.count(entry)
            data.append({'chapter': title, 'entry': entry, 'count': count})

# Run citestats() for text files containing the citations of a series of chapters, saving to file.

# Set relative paths for the directory (where output files will go) and data subdirectory.
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, 'data')

# Name the output file where citation statistics will be printed, and remove it if existent, since we append below.
filename = 'output_all_citation_statistics.txt'
output_path = os.path.join(dir_path, filename)
if os.path.exists(output_path):
    os.remove(output_path)

# Make and save citation statistics in "append" mode to a new file.
with open(output_path, "a") as f:

    # Set system's output to file.
    sys.stdout = f

    # Specify file names and section titles.
    chapters = [('chapter_three_citations.txt', 'Chapter 3:'),
                ('chapter_four_citations.txt', 'Chapter 4:'),
                ('chapter_five_citations.txt', 'Chapter 5:'),
                ('chapter_six_citations.txt', 'Chapter 6:'),
                ('chapter_seven_citations.txt', 'Chapter 7:')]

    # Run the custom citestats() function for each file.            
    for chapter in chapters:
        citestats(os.path.join(data_path, chapter[0]), chapter[1])

    # Return to system's standard out.    
    sys.stdout = sys.__stdout__

# Make a Dataframe with a pivot table of aggregate statistics saved to the `data` list of dictionaries.
df = pd.DataFrame(data)
table = df.pivot_table(values = 'count', index = 'entry', columns = 'chapter', aggfunc = 'sum', 
    margins = True, margins_name = "Total")

# Sort the table by the `Total` column.
table = table.sort_values('Total', ascending = True)

# Replace cells with missing values with 0 and convert cell types to integers for pretty printing.
table = table.fillna(0).round().astype(int)

# Stop 'entry' and 'chapter' from appearing as labels of the two table axes.
table = table.rename_axis(None, axis = 1).rename_axis(None, axis = 0)

# Re-open the file of results and add the aggregate table at the top, casting as string for wide printing.
with open(output_path, "r+") as f:
    content = f.read()
    f.seek(0)
    print('Aggregate citation count statistics, by chapter\n', file = f)
    print(table.to_string(max_rows = None), file = f)
    makelines(file = f)
    print(content, file = f)

# Save a table of the results as a .tex file.
tex_table_name = 'output_pivot_table.tex'
with open(os.path.join(dir_path, tex_table_name), 'w') as f:
    f.write(table.style.to_latex())
