from task_system import TaskSystem

task = TaskSystem()

# ADD TASKS
task.add_task("Study Python")
task.add_task("Do assignment")

# SHOW TASKS
print(task.get_tasks())

# COMPLETE FIRST TASK
task.complete_task(0)

# DELETE SECOND TASK
task.delete_task(1)

print(task.get_tasks())