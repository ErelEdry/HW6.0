
class Worker:
    def __init__(self, worker_id, name, skills, availability, salary):
        if not isinstance(worker_id,int):
            raise TypeError("worker_id must to be an int")
        if worker_id<0:
            raise ValueError("worker_id must to be an natural number")
        if not isinstance(name,str):
            raise TypeError("name must to be a string")
        if name == "":
            raise ValueError("name can't be an empty string")
        if not isinstance(skills, dict):
            raise TypeError("skills must to be a dictionary")
        if len(skills) == 0 or any(not isinstance(value, int) or value <= 0 for value in skills.values()):
            raise ValueError("Skills must all be positive integers.")
        if not isinstance(availability,list) or not all(isinstance(item,tuple)  and all(isinstance(x,int) for x in item)for item in availability):
            raise TypeError("availability must to be a list with tuple with 2 int values!")
        if all(len(item)!=2 for item in availability) or any(not (0 <= t[0] <= 23 and 0 <= t[1] <= 23 and t[0] < t[1]) for t in availability):
            raise ValueError("availability must to be tuple with 2 int values that start time is smaller than end time and between 0-23")
        if not isinstance(salary,(float,int)):
            raise TypeError("Salary must to be a float or int number")
        if salary<1:
            raise ValueError("Salary must to be a number that bigger than 0!")
        if not isinstance(name, str):
            raise TypeError("name must to be a string")
        if name == "" or not name.isalpha():
            raise ValueError("Name must be a all alphabetic and non-empty string.")


        self.__worker_id=worker_id
        self.name=name
        self.__skills=skills
        self.__availability=availability
        self.__salary=salary

    def __repr__(self):
        return f"Worker ID: {self.__worker_id}, Name: {self.name}, Skills: {self.__skills}, Availability: {self.__availability}, Salary: {self.__salary}"
    
    def update_salary(self, additional_salary):
        if not isinstance(additional_salary,(int,float)):
            raise TypeError("additional_salary must to be a number!")
        if additional_salary < 1:
            raise ValueError("additional_salary must to be bigger than 0!")
        self.__salary+=additional_salary


    def update_skills(self, new_skills):
        if not isinstance(new_skills, dict):
            raise TypeError("skills must to be a dictionary")
        if len(new_skills) == 0 or any(not isinstance(value, int) or value <= 0 for value in new_skills.values()):
            raise ValueError("Skills must all be positive integers.")
        for skill in new_skills:
            self.__skills[skill]=1

    def update_availability(self, new_availability):
        if not isinstance(new_availability, tuple) or not all(isinstance(x, int) for x in new_availability):
            raise TypeError("new_availability must be a tuple with 2 int values!")
        if len(new_availability) != 2 or not (
                0 <= new_availability[0] <= 23 and 0 <= new_availability[1] <= 23 and new_availability[0] <
                new_availability[1]):
            raise ValueError("new_availability must be a tuple with 2 int values that start time is smaller than end time and between 0-23")

        for i, curr_slot in enumerate(self.__availability):
            if curr_slot[0] == new_availability[1]:
                self.__availability[i] = (new_availability[0], curr_slot[1])
                return
            elif curr_slot[1] == new_availability[0]:
                self.__availability[i] = (curr_slot[0], new_availability[1])
                return
            elif (curr_slot[0] <= new_availability[0] <= curr_slot[1] or
                  curr_slot[0] <= new_availability[1] <= curr_slot[1]):
                return

        self.__availability.append(new_availability)

    def get_availability(self):
        return self.__availability
    
    def get_skills(self):
        return self.__skills

    def get_salary(self):
        return self.__salary
    
    def get_worker_id(self):
       return self.__worker_id


