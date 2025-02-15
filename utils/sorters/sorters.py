class Sorters:
    
    @staticmethod
    def quicksort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return Sorters.quicksort(left) + middle + Sorters.quicksort(right)
    
    @staticmethod
    def merge_sort(arr):
        if len(arr) <= 1:
            return arr

        def merge(left, right):
            merged = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
            merged.extend(left[i:])
            merged.extend(right[j:])
            return merged

        mid = len(arr) // 2
        left = Sorters.merge_sort(arr[:mid])
        right = Sorters.merge_sort(arr[mid:])
        return merge(left, right)
    
    @staticmethod
    def radix_sort(arr):
        if not arr:
            return arr

        max_val = max(arr)
        exp = 1
        while max_val // exp > 0:
            arr = Sorters._counting_sort(arr, exp)
            exp *= 10
        return arr

    @staticmethod
    def _counting_sort(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10 

        for number in arr:
            index = (number // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1

        return output