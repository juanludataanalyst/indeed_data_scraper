import json
import re


# JSON de ejemplo (reemplázalo con tu archivo)
data = [
    {
        
         "title": "Business Analysis Trainee, DCS IT - Spring 2025",
        "company": "Sony Pictures Entertainment, Inc.\nCulver City, CA",
        "description": "Our Emerging Talent Programs, which includes Interns, Trainees, and Finance Rotational Associates, offer unique opportunities for students, recent graduates, and emerging talent to work alongside the teams that come together to create movies, TV shows, and other great experiences. These seasonal, paid assignments provide meaningful and productive work that allows you to build on your experience and develop your skills further. You will be provided with challenging tasks, real-world experience, and many educational and social networking opportunities.\n\nThis Spring Trainee position is from January through May 30th (start and end dates are flexible based on your schedule)and all candidates must be able to work 40 hours a week, Monday through Friday in the specified location. This type of opportunity will jump-start your career and prepare you for a career in the desired field. This is not a remote role. A hybrid work option may or may not be available.\nDEPARTMENT DESCRIPTION:\nDistribution & Content Services (DCS) IT provides business process analysis, project-based application, process & reporting enhancements, and break-fix application support. Our development team is comprised of both on and offshore resources.\nDCS manages SPE’s library and distribution operations for all of Sony Pictures Entertainment’s business lines, including theatrical, home entertainment (streaming & physical), broadcast and cable. The division provides services related to the preservation and restoration of assets, mastering and foreign language creation, content manipulation, and file and tape-based delivery to worldwide clients.\n\nRESPONSIBILITIES:\nResponsibilities may include, but are not limited to the following:\nSupporting managers, business analysts, developers, and testers as they define, test & deploy functionality for existing & new systems\nGathering functional requirements and writing user stories with business customers\nCreating & maintaining documentation for new & existing functions, processes, and workflows\nAssisting with data analysis and data cleanup projects which result in meaningful business metrics and efficiencies\nAssisting with defining test cases, staging test data, and executing tests for application & reporting enhancements\nDesigning reports and dashboards to visualize important trends for management\nDesigning wireframes based on business requirements\nQUALIFICATIONS:\nAbility to work 40 hours a week\nAptitude towards learning quickly and having a proactive mindset towards developing solutions and process improvements\nEnthusiasm towards media and entertainment industry\nStrong service orientation and focus; good verbal and written communication skills\nAbility to analyze and define solutions for complex business needs and translate into functional specs\nKnowledge of Microsoft Office (Outlook, Word, Excel, etc.)\nPREFERRED QUALIFICATIONS:\nRelevant experience within this field\nExperience creating business / technical requirement documents\nExperience defining and executing test scripts\nExperience with at least one reporting/visualization tool\nThe anticipated base salary for this position is $27/hour. This role may also qualify for comprehensive benefits. The actual base salary offered will depend on a variety of factors, including without limitation, the qualifications of the individual applicant for the position, years of relevant experience, level of education attained, certifications or other professional licenses held, and if applicable, the location of the position.\nSony Pictures Entertainment is an equal opportunity employer. We evaluate qualified applicants without regard to race, color, religion, sex, national origin, disability, veteran status, age, sexual orientation, gender identity, or other protected characteristics.\nSPE will consider qualified applicants with arrest or conviction records in accordance with applicable law.\nTo request an accommodation for purposes of participating in the hiring process, you may contact us at SPE_Accommodation_Assistance@spe.sony.com.",
        "salary": "$27 por hora",
        "employment_type": "Tipo de empleo\nFull-time"
    }
]

# Diccionario con tecnologías
skills = {
    'sql' : 'SQL', 'python' : 'Python', 'r' : 'R', 'c':'C', 'c#':'C#', 'javascript' : 'JavaScript', 'js':'JS', 'java':'Java', 
    'scala':'Scala', 'sas' : 'SAS', 'matlab': 'MATLAB', 'c++' : 'C++', 'c/c++' : 'C / C++', 'perl' : 'Perl',
    'typescript' : 'TypeScript','bash':'Bash','html' : 'HTML','css' : 'CSS','php' : 'PHP','powershell' : 'Powershell',
    'rust' : 'Rust', 'kotlin' : 'Kotlin','ruby' : 'Ruby','dart' : 'Dart','assembly' :'Assembly',
    'swift' : 'Swift','vba' : 'VBA','lua' : 'Lua','groovy' : 'Groovy','delphi' : 'Delphi','objective-c' : 'Objective-C',
    'haskell' : 'Haskell','elixir' : 'Elixir','julia' : 'Julia','clojure': 'Clojure','solidity' : 'Solidity',
    'lisp' : 'Lisp','f#':'F#','fortran' : 'Fortran','erlang' : 'Erlang','apl' : 'APL','cobol' : 'COBOL',
    'ocaml': 'OCaml','crystal':'Crystal','javascript/typescript' : 'JavaScript / TypeScript','golang':'Golang',
    'nosql': 'NoSQL', 'mongodb' : 'MongoDB','t-sql' :'Transact-SQL', 'no-sql' : 'No-SQL','visual_basic' : 'Visual Basic',
    'pascal':'Pascal', 'mongo' : 'Mongo', 'pl/sql' : 'PL/SQL','sass' :'Sass', 'vb.net' : 'VB.NET','mssql' : 'MSSQL',
    'airflow': 'Airflow', 'alteryx': 'Alteryx', 'asp.net': 'ASP.NET', 'atlassian': 'Atlassian', 
    'excel': 'Excel', 'power_bi': 'Power BI', 'tableau': 'Tableau', 'srss': 'SRSS', 'word': 'Word', 
    'unix': 'Unix', 'vue': 'Vue', 'jquery': 'jQuery', 'linux/unix': 'Linux / Unix', 'seaborn': 'Seaborn', 
    'microstrategy': 'MicroStrategy', 'spss': 'SPSS', 'visio': 'Visio', 'gdpr': 'GDPR', 'ssrs': 'SSRS', 
    'spreadsheet': 'Spreadsheet', 'aws': 'AWS', 'hadoop': 'Hadoop', 'ssis': 'SSIS', 'linux': 'Linux', 
    'sap': 'SAP', 'powerpoint': 'PowerPoint', 'sharepoint': 'SharePoint', 'redshift': 'Redshift', 
    'snowflake': 'Snowflake', 'qlik': 'Qlik', 'cognos': 'Cognos', 'pandas': 'Pandas', 'spark': 'Spark', 'outlook': 'Outlook',
}

# Compilar expresiones regulares para cada tecnología
patterns = {key: re.compile(r'\b' + re.escape(key) + r'\b', re.IGNORECASE) for key in skills}

# Extraer tecnologías
def extract_technologies(description):
    found_technologies = []
    for key, pattern in patterns.items():
        if pattern.search(description):
            found_technologies.append(skills[key])
    return found_technologies


# Procesar cada puesto en el JSON
for job in data:
    description = job.get("description", "")
    technologies = extract_technologies(description)
    print(f"Tecnologías para '{job['title']}': {technologies}")