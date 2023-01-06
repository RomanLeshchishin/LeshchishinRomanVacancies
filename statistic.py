import csv
import datetime as DT
import re
currency_to_rub = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}
class Salary:
    def __init__(self, salary_from, salary_to, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.salary_ru = int((float(self.salary_from) + float(self.salary_to)) / 2) * currency_to_rub[self.salary_currency]
    def getSalaryRu(self):
        return self.salary_ru
class Vacancy:
    def __init__(self, name, salary, area_name, published_at):
        self.name = name
        self.salary = salary
        self.area_name = area_name
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
    def csv_reader(fileName):
        file_csv = csv.reader(open(fileName, encoding='utf_8_sig'))
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
            for i in range(0, len(value)):
                ans = DataSet.clean_string(value[i])
                vacDic[titles[i]] = ans
            vacList.append(Vacancy(vacDic['name'], Salary(vacDic['salary_from'], vacDic['salary_to'], vacDic['salary_currency']), vacDic['area_name'], vacDic['published_at']))
        return vacList
class InputConnect:
    def __init__(self):
        self.params = InputConnect.get_params()
    @staticmethod
    def get_params():
        filename = input('Введите название файла: ')
        vacancy = input('Введите названия профессии: ')
        return filename, vacancy
    @staticmethod
    def convert_data(vacancy):
        return int(DT.datetime.strptime(vacancy.published_at, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y'))
    @staticmethod
    def create_years(vacList, years):
        for vac in vacList:
            years.add(InputConnect.convert_data(vac))
        years = sorted(list(years))
        years = list(range(min(years), max(years) + 1))
        return years
    @staticmethod
    def create_area_dic(vacList, areaDic):
        for vac in vacList:
            if vac.area_name in areaDic:
                areaDic[vac.area_name].append(vac.salary.getSalaryRu())
            else:
                areaDic[vac.area_name] = [vac.salary.getSalaryRu()]
        return areaDic

    @staticmethod
    def create_vacancies_dic(vacList, vacsDic):
        for vac in vacList:
            if vac.area_name in vacsDic:
                vacsDic[vac.area_name] += 1
            else:
                vacsDic[vac.area_name] = 1
        return vacsDic

    @staticmethod
    def printing_statistical_data(vacList, vacancyNames):
        years = set()
        years = InputConnect.create_years(vacList, years)
        salaryLevelYear = {year: [] for year in years}
        vacYear = {year: 0 for year in years}
        vacSalaryLevelYear = {year: [] for year in years}
        vacCountsYear = {year: 0 for year in years}
        for vac in vacList:
            year = int(InputConnect.convert_data(vac))
            salaryLevelYear[year].append(vac.salary.getSalaryRu())
            vacYear[year] += 1
            for vacancyName in vacancyNames.split(', '):
                if vacancyName in vac.name:
                    vacSalaryLevelYear[year].append(vac.salary.getSalaryRu())
                    vacCountsYear[year] += 1
        salaryLevelYear = {key: int(sum(value)/ len(value)) if len(value) != 0 else 0 for key, value in salaryLevelYear.items()}
        vacSalaryLevelYear = {key: int(sum(value)/ len(value)) if len(value) != 0 else 0 for key, value in vacSalaryLevelYear.items()}
        areaNameDic = {}
        areaNameDic = InputConnect.create_area_dic(vacList, areaNameDic)
        areaNameList = areaNameDic.items()
        areaNameList = [x for x in areaNameList if len(x[1]) / len(vacList) > 0.01]
        areaNameList = sorted(areaNameList, key=lambda item: sum(item[1]) / len(item[1]), reverse=True)
        salaryCities = \
            {item[0]: int(sum(item[1]) / len(item[1])) for item in areaNameList[0: min(len(areaNameList), 10)]}
        vacanciesDic = {}
        vacanciesDic = InputConnect.create_vacancies_dic(vacList, vacanciesDic)
        vacanciesCounts = {x: round(y / len(vacList), 4) for x, y in vacanciesDic.items()}
        vacanciesCounts = {k: val for k, val in vacanciesCounts.items() if val >= 0.01}
        vacanciesCities = dict(sorted(vacanciesCounts.items(), key=lambda item: item[1], reverse=True))
        vacanciesCities = dict(list(vacanciesCities.items())[:10])
        print('Динамика уровня зарплат по годам:', salaryLevelYear)
        print('Динамика количества вакансий по годам:', vacYear)
        print('Динамика уровня зарплат по годам для выбранной профессии:', vacSalaryLevelYear)
        print('Динамика количества вакансий по годам для выбранной профессии:', vacCountsYear)
        print('Уровень зарплат по городам (в порядке убывания):', salaryCities)
        print('Доля вакансий по городам (в порядке убывания):', vacanciesCities)
        return salaryLevelYear, vacYear, vacSalaryLevelYear, vacCountsYear, salaryCities, vacanciesCities
pars = InputConnect()
if pars.params is not None:
    data = DataSet(pars.params[0])
    pars.printing_statistical_data(data.vacancies_objects, pars.params[1])
