import ipywidgets as widgets
import time

def get_user_input_widgets():
    num_tasks = widgets.IntSlider(
        value=100,
        min=20,
        max=1000,
        step=1,
        description='Number of tasks:',
        style = {'description_width': 'initial'},
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d'
    )
    num_workers = widgets.IntSlider(
        value=10,
        min=5,
        max=30,
        step=1,
        description='Max number of workers:',
        style = {'description_width': 'initial'},
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d'
    )
    first_number = widgets.IntText(
        value=2,
        description='Starting number',
        style = {'description_width': 'initial'},
        disabled=False
    )
    display(widgets.HBox([num_tasks, num_workers, first_number])) # displays the input widgets 
    return [num_tasks, num_workers, first_number]

def get_output_widgets(input_widgets):
    tasks_done_bar = widgets.IntProgress(
        value=0,
        min=0,
        max=input_widgets[0].value,
        description='Percent of tasks complete:',
        style = {'description_width': 'initial'},
        orientation='horizontal'
    )
    tasks_idling = widgets.IntProgress(
        value=0,
        min=0,
        max=input_widgets[1].value,
        description='Percent of workers idle',
        style = {'description_width': 'initial'},
        orientation='horizontal'
    )
    workers_connected = widgets.IntProgress(
        value=0,
        min=0,
        max=input_widgets[1].value,
        description='Percent of max workers connected',
        style = {'description_width': 'initial'},
        orientation='horizontal'
    )
    status_message = widgets.Text(
        value='Initializing workers',
        description='Workqueue Status',
        disabled=True,
        style = {'description_width': 'initial'},
        orientation='horizontal'
    )
    worker_time = widgets.Text(
        description='Time spent by workers (Seconds)',
        disabled=True,
        style = {'description_width': 'initial'},
        orientation='horizontal'
    )
    tasks_per_second = widgets.FloatText(
        value=0,
        description='Average tasks complete per second',
        style = {'description_width': 'initial'},
        disabled=True
    )

    worker_properties = ["Number of workers", "Cores", "Memory", "Disk", "GPUs"]
    worker_array = []
    for name in worker_properties:
        worker_array.append(widgets.Text(description=name, disabled=True, style = {'description_width': 'initial'}, layout=widgets.Layout(width='15%', height='40px')))
    display(widgets.HBox([status_message, tasks_per_second, worker_time]))
    display(widgets.HBox([tasks_done_bar, workers_connected, tasks_idling]))
    # display output information
    task_output_storage = []
    create_progress_tracker(task_output_storage, input_widgets)
    return [tasks_done_bar, workers_connected, tasks_idling, tasks_per_second, worker_array, status_message, worker_time, task_output_storage]

def create_progress_tracker(task_output_storage, input_widgets):
    # the three following lines are just shortcuts to access the input widget numbers
    #number_of_tasks = input_widgets[0] 
    #number_of_workers = input_widgets[1]
    #starting_number = input_widgets[2]
    for i in range(input_widgets[2].value, input_widgets[2].value + input_widgets[0].value + input_widgets[1].value + 10):
        task_output_storage.append(widgets.ToggleButton(
            value=False,
            description=str(i - 2),
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            layout=widgets.Layout(width='20%', height='20px')
        ))
    horizontal_boxes = 15
    vertical_boxes = input_widgets[0].value // horizontal_boxes + 1
    vertical_temp = []
    for j in range(vertical_boxes):
        horizontal_temp = []
        for i in range(horizontal_boxes):
            if (i + j * horizontal_boxes + 2) > input_widgets[0].value:
                break
            horizontal_temp.append(task_output_storage[i + j * horizontal_boxes + 2])
        vertical_temp.append(widgets.HBox(horizontal_temp))
    output = widgets.VBox(vertical_temp)
    display(output)
def update_output(output_widgets, q, starting_time, t):
    if t.output == 1: # if x is a prime number then update it accordingly
        output_widgets[7][int(t.id) + 1].disabled = True
    output_widgets[7][int(t.id) + 1].button_style = 'success'
    for i in range(q.stats.workers_connected + 1): # update the display of which tasks are currently being worked on
        if (int(t.id) + 1 - i) > 0:
            if (output_widgets[7][int(t.id) + 1 - i].button_style == ''):
                    output_widgets[7][int(t.id) + 1 - i].button_style='warning'
    output_widgets[0].value = q.stats.tasks_done
    output_widgets[1].value = q.stats.workers_connected
    output_widgets[2].value = q.stats.workers_idle
    output_widgets[3].value = output_widgets[0].value / (time.perf_counter() - starting_time)
    output_widgets[5].value = "Getting worker output"
    output_widgets[6].value = str(q.stats.time_workers_execute / 1000000)
    