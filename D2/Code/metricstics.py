class Metricstics:
    def __init__(self, data):
        if not data:
            raise ValueError("Data not present.")
        self.data = self.manual_sort(data)

    # Implementing a simple sorting algorithm
    def manual_sort(self, data):
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            while j >=0 and key < data[j]:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key
        return data

    # Implementing manual minimum function
    def minimum(self):
        return self.data[0]  # Assuming the data is sorted, the first element is the minimum

    # Implementing manual maximum function
    def maximum(self):
        return self.data[-1]  # Assuming the data is sorted, the last element is the maximum

    # Implementing manual mean function
    def mean(self):
        total = sum(self.data)
        return total / len(self.data)

    # Implementing manual median function
    def median(self):
        n = len(self.data)
        mid = n // 2
        if n % 2 == 0:
            # If even number of data points, median is the average of the two middle numbers
            return (self.data[mid - 1] + self.data[mid]) / 2
        else:
            # If odd number of data points, median is the middle number
            return self.data[mid]

    # Implementing manual mode function
    def mode(self):
        frequency = {}
        max_freq = 0
        mode_val = set()
        for num in self.data:
            frequency[num] = frequency.get(num, 0) + 1
            if frequency[num] > max_freq:
                max_freq = frequency[num]
                mode_val = {num}
            elif frequency[num] == max_freq:
                mode_val.add(num)
        return mode_val if len(mode_val) > 1 else mode_val.pop()

    # Implementing manual mean absolute deviation function
    def mean_absolute_deviation(self):
        mean_val = self.mean()
        total_deviation = sum(abs(x - mean_val) for x in self.data)
        return total_deviation / len(self.data)

    # Implementing manual standard deviation function
    def standard_deviation(self):
        mean_val = self.mean()
        variance = sum((x - mean_val) ** 2 for x in self.data) / len(self.data)
        return variance ** 0.5
