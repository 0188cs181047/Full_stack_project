from django.db import models
from django.forms import SelectDateWidget
from django.contrib.auth import get_user_model

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class Asset_inform(models.Model):
    BOOKED = 'BUFFER'
    APPROVED = 'IN-USE'

    STATUS_TYPE = (
        (BOOKED, 'BUFFER'),
        (APPROVED, 'IN-USE')
    )
    email = models.EmailField(null=True)
    asset_id = models.CharField(max_length=100)
    asset_owner = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=200)
    asset_status = models.CharField(max_length=20, choices=STATUS_TYPE,null=True)
    # date_created = models.DateField(auto_now=True)
    Asset_date = models.DateTimeField(null=True)
    requested_approval = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.asset_id)
    

    def request_approval(self):
        if self.approved:
            self.approved=False
        self.requested_approval = True
        self.save()

    def approve_approval(self, email):
        if self.requested_approval:
            self.approved = True
            self.save()

            # Get the user with the provided email
            User = get_user_model()
            user = User.objects.filter(email=email).first()

            if user:
                message = """Hello,<br><br>
                             You have approved the pending asset request.
                             <br>
                        Here are the details of the approved asset transfer:<br>
                        Asset ID: {asset_id}<br>
                        asset_owner: {asset_owner}<br><br>
                        regards,<br>
                        Asset Management System
                        """.format(asset_id=self.asset_id,
                                   asset_owner=self.asset_owner,)

                # Send email notification to the user
                context = {'Asset_inform': self, 'user': user}
                html_message = message
                plain_message = message
                send_mail(
                    'Asset Approval',
                    plain_message,
                    'acteviashiv@gmail.com',
                    [user.email],
                    html_message=html_message,
                )

                # Send email notification to the recipient
                recipient_message = """Hello,<br><br>
                             Your asset request was approved.
                             <br>
                        Here are the details of the approved asset transfer:<br>
                        Asset ID: {asset_id}<br>
                        asset_owner: {asset_owner}<br><br>
                        regards,<br>
                        Asset Management System
                        """.format(asset_id=self.asset_id,
                                   asset_owner=self.asset_owner,)

                # Send email notification to the recipient
                recipient_html_message = recipient_message
                recipient_plain_message = recipient_message
                send_mail(
                    'Asset Approval',
                    recipient_plain_message,
                    'acteviashiv@gmail.com',
                    [email],
                    html_message=recipient_html_message,
                )

    def reject_approval(self):
        if self.requested_approval:
            self.requested_approval = False
            self.save()
            

class asset_Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    Asset_inform = models.ForeignKey(Asset_inform, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for User: {self.user.username}, Asset_inform: {self.Asset_inform.asset_id}"