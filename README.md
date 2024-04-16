# ExcelGuard
## What is ExcelGuard?
This application seeks to tackle the specific issue of plagiarism detection in Excel  files, which is an area where existing software solutions are lacking in. ExcelGuard is a specialized tool capable of accurately scanning and analyzing Excel file submissions for suspicious similarities to maintain academic integrity more effectively.

## What is the point of ExcelGuard?
This application has the potential to automate the detection of suspicious content in submitted spreadsheet documents and empower educators and academic institutions to uphold academic integrity standards more effectively. With the ability to process multiple files rapidly and accurately, our application saves valuable time and resources, enabling educators to focus on providing quality feedback and make informed decisions when assessing their students’ academic integrity.

Furthermore, our application enhances the overall learning experience by promoting a fair and level playing field, where students are recognized and rewarded for original work. By deterring plagiarism and ensuring academic honesty, our system cultivates ethical scholarship within educational institutions. Ultimately, the adoption of our system has the potential to evaluate academic standards, enhance credibility, and foster cultures of excellence in education. By leveraging technology to automate plagiarism detection processes, faculty can focus on what truly matters—nurturing intellectual curiosity, critical thinking skills, and a passion for learning among their students.

## How to set up ExcelGuard locally
1. Download Anaconda Navigator (https://docs.anaconda.com/free/anaconda/install/windows/)
2. Set up a Python environment on Anaconda (only need to do this once)
    - Click the Environments tab
    - Click `Create`
    - Enter a name for your environment
    - Click the `Python` checkbox
    - Make sure 3.11.4 is selected
3. Click on your Python environment
4. Click the `Play` button that pops up and click `Open with Terminal` in the menu that pops up.
5. **Optional**: you can use `cd directory_name` (where `directory_name` is the name of the folder), if you have a specific folder you want to store the project in.
6. After opening the terminal for the Python environment using Anaconda, ensure that `git` is installed by running the following command in the terminal: `conda install -c anaconda git`.
7. Run `git clone https://github.com/Dhruv-Panicker/excel-plagiarism-tool.git`
8. Run `cd excel-plagiarism-tool`
9. Run `env.bat`
10. Run `setup.bat`
11. Visit the URL specified in your terminal after running the command above
<img width="656" alt="download" src="https://github.com/Dhruv-Panicker/excel-plagiarism-tool/assets/57971751/dfafb0cd-bc75-4e44-a11d-abb91cdedc34">

## Acknowledgments
We would like to acknowledge Kyle Maclean as he was a huge help in determining the scope and objectives of the project. He took the time to provide us with high quality datasets to properly test our application with. Additionally, he walked us through and provided feedback on our plagiarism checker algorithm, which really helped in understanding how the core algorithm will be designed. Kyle truly played a pivotal role in helping us define clear requirements and objectives which the application is based on.
