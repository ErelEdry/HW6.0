from id_generator import id_generator
class Task:
    def __init__(self, task_id, description, urgency, importance, time_window, needed_skills):
        if not isinstance(task_id,int):
            raise TypeError("task_id must to be an int")
        if task_id < 1:
            ValueError("task_id must to be bigger than 0")
        if not isinstance(description,str):
            raise TypeError("Description must to be a string")
        if description == "":
            raise ValueError("Description must be a non-empty string.")
        if not isinstance(urgency,int):
            raise TypeError("Urgency need to be an int")
        if urgency < 1:
            ValueError("task_id must to be bigger than 0")
        if not isinstance(importance, int):
            raise TypeError("Importance need to be an int")
        if importance < 1:
            ValueError("Importance must to be bigger than 0")
        if not isinstance(time_window,tuple) or len(time_window)!=2:
            raise TypeError("time_window must to be a tuple with just 2 values")
        if not isinstance(time_window[0],int) or not isinstance(time_window[1],int):
            raise TypeError("time_window must to be a tuple with int values")
        if not (0 <= time_window[0] <= 23) or not (0 <= time_window[1] <= 23):
            raise ValueError("time_window values must to be between 0-23")
        if time_window[1]<=time_window[0]:
            raise ValueError("time_window end value must to be bigger from start value")
        if not isinstance(needed_skills,dict) or any(not isinstance(value, int) for value in needed_skills.values()) or any(not isinstance(key, str) for key in needed_skills.keys()):
            raise TypeError("needed_skills must b a dictionary and the keys must be string and values must to be int")
        if len(needed_skills)==0 or "" in needed_skills or any(value<1 for value in needed_skills.values()):
            raise ValueError("needed_skills can't be an empty dictionary or an empty string in keys or values smaller than one")
        self.__task_id=task_id
        self.description=description
        self.urgency=urgency
        self.importance=importance
        self.time_window=time_window
        self.needed_skills=needed_skills
    def __repr__(self):
        return f"Task ID: {self.__task_id}, Description: {self.description}, Urgency: {self.urgency}, Importance: {self.importance}, Time Window: {self.time_window}, Needed skills: {self.needed_skills}"
    def get_task_id(self):
        return self.__task_id
