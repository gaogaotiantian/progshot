from progshot import trace


def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


@trace
def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                swap(arr, j, j + 1)


arr = [54, 98, 42, 40, 25, 45, 33, 82]
bubble_sort(arr)
print(arr)
