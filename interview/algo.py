# 数据结构与算法

## 快速排序

## 冒泡排序
def pope(input_list):
    list_length = len(input_list)

    for i in range(list_length - 1):
        for j in range(list_length - 1 - i):
            if input_list[j] > input_list[j+1]:
              input_list[j], input_list[j+1] = input_list[j+1], input_list[j]
    return input_list

def quick_sort(input_list, start_index, end_index):
    if start_index >= end_index:
        return
    origin_end = end_index
    origin_index = start_index
    sentry = input_list[origin_index]

    while start_index != end_index:
        while start_index < end_index and input_list[end_index] >= sentry:
            end_index -= 1

        while start_index < end_index and input_list[start_index] <= sentry:
            start_index += 1

        if start_index < end_index:
            input_list[start_index], input_list[end_index] = input_list[end_index], input_list[start_index]
        
        print(input_list)
    
    input_list[origin_index] = input_list[start_index]
    input_list[start_index] = sentry

    print(input_list)

    quick_sort(input_list, origin_index, start_index - 1)
    quick_sort(input_list, start_index+1, origin_end)


def quick_sorted_2(input_list, start_index, end_index):
    if start_index >= end_index:
        return
    
    head = start_index
    tail = end_index
    sentry = input_list[head]

    while start_index != end_index:
        while start_index < end_index and input_list[end_index] >= sentry:
            end_index -= 1
        
        while start_index < end_index and input_list[start_index] <= sentry:
            start_index += 1

        if start_index < end_index:
            input_list[start_index], input_list[end_index] = input_list[end_index], input_list[start_index]

    input_list[head] = input_list[start_index]
    input_list[start_index] = sentry

    quick_sorted_2(input_list, head, start_index-1)
    quick_sorted_2(input_list, start_index+1, tail)


if __name__ == '__main__':
    input_list = [10,2,15,23,432,1,5,3,89]
    res = quick_sorted_2(input_list, 0, len(input_list)-1)
    print('res:', input_list)