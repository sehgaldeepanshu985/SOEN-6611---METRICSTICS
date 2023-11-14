class Metricstics:
    def __init__(self, data):
        if not data:
            raise ValueError("Data not present.")
        self.data = self._sort_data(data)

    def _sort_data(self, data):
        # Implementing a simple sorting algorithm (Insertion Sort)
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            while j >= 0 and key < data[j]:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key
        return data

    def _sum_data(self, data):
        # Manually summing the data
        total = 0
        for num in data:
            total += num
        return total

    def minimum(self):
        # The first element of the sorted data is the minimum
        return self.data[0]

    def maximum(self):
        # The last element of the sorted data is the maximum
        return self.data[-1]

    def mean(self):
        # Mean is sum of data divided by the number of data points
        total = self._sum_data(self.data)
        return total / len(self.data)

    def median(self):
        # Median is the middle value or the average of the two middle values
        n = len(self.data)
        mid = n // 2
        if n % 2 == 0:
            return (self.data[mid - 1] + self.data[mid]) / 2
        else:
            return self.data[mid]

    def mode(self):
        # Mode is the most common data point(s)
        frequency = {}
        max_count = 0
        for num in self.data:
            frequency[num] = frequency.get(num, 0) + 1
            if frequency[num] > max_count:
                max_count = frequency[num]

        return {num for num, freq in frequency.items() if freq == max_count}

    def mean_absolute_deviation(self):
        # Mean Absolute Deviation is the average of absolute differences between each data point and the mean
        mean_value = self.mean()
        total_deviation = sum(abs(x - mean_value) for x in self.data)
        return total_deviation / len(self.data)

    def standard_deviation(self):
        # Standard Deviation is the square root of the average of squared differences from the Mean
        mean_value = self.mean()
        sum_of_squares = sum((x - mean_value) ** 2 for x in self.data)
        return (sum_of_squares / len(self.data)) ** 0.5
