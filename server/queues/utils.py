import pickle
from river import metrics
from river import linear_model
import pickle

def get_gender(gender):
    """
    Gets the gender of the patients in numerical form 
    for the  ml model 
    """
    if gender=='MALE': return 1
    elif gender=='FEMALE': return 2
    else: return 3

def load_model():
    """
    loads the ml model by deserializing the pickle file 
    """
    pickle_off = open ("core/static/models/model.sav", "rb")
    model = pickle.load(pickle_off)
    return model

def save_model(model):
    """
    saves the ml model by serializing the pickle file 
    """
    with open('core/static/models/model.sav', 'wb') as fh:
        pickle.dump(model, fh)

def update_model(vqueue):
    """
    updates the ml model 
    """
    x, y = get_data(vqueue)
    model = load_model()
    model.learn_one(x, y)
    save_model(model)


def get_data(vqueue):
    """
    converts the data from virtual_queue object 
    into the format required by river to update the ml model 
    """
    x = {
        'age': vqueue.patient.age,
        'actual_arrival_time': vqueue.joined_at.hour*60 + vqueue.joined_at.minute,
        'position': vqueue.get_patients_ahead(),
        'gender': get_gender(vqueue.patient.gender)
    }

    y = vqueue.wait_time()

    print(x, y)
    return x, y

def predict_waittime(vqueue, completion):
    """
    predicts the wait time 
    """
    
    actual_arrival_time = vqueue.joined_at.hour*60 + vqueue.joined_at.minute
    x = {
        'age': vqueue.patient.age,
        'actual_arrival_time': actual_arrival_time,
        'position': vqueue.queue.get_active_patients_count(),
        'gender': get_gender(vqueue.patient.gender)
    }
    print('completion:', completion)
    model = load_model()
    service_time = model.predict_one(x)
    enter_service = max(actual_arrival_time, completion)
    completion = enter_service + service_time
    wait_time = enter_service - actual_arrival_time
    return wait_time, completion

