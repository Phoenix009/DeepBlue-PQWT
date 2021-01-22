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
    pickle_off = open ("static/models/model.sav", "rb")
    model = pickle.load(pickle_off)
    return model

def save_model(model):
    """
    saves the ml model by serializing the pickle file 
    """
    with open('static/models/model.sav', 'wb') as fh:
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
        'arrival_time': vqueue.joined_at.hour*60 + vqueue.joined_at.minute,
        'position': vqueue.get_patients_ahead(),
        'gender': get_gender(vqueue.patient.gender)
    }

    y = vqueue.wait_time()

    print(x, y)
    return x, y

def predict_waittime(vqueue):
    """
    predicts the wait time 
    """
    x = {
        'age': vqueue.patient.age,
        'arrival_time': vqueue.joined_at.hour*60 + vqueue.joined_at.minute,
        'active_patients': vqueue.queue.get_active_patients_count(),
        'gender': get_gender(vqueue.patient.gender)
    }
    model = load_model()
    return model.predict_one(x)

