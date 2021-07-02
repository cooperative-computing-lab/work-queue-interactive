import ipywidgets as widgets
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
    return [num_tasks, num_workers, first_number]

def get_output_widgets(number_of_tasks, number_of_workers):
    tasks_done_bar = widgets.IntProgress(
        value=0,
        min=0,
        max=number_of_tasks,
        description='Percent of tasks complete:',
        style = {'description_width': 'initial'},
        orientation='horizontal'
    )
    tasks_idling = widgets.IntProgress(
        value=0,
        min=0,
        max=5,
        description='Percent of workers idle',
        style = {'description_width': 'initial'},
        orientation='horizontal'
    )
    workers_connected = widgets.IntProgress(
        value=0,
        min=0,
        max=number_of_workers,
        description='Percent of max workers connected',
        style = {'description_width': 'initial'},
        orientation='horizontal'
    )
    status_message = widgets.Text(
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
    return [tasks_done_bar, workers_connected, tasks_idling, tasks_per_second, worker_array, status_message, worker_time]

def create_progress_tracker(task_output_storage, number_of_tasks, starting_number, number_of_workers):
    for i in range(starting_number, starting_number + number_of_tasks + number_of_workers + 10):
        task_output_storage.append(widgets.ToggleButton(
            value=False,
            description=str(i - 2),
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            layout=widgets.Layout(width='20%', height='20px')
        ))
    horizontal_boxes = 15
    vertical_boxes = number_of_tasks // horizontal_boxes + 1
    vertical_temp = []
    for j in range(vertical_boxes):
        horizontal_temp = []
        for i in range(horizontal_boxes):
            if (i + j * horizontal_boxes + 2) > number_of_tasks:
                break
            horizontal_temp.append(task_output_storage[i + j * horizontal_boxes + 2])
        vertical_temp.append(widgets.HBox(horizontal_temp))
    output = widgets.VBox(vertical_temp)
    display(output)