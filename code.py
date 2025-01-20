"""
Author: Leran Peng
Student Number: 23909531
Project Name: CITS1401 Project1
"""


def read_csvfile(file_name):
    """Read file and extract data, standardised data type, we also consider the extreme condition."""
    data = []
    try:
        with open(file_name, 'r') as file:
            raw_header = file.readline().strip().split(',')
            header = [i.lower().strip() for i in raw_header]

            for line in file:  # Read and parse each line, convert data type
                values = line.strip().split(',')
                if len(values) != len(header):
                    continue

                record = {}
                for i in range(len(header)):  # Use a loop adding the header and corresponding values to dictionary
                    key = header[i]
                    value = values[i].strip()
                    record[key] = value

                try:  # convert data type to integer or float
                    record['founded'] = int(record['founded'])
                    record['number of employees'] = int(record['number of employees'])
                    record['median salary'] = int(record['median salary'])
                    record['profits in 2020(million)'] = float(record['profits in 2020(million)'])
                    record['profits in 2021(million)'] = float(record['profits in 2021(million)'])
                except ValueError:
                    continue
                data.append(record)
    except FileNotFoundError:
        return 0
    return data


def normalised_string(a):
    """ Make sure the data input is string and convert them to lower case"""
    return a.strip().lower() if isinstance(a, str) else a


def max_min_org(data, country):
    """Find the organisations with the highest and lowest number of employees."""
    max_org, min_org = None, None
    max_employees = 0
    min_employees = float('inf')  # Initialise to infinity
    country = normalised_string(country)
    for record in data:
        if normalised_string(record['country']) == country and 1981 <= record['founded'] <= 2000:
            if record['number of employees'] > max_employees:
                max_org = record['name']
                max_employees = record['number of employees']
            # compare to infinity and find the organisation with the minimum employees
            if record['number of employees'] < min_employees:
                min_org = record['name']
                min_employees = record['number of employees']
    if not max_org or not min_org:
        return [0, 0]
    return [max_org, min_org]


def sd(numbers):  # Calculate sample standard deviation
    n = len(numbers)
    if n <= 1:
        return 0
    mean = sum(numbers) / n
    variance = sum((num - mean) ** 2 for num in numbers) / (n - 1)
    return round(variance ** 0.5, 4)


def output_sd_salaries(data, country):  # Take csvfile data back to expected sd
    country = normalised_string(country)
    country_salaries = []
    for record in data:
        if normalised_string(record['country']) == country:
            country_salaries.append(record['median salary'])

    """Creating a list of all median salaries from the dictionaries in the "data" list"""
    all_salaries = [record['median salary'] for record in data]
    return [round(sd(country_salaries), 4), round(sd(all_salaries), 4)]


def ratio(data, country):
    increase, decrease = 0, 0
    country = normalised_string(country)
    for record in data:
        if record['country'].lower() != country.lower():  # check matching countries
            continue
        profit_change = record['profits in 2021(million)'] - record['profits in 2020(million)']
        if profit_change > 0:
            increase += profit_change
        else:
            decrease += abs(profit_change)
    if decrease == 0:  # Any number cannot divide by 0
        return 0
    return round(increase / decrease, 4)


def cor(dataset_x, dataset_y):  # Calculate correlation
    if len(dataset_x) <= 1 or len(dataset_y) <= 1:
        return 0
    mean_x = sum(dataset_x) / len(dataset_x)
    mean_y = sum(dataset_y) / len(dataset_y)
    # Calculate covariance
    cov_xy = 0
    for x, y in zip(dataset_x, dataset_y):
        cov_xy += (x - mean_x) * (y - mean_y)
    cov_xy /= (len(dataset_x) - 1)
    # Exclude cases where the denominator is equal to 0
    denominator = sd(dataset_x) * sd(dataset_y)
    if denominator == 0:
        return 0
    return round(cov_xy / denominator, 4)


def output_cor(data, country):  # Cor of 2021 salaries & profits for firms with 2020-21 profit growth.
    median_salaries = []
    profits_2021 = []
    country = normalised_string(country)
    for record in data:
        if normalised_string(record['country']) == country:
            if record['profits in 2021(million)'] > record['profits in 2020(million)']:
                median_salaries.append(record['median salary'])
                profits_2021.append(record['profits in 2021(million)'])
    return round(cor(median_salaries, profits_2021), 4)


def main(csvfile, country):
    data = read_csvfile(csvfile)  # Parse the data in file
    if data == 0:  # Exclude the extreme condition
        return 0
    """
       Return1: Organisation with most and fewest employees.
       Return2: Standard deviation of country's and all organisations' median salary
       Return3: Ratio of positive to negative changes from 2020-21
       Return4: Correlation of 2021 salaries & profits for firms with 2020-21 profit growth.
    """
    return (
        max_min_org(data, country),
        output_sd_salaries(data, country),
        ratio(data, country),
        output_cor(data, country),
    )