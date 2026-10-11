#Section 3:

from catalog.search import search_courses


def main() -> None:
    for course in search_courses("python"):
        print(course.model_dump_json())


if __name__ == "__main__":
    main()


#Section 2:

# def search_courses(query: str) -> list[str]:
#     titles = ["Python foundations", "Python for data analysis", "Machine learning introduction"]
#     matches = []
#     for title in titles:
#         if query.strip().casefold() in title.casefold():
#             matches.append(title)
#     return matches


# def main() -> None:
#     print(search_courses("python"))


# if __name__ == "__main__":
#     main()

#---Main original -----
# def main():
#     print("Hello from course-catalog!")


# if __name__ == "__main__":
#     main()