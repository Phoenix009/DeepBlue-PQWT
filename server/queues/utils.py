import qrcode
import pickle
from river import metrics
from river import linear_model
import pickle


def generate_qrcode(data:str):
    qr = qrcode.QRCode(
        version = 1,
        box_size = 10,
        border = 5
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    return img


def get_gender(gender):
    if gender=='MALE': return 1
    elif gender=='FEMALE': return 2
    else: return 3

def load_model():
    pickle_off = open ("static/models/model.sav", "rb")
    model = pickle.load(pickle_off)
    return model

def save_model(model):
    with open('static/models/model.sav', 'wb') as fh:
        pickle.dump(model, fh)



def update_model(vqueue):
    x, y = get_data(vqueue)
    model = load_model()
    model.learn_one(x, y)
    save_model(model)


def get_data(vqueue):
    x = {
        'age': vqueue.patient.age,
        'arrival_time': vqueue.joined_at.hour*60 + vqueue.joined_at.minute,
        'active_patients': vqueue.queue.get_active_patients_count(),
        'gender': get_gender(vqueue.patient.gender)
    }

    y = vqueue.wait_time()

    print(x, y)
    return x, y

def predict_waittime(vqueue):
    x = {
        'age': vqueue.patient.age,
        'arrival_time': vqueue.joined_at.hour*60 + vqueue.joined_at.minute,
        'active_patients': vqueue.queue.get_active_patients_count(),
        'gender': get_gender(vqueue.patient.gender)
    }
    model = load_model()
    return model.predict_one(x)

