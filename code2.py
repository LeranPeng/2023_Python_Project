"""
Author: Leran Peng
Student Number: 23909531
Project Name: CITS1401 Project2
"""


class CaseInsensitiveDict(dict):
    """Make the dictionary case-insensitive when it comes to keys."""

    def _normalise_key(self, key):
        return key.lower()

    def __getitem__(self, key):
        # converts the key to lowercase then uses the superclass method to fetch the value associated with that key.
        normalised_key = self._normalise_key(key)
        return super().__getitem__(normalised_key)

    def __setitem__(self, key, value):
        # Setting an item in the dictionary
        normalised_key = self._normalise_key(key)
        super().__setitem__(normalised_key, value)

    def __contains__(self, key):
        # Check if a key exists in the dictionary
        normalised_key = self._normalise_key(key)
        return super().__contains__(normalised_key)


def read_csvfile(file_name):
    """Read file and extract data,considering the extreme condition."""
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            if not lines:  # Check if file is empty
                raise ValueError("The file is empty")

            headers = []
            for header in lines[0].split(','):
                out_header = header.strip().lower().replace(" ", "_")
                headers.append(out_header)
            if len(lines) == 1:
                raise ValueError("The file haven't data")

            data = []
            for line in lines[1:]:  # Starting from the second line
                values = line.strip().split(',')
                if len(values) != len(headers):
                    continue

                row = {}
                for i in range(len(headers)):  # Creating dictionary for each row
                    key = headers[i]
                    value = values[i].lower()
                    row[key] = value
                data.append(row)
            return data
    except FileNotFoundError:
        print("File cannot be found")
        return {}
    except ValueError:
        print("Value Error happened while reading the file")
        return {}
    except IOError:
        print("Error: An error occurred while reading the file.")
        return {}
    except Exception:
        print("Unexpected error happened, cannot be fixed")
        return {}


def t_test(sample1, sample2):
    """T-Test calculation"""

    def var(numbers):  # Calculate variance
        n = len(numbers)
        if n <= 1:
            return 0
        mean = sum(numbers) / n
        variance = sum((num - mean) ** 2 for num in numbers) / (n - 1)
        return variance

    try:
        if len(sample1) < 2 or len(sample2) < 2:  # Check if the sample sizes are less than 2
            raise ValueError("Sample sizes should be at least 2.")

        n1, n2 = len(sample1), len(sample2)  # size of samples
        mean1, mean2 = sum(sample1) / n1, sum(sample2) / n2  # observed mean of samples
        var1, var2 = var(sample1), var(sample2)  # variance of samples
        if var1 == 0 or var2 == 0:
            raise ValueError("Variance of one of the samples is zero.")

        denominator = (var1 / n1 + var2 / n2) ** 0.5
        t = (mean1 - mean2) / denominator
        return round(t, 4)

    except ValueError:
        print("Value Error happened when doing the t-test")
        return {}
    except ZeroDivisionError:
        print("T-test calculate failure duo to Zero Division Error")
        return {}


def Minkowski_distance(x, y, p=3):  # Calculate the Minkowski distance between two lists
    try:
        if len(x) != len(y):
            raise ValueError("Input lists x and y must have the same length.")
        total = 0
        for a, b in zip(x, y):
            total += abs(a - b) ** p
        distance = total ** (1 / p)
        return round(distance, 4)

    except ValueError:
        print("Value Error happened when calculating Minkowski Distance")
        return {}
    except ZeroDivisionError:
        return {}


def output_country(data):
    if not data:  # Empty data check
        return {}

    divided_by_country = {}
    for row in data:
        country = row['country']
        if country not in divided_by_country:  # Initialise Country Data
            divided_by_country[country] = {
                'profits_for_2020': [], 'profits_for_2021': [], 'employees': [], 'salaries': []
            }
        try:  # Extract and convert data values
            employees = int(row['number_of_employees'])
            salary = float(row['median_salary'])
            profit_2020 = float(row['profits_in_2020(million)'])
            profit_2021 = float(row['profits_in_2021(million)'])
            if employees <= 0 or salary <= 0:
                continue
        except ValueError:
            continue
        """Storing data by country"""
        divided_by_country[country]['profits_for_2020'].append(profit_2020)
        divided_by_country[country]['profits_for_2021'].append(profit_2021)
        divided_by_country[country]['employees'].append(employees)
        divided_by_country[country]['salaries'].append(salary)

    output = {}
    for country, values in divided_by_country.items():
        t_score = t_test(values['profits_for_2020'], values['profits_for_2021'])
        Minkowski = Minkowski_distance(values['employees'], values['salaries'])
        output[country] = [t_score, Minkowski]
    return output


def output_category(data):
    if not data:  # Empty data check
        return {}

    divided_by_category = {}  # Initialise Category Data
    for row in data:
        category = row['category']
        if category not in divided_by_category:
            divided_by_category[category] = []
        try:  # Extract and convert data values
            employees = int(row['number_of_employees'])
            profit_2020 = float(row['profits_in_2020(million)'])
            profit_2021 = float(row['profits_in_2021(million)'])
            if employees <= 0 or profit_2020 <= 0:
                continue

            profit_change = abs(profit_2020 - profit_2021)
            percentage = (profit_change / profit_2020) * 100
            organisations_data = {'id': row['organisation_id'],
                                  'employees': employees,
                                  'profit_change': round(percentage, 4)}
            divided_by_category[category].append(organisations_data)
        except ValueError:
            continue

    output = {}
    for category, organisations in divided_by_category.items():
        """Sort based on the criteria: number of employees then profit change in descending order"""
        sorted_organisations = sorted(organisations, key=lambda x: (-x['employees'], -x['profit_change']))

        rank = 1  # highest rank starts from 1
        prev_employees = sorted_organisations[0]['employees']
        prev_profit_change = sorted_organisations[0]['profit_change']
        for j, org in enumerate(sorted_organisations):
            if org['employees'] != prev_employees or org['profit_change'] != prev_profit_change:
                rank = j + 1
            org['rank'] = rank
            prev_employees = org['employees']
            prev_profit_change = org['profit_change']
            output.setdefault(category, {})[org['id']] = [org['employees'], org['profit_change'], org['rank']]

    return output


def main(csvfile):  # Wrapping function
    data = read_csvfile(csvfile)
    if not data:
        return {}, {}
    country = CaseInsensitiveDict(output_country(data))
    category = CaseInsensitiveDict(output_category(data))
    return country, category
