from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings


def send_password_reset(user_email, token):
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=user_email,
        subject="Password Reset Request",
        html_content=f"""
            <h2>Password Reset</h2>
            <p>You requested a password reset. Click the link below:</p>
            <a href="{reset_url}">Reset My Password</a>
            <p>This link expires in 1 hour.</p>
            <p>If you did not request this, ignore this email.</p>
        """
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print(f"SendGrid error: {e}")


def send_low_stock_alert(item, user_email):
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=user_email,
        subject=f"Low Stock Alert: {item.name}",
        html_content=f"""
            <h2>Low Stock Alert</h2>
            <p>The following item is running low:</p>
            <table>
                <tr><td><strong>Item:</strong></td><td>{item.name}</td></tr>
                <tr><td><strong>Current Quantity:</strong></td><td>{item.quantity}</td></tr>
                <tr><td><strong>Low Stock Threshold:</strong></td><td>{item.low_stock}</td></tr>
            </table>
            <p>Please restock</p>
        """
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"SendGrid error: {e}")