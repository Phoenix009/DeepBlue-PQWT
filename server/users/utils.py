from django.core.mail import send_mail 


def send_staff_registration_mail(staff, password, admin_email):
    subject = 'You have been added as a Staff'
    body = f"""
    You have been added in the Hospital {staff.department.hospital.name}
    in the {staff.department.name} Department
    by {admin_email}
    Following are your credentials:
    Username: {staff.user.username}
    Password: {password}s
    """
    sender = 'stationeymanagerkjsieit@gmail.com'
    receiver = staff.user.email 
    send_mail(
        subject,
        body,
        sender,
        [receiver,],
        fail_silently=False
    )