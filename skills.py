import csv
import datetime as DT
import re
from collections import Counter
class Vacancy:
    def __init__(self, name, key_skills, published_at):
        self.name = name
        self.key_skills = key_skills
        self.published_at = published_at
class DataSet:
    def __init__(self, file_name):
        self.file_name = file_name
        self.vacancies_objects = DataSet.csv_filter(file_name)
    @staticmethod
    def clean_string(text):
        text = re.sub(r'<[^>]*>', '', text).replace('\r\n', ' ').strip()
        return re.sub(' +', ' ', text)
    @staticmethod
    def csv_reader(file_name):
        file_csv = csv.reader(open(file_name, encoding='utf_8_sig'))
        try:
            list_data = [x for x in file_csv]
            titles = list_data[0]
            values = [x for x in list_data[1:] if x.count('') == 0 and len(x) == len(titles)]
            return titles, values
        except:
            print('Пустой файл')
            exit()
    @staticmethod
    def csv_filter(file_name):
        titles, values = DataSet.csv_reader(file_name)
        vacList = []
        for value in values:
            vacDic = {}
            vacValues = []
            for i in range(0, len(value)):
                ans = DataSet.clean_string(value[i])
                if(titles[i] == 'key_skills'):
                    vacValues = ans.split('\n')
                    vacDic[titles[i]] = vacValues
                else:
                    vacDic[titles[i]] = ans
            vacList.append(Vacancy(vacDic['name'], vacDic['key_skills'], vacDic['published_at']))
        return vacList
class InputConnect:
    def __init__(self):
        self.param = InputConnect.get_params()
    @staticmethod
    def get_params():
        filename = 'vacancies_with_skills.csv'
        return filename
    @staticmethod
    def convert_data(vacancy):
        return int(DT.datetime.strptime(vacancy.published_at, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y'))
    @staticmethod
    def create_years(vacList, years):
        for vacancy in vacList:
            years.add(InputConnect.convert_data(vacancy))
        years = sorted(list(years))
        years = list(range(min(years), max(years) + 1))
        return years
    @staticmethod
    def printing_statistical_data(vacList):
        vacancyNames = ['Frontend-программист', 'frontend', 'фронтенд', 'вёрстка', 'верстка', 'верста', 'front end', 'angular', 'html', 'css', 'react', 'vue', 'Frontend']
        years = set()
        years = InputConnect.create_years(vacList, years)
        skillsYear = {year: [] for year in years}
        for vacancy in vacList:
            year = int(InputConnect.convert_data(vacancy))
            for vacName in vacancyNames:
                if (vacName in vacancy.name):
                    for skill in vacancy.key_skills:
                        skillsYear[year].append(skill)
                    break
        print('Навыки по годам:', skillsYear)
        for year in skillsYear.keys():
            c = Counter(skillsYear[year])
            print(year, c.most_common(10))
        skillsAllYears = {}
        for year, value in skillsYear.items():
            for skill in skillsYear[year]:
                if skill not in skillsAllYears.keys():
                    skillsAllYears[skill] = 1
                else:
                    skillsAllYears[skill] += 1
        return skillsYear
pars = InputConnect()
if pars.param is not None:
    data = DataSet(pars.param)
    pars.printing_statistical_data(data.vacancies_objects)
