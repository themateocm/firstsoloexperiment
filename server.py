import http.server
import json
import random
from http.server import SimpleHTTPRequestHandler
from urllib.parse import urlparse

# Collection of motivational quotes
quotes = [
    # Quotes about hardship
    {"quote": "Hard times don't create heroes. It is during the hard times when the 'hero' within us is revealed.", "author": "Bob Riley", "category": "hardship"},
    {"quote": "The gem cannot be polished without friction, nor man perfected without trials.", "author": "Chinese Proverb", "category": "hardship"},
    {"quote": "Life's challenges are not supposed to paralyze you; they're supposed to help you discover who you are.", "author": "Bernice Johnson Reagon", "category": "hardship"},
    {"quote": "What lies behind us and what lies before us are tiny matters compared to what lies within us.", "author": "Ralph Waldo Emerson", "category": "hardship"},
    {"quote": "The ultimate measure of a man is not where he stands in moments of comfort and convenience, but where he stands at times of challenge and controversy.", "author": "Martin Luther King Jr.", "category": "hardship"},
    {"quote": "Rock bottom became the solid foundation on which I rebuilt my life.", "author": "J.K. Rowling", "category": "hardship"},
    {"quote": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein", "category": "hardship"},
    {"quote": "The greater the difficulty, the more glory in surmounting it.", "author": "Epicurus", "category": "hardship"},
    {"quote": "Tough times never last, but tough people do.", "author": "Robert H. Schuller", "category": "hardship"},
    {"quote": "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.", "author": "Henry Ford", "category": "hardship"},
    {"quote": "It's not about how hard you hit. It's about how hard you can get hit and keep moving forward.", "author": "Rocky Balboa", "category": "hardship"},
    {"quote": "Character cannot be developed in ease and quiet. Only through experience of trial and suffering can the soul be strengthened, ambition inspired, and success achieved.", "author": "Helen Keller", "category": "hardship"},
    {"quote": "The pain you feel today will be the strength you feel tomorrow.", "author": "Anonymous", "category": "hardship"},
    {"quote": "Difficulties strengthen the mind, as labor does the body.", "author": "Seneca", "category": "hardship"},
    {"quote": "We must embrace pain and burn it as fuel for our journey.", "author": "Kenji Miyazawa", "category": "hardship"},

    # Celebration quotes
    {"quote": "The more you praise and celebrate your life, the more there is in life to celebrate.", "author": "Oprah Winfrey", "category": "celebration"},
    {"quote": "Life is a celebration of awakenings, of new beginnings, and wonderful surprises that enlighten the soul.", "author": "Ciara", "category": "celebration"},
    {"quote": "Success is not the destination, it's the journey; celebrate the small wins.", "author": "Tony Robbins", "category": "celebration"},
    {"quote": "Celebrate what you've accomplished, but raise the bar a little higher each time you succeed.", "author": "Mia Hamm", "category": "celebration"},
    {"quote": "The more you celebrate your life, the more life you have to celebrate.", "author": "Maya Angelou", "category": "celebration"},
    {"quote": "Take time to celebrate the quiet miracles that seek no attention.", "author": "Anonymous", "category": "celebration"},
    {"quote": "Life is short, and it is up to you to make it sweet.", "author": "Sarah Louise Delany", "category": "celebration"},
    {"quote": "Celebrate the small victories, for they will lead to bigger ones.", "author": "Anonymous", "category": "celebration"},
    {"quote": "Joy is the simplest form of gratitude.", "author": "Karl Barth", "category": "celebration"},
    {"quote": "Find ecstasy in life; the mere sense of living is joy enough.", "author": "Emily Dickinson", "category": "celebration"},
    {"quote": "Dance like no one is watching, love like you'll never be hurt, sing like no one is listening.", "author": "William Purkey", "category": "celebration"},
    {"quote": "Life is meant to be a celebration! It shouldn't be necessary to set aside special times to remind us of this fact.", "author": "Nathaniel Branden", "category": "celebration"},
    {"quote": "Celebrate the mistakes; they're how you learn and grow.", "author": "Anonymous", "category": "celebration"},
    {"quote": "Today is a perfect day to celebrate the gift of life.", "author": "Anonymous", "category": "celebration"},
    {"quote": "In life, it's not about the destination, it's about celebrating the journey.", "author": "Anonymous", "category": "celebration"},

    # Anger quotes
    {"quote": "Anger is an acid that can do more harm to the vessel in which it is stored than to anything on which it is poured.", "author": "Mark Twain", "category": "anger"},
    {"quote": "For every minute you remain angry, you give up sixty seconds of peace of mind.", "author": "Ralph Waldo Emerson", "category": "anger"},
    {"quote": "Speak when you are angry and you will make the best speech you will ever regret.", "author": "Ambrose Bierce", "category": "anger"},
    {"quote": "The best fighter is never angry.", "author": "Lao Tzu", "category": "anger"},
    {"quote": "Anger is a wind which blows out the lamp of the mind.", "author": "Robert Green Ingersoll", "category": "anger"},
    {"quote": "When angry, count to ten before you speak. If very angry, count to one hundred.", "author": "Thomas Jefferson", "category": "anger"},
    {"quote": "Anger makes you smaller, while forgiveness forces you to grow beyond what you were.", "author": "Cherie Carter-Scott", "category": "anger"},
    {"quote": "Anger is like flowing water; there's nothing wrong with it as long as you let it flow.", "author": "Thich Nhat Hanh", "category": "anger"},
    {"quote": "Whatever is begun in anger, ends in shame.", "author": "Benjamin Franklin", "category": "anger"},
    {"quote": "Anger dwells only in the bosom of fools.", "author": "Albert Einstein", "category": "anger"},
    {"quote": "The greatest remedy for anger is delay.", "author": "Seneca", "category": "anger"},
    {"quote": "Anger is never without a reason, but seldom with a good one.", "author": "Benjamin Franklin", "category": "anger"},
    {"quote": "He who angers you conquers you.", "author": "Elizabeth Kenny", "category": "anger"},
    {"quote": "Where there is anger, there is always pain underneath.", "author": "Eckhart Tolle", "category": "anger"},
    {"quote": "In times of anger, silence is golden.", "author": "Anonymous", "category": "anger"},

    # Exhaustion quotes
    {"quote": "Sometimes the most productive thing you can do is rest.", "author": "Mark Black", "category": "exhaustion"},
    {"quote": "Rest when you're weary. Refresh and renew yourself, your body, your mind, your spirit.", "author": "Ralph Marston", "category": "exhaustion"},
    {"quote": "Even the strongest minds need time to recharge.", "author": "Anonymous", "category": "exhaustion"},
    {"quote": "Listen to your body when it whispers, so you won't have to hear it scream.", "author": "Anonymous", "category": "exhaustion"},
    {"quote": "Sleep is not a luxury, it's a necessity.", "author": "Dr. James B. Maas", "category": "exhaustion"},
    {"quote": "Your body is telling you it needs a break. Listen to it.", "author": "Anonymous", "category": "exhaustion"},
    {"quote": "Taking care of yourself doesn't mean me first, it means me too.", "author": "L.R. Knost", "category": "exhaustion"},
    {"quote": "Rest is not idleness, and to lie sometimes on the grass under trees on a summer's day, listening to the murmur of the water, or watching the clouds float across the sky, is by no means a waste of time.", "author": "John Lubbock", "category": "exhaustion"},
    {"quote": "The time to relax is when you don't have time for it.", "author": "Sydney J. Harris", "category": "exhaustion"},
    {"quote": "Almost everything will work again if you unplug it for a few minutes, including you.", "author": "Anne Lamott", "category": "exhaustion"},
    {"quote": "Sometimes the most important thing in a whole day is the rest we take between two deep breaths.", "author": "Etty Hillesum", "category": "exhaustion"},
    {"quote": "Self-care is not selfish. You cannot serve from an empty vessel.", "author": "Eleanor Brown", "category": "exhaustion"},
    {"quote": "Your mind will answer most questions if you learn to relax and wait for the answer.", "author": "William S. Burroughs", "category": "exhaustion"},
    {"quote": "Rest and self-care are so important. When you take time to replenish your spirit, it allows you to serve others from the overflow.", "author": "Eleanor Brown", "category": "exhaustion"},
    {"quote": "Sometimes the bravest thing you can do is stop and rest.", "author": "Anonymous", "category": "exhaustion"}
]

class QuoteHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/quote':
            # Send CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Return a random quote
            quote = random.choice(quotes)
            self.wfile.write(json.dumps(quote).encode())
            return
        
        # Serve static files (index.html)
        return SimpleHTTPRequestHandler.do_GET(self)

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, QuoteHandler)
    print("Server running on http://localhost:8000")
    httpd.serve_forever()
