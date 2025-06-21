"""
Communication Functions
"""

import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Any, Dict, List, Optional
import os
from .base import BaseFunction


class SendEmailFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "send_email"
    
    @property
    def description(self) -> str:
        return "Send an email to specified recipients"
    
    @property
    def category(self) -> str:
        return "communication"
    
    @property
    def examples(self) -> List[str]:
        return [
            "send_email('abhayrajputcse@gmail.com', 'Subject', 'Message body')",
            "send_email(['abhayrajputcse@gmail.com', 'user2@example.com'], 'Report', 'Monthly report attached')"
        ]
    
    async def execute(self, to_email: str, subject: str, body: str, from_email: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Use environment variables for email configuration
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            email_user = from_email or os.getenv('EMAIL_USER')
            email_pass = os.getenv('EMAIL_PASS')
            
            if not email_user or not email_pass:
                return {"success": False, "error": "Email credentials not configured"}
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_user, email_pass)
            text = msg.as_string()
            server.sendmail(email_user, to_email, text)
            server.quit()
            
            return {"success": True, "message": f"Email sent to {to_email}"}
        except Exception as e:
            return {"success": False, "error": str(e)}


class SendSMSFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "send_sms"
    
    @property
    def description(self) -> str:
        return "Send SMS message (simulation for demo)"
    
    @property
    def category(self) -> str:
        return "communication"
    
    async def execute(self, phone_number: str, message: str) -> Dict[str, Any]:
        # This is a simulation - in real implementation, you'd use Twilio or similar
        try:
            # Simulate SMS sending
            return {
                "success": True,
                "message": f"SMS sent to {phone_number}: {message}",
                "simulation": True
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class MakeHTTPRequestFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "make_http_request"
    
    @property
    def description(self) -> str:
        return "Make HTTP request to specified URL"
    
    @property
    def category(self) -> str:
        return "communication"
    
    async def execute(self, url: str, method: str = "GET", headers: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            if headers is None:
                headers = {}
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=data)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                return {"success": False, "error": f"Unsupported HTTP method: {method}"}
            
            return {
                "success": True,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "data": response.text[:1000]  # Limit response size
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class PostToSlackFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "post_to_slack"
    
    @property
    def description(self) -> str:
        return "Post message to Slack channel (simulation)"
    
    @property
    def category(self) -> str:
        return "communication"
    
    async def execute(self, channel: str, message: str, webhook_url: Optional[str] = None) -> Dict[str, Any]:
        try:
            # This is a simulation - in real implementation, you'd use Slack API
            return {
                "success": True,
                "message": f"Posted to #{channel}: {message}",
                "simulation": True
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class SendNotificationFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "send_notification"
    
    @property
    def description(self) -> str:
        return "Send push notification (simulation)"
    
    @property
    def category(self) -> str:
        return "communication"
    
    async def execute(self, title: str, message: str, recipient: str) -> Dict[str, Any]:
        try:
            # This is a simulation - in real implementation, you'd use Firebase or similar
            return {
                "success": True,
                "message": f"Notification sent to {recipient}: {title} - {message}",
                "simulation": True
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class GetWeatherFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "get_weather"
    
    @property
    def description(self) -> str:
        return "Get weather information for a location"
    
    @property
    def category(self) -> str:
        return "communication"
    
    async def execute(self, location: str) -> Dict[str, Any]:
        try:
            # This is a simulation - in real implementation, you'd use OpenWeatherMap API
            weather_data = {
                "location": location,
                "temperature": "22°C",
                "condition": "Partly cloudy",
                "humidity": "65%",
                "wind_speed": "10 km/h"
            }
            
            return {
                "success": True,
                "weather": weather_data,
                "simulation": True
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class GetNewsFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "get_news"
    
    @property
    def description(self) -> str:
        return "Get latest news headlines"
    
    @property
    def category(self) -> str:
        return "communication"
    
    async def execute(self, category: str = "general", limit: int = 5) -> Dict[str, Any]:
        try:
            # This is a simulation - in real implementation, you'd use NewsAPI
            news_data = [
                {"title": f"Sample {category} news headline {i+1}", "source": "Demo News", "url": f"https://example.com/news/{i+1}"}
                for i in range(limit)
            ]
            
            return {
                "success": True,
                "news": news_data,
                "simulation": True
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
