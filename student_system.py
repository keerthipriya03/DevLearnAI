def calculate_average(marks):

    total = 0

    for mark in marks:
        total += mark

    return total / len(marks)


def find_grade(average):

    if average >= 90:
        return "A"

    elif average >= 75:
        return "B"

    elif average >= 60:
        return "C"

    else:
        return "D"


def generate_result(marks):

    average = calculate_average(marks)

    grade = find_grade(average)

    return {
        "average": average,
        "grade": grade
    }