import math
from collections import defaultdict
import copy
from functools import reduce


def chunks(lst):
    for i in range(len(lst) - 1):
        yield lst[i:i + 2]


class Solution:
    def __init__(self) -> None:
        super().__init__()
        self.data = None
        self.input_file_name = 'C:/Users/Anshumaan/Documents/Codes/hashcode21/c.txt'
        self.output_file_name = 'C:/Users/Anshumaan/Documents/Codes/hashcode21/checkmate.txt'
        self.STREETS = {}
        self.CARS = {}
        self.STREETS_LENS = {}
        self.DURATION = None
        self.NUM_INTER = None
        self.NUM_STREETS = None
        self.NUM_CARS = None
        self.BONUS = None
        self.BEST_CARS_STREET = {}
        self.used_streets_by_cars = set()

    def read_input(self, file_name):
        with open(f'./input/{file_name}') as f:
            self.data = [i.strip() for i in f.readlines()]
            line_num = 0
            self.DURATION, self.NUM_INTER, self.NUM_STREETS, self.NUM_CARS, self.BONUS = map(int, self.data[0].split(' '))
            for _ in range(self.NUM_STREETS):
                line_num += 1
                line = self.data[line_num]
                START, END, NAME, LEN = line.split(' ')
                self.STREETS[NAME] = {'start': int(START), 'end': int(END), 'len': int(LEN)}
                self.STREETS_LENS[NAME] = int(LEN)

            for i in range(self.NUM_CARS):
                line_num += 1
                line = self.data[line_num]
                CAR_STREETS = line.split(' ')[1:]
                self.CARS[i] = list(CAR_STREETS)

    def path_length(self, path):
        path_score = 0
        for street in path[1:]:
            path_score += 1 + self.STREETS_LENS[street]
        return path_score

    def pop_unused_streets(self):
        all_streets = set(street_name for street_name in self.STREETS)
        streets_to_remove = all_streets - self.used_streets_by_cars
        print(f'removing streets {len(streets_to_remove)}')
        for street_name in streets_to_remove:
            self.STREETS_LENS.pop(street_name)
            self.STREETS.pop(street_name)

    def run(self, file_name):
        self.read_input(file_name)
        for key, streets in self.CARS.items():
            self.used_streets_by_cars.update(streets)
            path_length = self.path_length(streets)
            if path_length <= self.DURATION:
                self.BEST_CARS_STREET[key] = path_length

        self.pop_unused_streets()
        BEST_CARS = sorted(self.BEST_CARS_STREET, key=self.BEST_CARS_STREET.get)

        streets_to_intersection_map = {}
        street_by_start = defaultdict(list)
        street_by_end = defaultdict(list)
        for street_slug, data in self.STREETS.items():
            street_by_start[data['start']].append(street_slug)
        for street_slug, data in self.STREETS.items():
            street_by_end[data['end']].append(street_slug)

        for street_slug, data in self.STREETS.items():
            for second_street in street_by_start[data['end']]:
                streets_to_intersection_map[f'{street_slug}__{second_street}'] = data['end']

        intersection_perf = defaultdict(lambda: 0)  # street_name__int_id
        streets_by_intersection_id = defaultdict(set)

        for car_id in BEST_CARS:
            STREETS_TO_GO = self.CARS[car_id]
            for item in chunks(STREETS_TO_GO):
                first_street, second_street = item
                intersection_id = streets_to_intersection_map[f'{first_street}__{second_street}']
                intersection_perf[f'{first_street}__{intersection_id}'] += 1
                streets_by_intersection_id[intersection_id].add(first_street)

        result_data = {}
        intersection_perf_ratio = {}
        for intersection_id, streets in streets_by_intersection_id.items():
            numbers = []
            for street in streets:
                numbers.append(intersection_perf[f'{street}__{intersection_id}'])
            if len(numbers) > 2:
                gcd = reduce(lambda x, y: math.gcd(x, y), numbers)
            elif len(numbers) == 2:
                gcd = math.gcd(*numbers)
            else:
                gcd = 1

            for street in streets:
                ratio = intersection_perf[f'{street}__{intersection_id}'] / gcd
                intersection_perf_ratio[f'{street}__{intersection_id}'] = ratio
                result_data[intersection_id] = {street: int(ratio)}

        # for CAR_ID in BEST_CARS:
        #     STREETS_TO_GO = self.CARS[CAR_ID]
        #     for STREET in STREETS_TO_GO:
        #         street = self.STREETS[STREET]
        #         result_data[street['end']] = {STREET: 1}

        result_lines = []
        result_lines.append(str(len(result_data)))
        for intersection_id, streets in result_data.items():
            result_lines.append(str(intersection_id))
            result_lines.append(str(len(streets)))
            for street_name, seconds in streets.items():
                result_lines.append(f'{street_name} {seconds}')
        with open(file_name, 'w') as f:
            f.writelines('\n'.join(result_lines))


s = Solution()
# for file_name in ['a.txt', 'b.txt', 'c.txt', 'd.txt', 'e.txt', 'f.txt']:
for file_name in ['c.txt']:
    s.run(file_name)
