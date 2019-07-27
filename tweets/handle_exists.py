from main.models import Handle

def handle_exists(handle):
    list_of_handles_raw = list(Handle.objects.values('handle'))
    list_of_handles = []
    x = False
    for i in range(len(list_of_handles_raw)):
        list_of_handles.append(list_of_handles_raw[i]['handle'])
    if handle in list_of_handles:
        x = True
    return x
