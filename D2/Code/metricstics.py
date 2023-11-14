class Metricstics:
    """
    The Metricstics class provides functionality to calculate various statistical
    metrics on a list of numerical data.
    """
    
    def __init__(self, data):
        """
        Initialize the Metricstics object with data after validation and sorting.
        """
        self.data = self._initialize_data(data)

    def _initialize_data(self, data):
        """
        Validate and sort the data upon initialization.
        """
        self._validate_data(data)
        return self._sort_data(data)

    def _validate_data(self, data):
        """
        Validate the data to ensure it is present and contains only numeric values.
        Raises a ValueError if the data is empty or contains non-numeric values.
        """
        if not data:
            raise ValueError("Data not present.")
        for value in data:
            if not isinstance(value, (int, float)):
                raise ValueError("Not a numerical value")

    def _sort_data(self, data):
        """
        Sort the data using insertion sort algorithm.
        """
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            while j >= 0 and key < data[j]:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key
        return data

    def minimum(self):
        """
        Return the minimum value in the data.
        """
        return self.data[0]

    def maximum(self):
        """
        Return the maximum value in the data.
        """
        return self.data[-1]

    def mean(self):
        """
        Calculate and return the mean of the data.
        """
        total = self._manual_sum(self.data)
        return total / len(self.data)

    def median(self):
        """
        Calculate and return the median of the data.
        """
        n = len(self.data)
        mid = n // 2
        if n % 2 == 0:
            return (self.data[mid - 1] + self.data[mid]) / 2
        else:
            return self.data[mid]

    def mode(self):
        """
        Calculate and return the mode(s) of the data.
        If there are multiple modes, return a list of modes.
        """
        frequency = self._calculate_frequency(self.data)
        max_freq = max(frequency.values())
        modes = [number for number, freq in frequency.items() if freq == max_freq]
        return modes if len(modes) > 1 else modes[0]

    def mean_absolute_deviation(self):
        """
        Calculate and return the mean absolute deviation of the data.
        """
        mean_val = self.mean()
        total_deviation = self._manual_sum(abs(x - mean_val) for x in self.data)
        return total_deviation / len(self.data)

    def standard_deviation(self):
        """
        Calculate and return the standard deviation of the data.
        """
        mean_val = self.mean()
        variance = self._manual_sum((x - mean_val) ** 2 for x in self.data) / len(self.data)
        return self._sqrt(variance)

    def _manual_sum(self, iterable):
        """
        Manually sum up an iterable of numbers and return the total.
        """
        total = 0
        for item in iterable:
            total += item
        return total

    def _calculate_frequency(self, data):
        """
        Calculate the frequency of each value in the data and return a dictionary.
        """
        frequency = {}
        for num in data:
            frequency[num] = frequency.get(num, 0) + 1
        return frequency

    def _sqrt(self, value):
        """
        Calculate and return the square root of a value using Newton's method.
        """
        x = value
        while True:
            root = (x + value / x) / 2
            if abs(root - x) < 0.000001:
                return root
            x = root

    # Dummy methods for future features or complex operations
    def _dummy_complex_operation(self):
        """
        Placeholder for a complex operation to be implemented in the future.
        Currently does nothing.
        """
        pass

    def future_feature_placeholder(self):
        """
        Another placeholder for potential future expansion of the class.
        Currently does nothing.
        """
        pass
