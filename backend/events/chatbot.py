from .models import Event
from django.contrib.auth.models import User
from datetime import datetime

class EventChatbot:
    def get_events_context(self):
        events = Event.objects.all()[:10]
        if not events:
            return "No events available right now."
        
        context = "📋 Available Events:\n"
        for event in events:
            context += f"• {event.name} - 📍 {event.location}, 📅 {event.date}, 💰 ₹{event.price}, 🎫 {event.available_seats()} seats available\n"
        return context
    
    def get_response(self, user_message):
        try:
            user_message_lower = user_message.lower()
            events_context = self.get_events_context()
            
            # ============ GREETINGS ============
            if any(word in user_message_lower for word in ['good morning', 'gm', 'morning']):
                return "🌅 Good Morning! Welcome to EventHub. How can I help you today? Have a great day! ☀️"
            
            elif any(word in user_message_lower for word in ['good evening', 'ge', 'evening']):
                return "🌇 Good Evening! Welcome to EventHub. How can I help you today? Enjoy your evening! 🌙"
            
            elif any(word in user_message_lower for word in ['good night', 'gn', 'night']):
                return "🌙 Good Night! Rest well. See you tomorrow! 💤"
            
            elif any(word in user_message_lower for word in ['hello', 'hi', 'hey']):
                return "👋 Hello! Welcome to EventHub AI Assistant. How can I help you today?"
            
            # ============ HOW ARE YOU ============
            elif any(word in user_message_lower for word in ['how are you', 'how r u', 'how are u', 'how do you do']):
                return "🤖 I'm doing great! Thanks for asking 😊. I'm here to help you with events, bookings, and more! How can I assist you today?"
            
            # ============ WHAT IS YOUR NAME ============
            elif any(word in user_message_lower for word in ['your name', 'who are you', 'tell me about yourself']):
                return "🤖 I'm EventHub AI Assistant! Your friendly chatbot for event management. I can help you with:\n• Finding events\n• Booking tickets\n• Login/Register help\n• Event details\n\nHow can I help you today? 🎉"
            
            # ============ THANK YOU ============
            elif any(word in user_message_lower for word in ['thank', 'thanks', 'thank you']):
                return "😊 You're welcome! Happy event hunting! 🎉 If you need any more help, just ask!"
            
            # ============ EVENTS ============
            elif any(word in user_message_lower for word in ['event', 'show', 'list', 'available', 'all events']):
                return f"📋 Here are the upcoming events:\n\n{events_context}"
            
            # ============ UPCOMING EVENTS ============
            elif any(word in user_message_lower for word in ['upcoming', 'future', 'next']):
                return f"📅 Here are the upcoming events:\n\n{events_context}"
            
            # ============ BOOKING ============
            elif any(word in user_message_lower for word in ['book', 'booking', 'ticket', 'reserve']):
                return "🎫 To book an event:\n1. Go to Dashboard\n2. Find your favorite event\n3. Click 'Book Now'\n4. Fill in your details\n5. Confirm booking\n\nMake sure you're logged in first! 🔐"
            
            # ============ LOGIN HELP ============
            elif any(word in user_message_lower for word in ['login', 'signin', 'account', 'log in']):
                return "🔐 To login:\n1. Click 'Login' in top right corner\n2. Enter your username and password\n3. Click 'Login'\n\nDon't have an account? Click 'Register' to create one! 📝"
            
            # ============ REGISTER HELP ============
            elif any(word in user_message_lower for word in ['register', 'signup', 'create account', 'new account']):
                return "📝 To register:\n1. Click 'Register' in top right corner\n2. Fill in your details (username, email, password)\n3. Agree to Terms\n4. Click 'Register'\n\nIt's quick and easy! 🚀"
            
            # ============ LOGOUT HELP ============
            elif any(word in user_message_lower for word in ['logout', 'log out']):
                return "🚪 To logout:\n1. Click 'Logout' in top right corner\n2. You'll be logged out successfully\n\nSee you again soon! 👋"
            
            # ============ PROFILE HELP ============
            elif any(word in user_message_lower for word in ['profile', 'my profile', 'edit profile']):
                return "👤 To view your profile:\n1. Click 'Profile' in the navbar\n2. View your details\n3. Edit your information\n\nComing soon: Profile editing! 🚀"
            
            # ============ MY BOOKINGS ============
            elif any(word in user_message_lower for word in ['my bookings', 'my tickets', 'my events']):
                return "📋 To view your bookings:\n1. Click 'My Bookings' in the navbar\n2. See all your booked events\n3. Cancel bookings if needed\n\nYou need to be logged in! 🔐"
            
            # ============ PRICE HELP ============
            elif any(word in user_message_lower for word in ['price', 'cost', 'how much', 'fee']):
                return "💰 Event prices vary:\n• Some events are free (₹0)\n• Paid events start from ₹50\n• Prices are shown on each event card\n\nCheck the Dashboard for exact prices! 💵"
            
            # ============ SEATS HELP ============
            elif any(word in user_message_lower for word in ['seat', 'seats', 'available seats', 'capacity']):
                return "🎫 Seat availability:\n• Available seats shown on each event\n• 'Available: X seats'\n• Book quickly before seats fill up!\n• Some events may be sold out ❌"
            
            # ============ DATE HELP ============
            elif any(word in user_message_lower for word in ['date', 'when', 'time', 'schedule']):
                return "📅 Event dates and times:\n• Each event has a specific date/time\n• Check the event card for details\n• Mark your calendar! 📌\n• Don't miss out on your favorite events!"
            
            # ============ LOCATION HELP ============
            elif any(word in user_message_lower for word in ['location', 'where', 'venue', 'address']):
                return "📍 Event locations:\n• Each event has a venue\n• Location shown on event card\n• Online events are marked 'Online'\n• Check the address before going! 🗺️"
            
            # ============ HELP ============
            elif any(word in user_message_lower for word in ['help', 'support', 'assist']):
                return "🆘 I can help you with:\n• 📋 Finding events\n• 🎫 Booking tickets\n• 🔐 Login/Register help\n• 📅 Upcoming events\n• 👤 Profile info\n• 📋 My Bookings\n• 💰 Prices\n• 📍 Locations\n\nJust ask me anything! 😊"
            
            # ============ ABOUT ============
            elif any(word in user_message_lower for word in ['about', 'what is this', 'about eventhub']):
                return "🎉 EventHub is a Real-Time Event Management Platform!\n\nFeatures:\n• 📋 Browse events\n• 🎫 Book tickets\n• 📅 Track your bookings\n• 🔔 Real-time notifications\n• 🤖 AI Assistant (me!)\n\nStart exploring now! 🚀"
            
            # ============ FEEDBACK ============
            elif any(word in user_message_lower for word in ['feedback', 'suggest', 'improve']):
                return "💡 We value your feedback!\n• Share your suggestions\n• Report any issues\n• Help us improve\n• Email: support@eventhub.com\n\nThank you for using EventHub! 🌟"
            
            # ============ CONTACT ============
            elif any(word in user_message_lower for word in ['contact', 'email', 'call', 'reach']):
                return "📞 Contact Us:\n• Email: support@eventhub.com\n• Phone: +91-XXXXX-XXXXX\n• Working Hours: 9 AM - 6 PM\n\nWe're here to help! 💬"
            
            # ============ WEATHER ============
            elif any(word in user_message_lower for word in ['weather', 'temperature', 'hot', 'cold', 'rain']):
                return "🌤️ I don't have real-time weather data, but you can check your local weather app! 😊\n\nFor event planning, always check weather before attending outdoor events! ☀️🌧️"
            
            # ============ TIME ============
            elif any(word in user_message_lower for word in ['time', 'what time', 'current time']):
                now = datetime.now()
                return f"🕐 Current time: {now.strftime('%I:%M %p')}\nDate: {now.strftime('%B %d, %Y')}\n\nIs there any event you'd like to know about? 🎫"
            
            # ============ SORRY / BYE ============
            elif any(word in user_message_lower for word in ['sorry', 'bye', 'goodbye']):
                return "👋 Goodbye! Thanks for chatting with me. Have a great day! 😊\n\nCome back anytime if you need help! 🎉"
            
            # ============ RECOMMEND EVENTS ============
            elif any(word in user_message_lower for word in ['recommend', 'suggest', 'what should i attend']):
                return "🎯 Based on popular events, I recommend:\n\n1. 🎵 Music Festival - Great for music lovers!\n2. 💻 Tech Conference - For tech enthusiasts!\n3. 🎭 Cultural Events - Experience traditions!\n\nCheck the Dashboard for all events! 📋"
            
            # ============ CANCEL BOOKING ============
            elif any(word in user_message_lower for word in ['cancel booking', 'cancel ticket']):
                return "❌ To cancel a booking:\n1. Go to 'My Bookings'\n2. Find your booking\n3. Click 'Cancel Booking'\n4. Confirm cancellation\n\nNote: Cancellations may have fees! ⚠️"
            
            # ============ DEFAULT ============
            else:
                return f"🤔 I'm not sure about that. Here are some things I can help with:\n\n• 👋 Greetings (Hello, Good Morning)\n• 📋 Show events\n• 🎫 How to book?\n• 🔐 Login/Register help\n• 📅 Upcoming events\n• 👤 Profile info\n• 📋 My Bookings\n• 💰 Prices\n• 📍 Locations\n• 🆘 Help\n\nTry asking one of these! 😊"
                
        except Exception as e:
            print(f"Chatbot Error: {e}")
            return "😅 I'm having trouble. Please try again!"