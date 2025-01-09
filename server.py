import http.server
import json
import random
from http.server import SimpleHTTPRequestHandler
from urllib.parse import urlparse

# Collection of motivational quotes with difficulty ratings (1-3)
quotes = [
    # Level 1 (Easy) - Very distinct emotional tones
    {"quote": "I am completely broken and exhausted.", "author": "Anonymous", "category": "exhaustion", "difficulty": 1},
    {"quote": "I can barely keep my eyes open.", "author": "Anonymous", "category": "exhaustion", "difficulty": 1},
    {"quote": "I need to rest, I'm so tired.", "author": "Anonymous", "category": "exhaustion", "difficulty": 1},
    {"quote": "My energy is completely drained.", "author": "Anonymous", "category": "exhaustion", "difficulty": 1},
    {"quote": "I can't take another step, I'm too tired.", "author": "Anonymous", "category": "exhaustion", "difficulty": 1},

    {"quote": "I am furious right now!", "author": "Anonymous", "category": "anger", "difficulty": 1},
    {"quote": "This makes my blood boil!", "author": "Anonymous", "category": "anger", "difficulty": 1},
    {"quote": "I can't control my rage anymore!", "author": "Anonymous", "category": "anger", "difficulty": 1},
    {"quote": "My anger is overwhelming!", "author": "Anonymous", "category": "anger", "difficulty": 1},
    {"quote": "I'm so mad I could scream!", "author": "Anonymous", "category": "anger", "difficulty": 1},

    {"quote": "This is the best day ever!", "author": "Anonymous", "category": "celebration", "difficulty": 1},
    {"quote": "I'm so happy I could dance!", "author": "Anonymous", "category": "celebration", "difficulty": 1},
    {"quote": "Let's celebrate this amazing moment!", "author": "Anonymous", "category": "celebration", "difficulty": 1},
    {"quote": "Victory is ours! Time to celebrate!", "author": "Anonymous", "category": "celebration", "difficulty": 1},
    {"quote": "What a wonderful achievement to celebrate!", "author": "Anonymous", "category": "celebration", "difficulty": 1},

    {"quote": "This is the hardest thing I've ever faced.", "author": "Anonymous", "category": "hardship", "difficulty": 1},
    {"quote": "I don't know if I can overcome this challenge.", "author": "Anonymous", "category": "hardship", "difficulty": 1},
    {"quote": "This obstacle seems impossible to overcome.", "author": "Anonymous", "category": "hardship", "difficulty": 1},
    {"quote": "I'm struggling to keep going through this difficulty.", "author": "Anonymous", "category": "hardship", "difficulty": 1},
    {"quote": "This burden feels too heavy to bear.", "author": "Anonymous", "category": "hardship", "difficulty": 1},

    # Level 2 (Medium) - Less obvious emotional tones
    {"quote": "The oak fought the wind and was broken, the willow bent when it must and survived.", "author": "Robert Jordan", "category": "hardship", "difficulty": 2},
    {"quote": "In the depth of winter, I finally learned that within me there lay an invincible summer.", "author": "Albert Camus", "category": "hardship", "difficulty": 2},
    {"quote": "The bamboo that bends is stronger than the oak that resists.", "author": "Japanese Proverb", "category": "hardship", "difficulty": 2},
    {"quote": "Stars can't shine without darkness.", "author": "D.H. Sidebottom", "category": "hardship", "difficulty": 2},
    {"quote": "The gem cannot be polished without friction.", "author": "Chinese Proverb", "category": "hardship", "difficulty": 2},

    {"quote": "Dance like the morning dew in sunlight.", "author": "Unknown", "category": "celebration", "difficulty": 2},
    {"quote": "Life is a canvas, paint your dreams in bold colors.", "author": "Unknown", "category": "celebration", "difficulty": 2},
    {"quote": "The music in my heart I bore, long after it was heard no more.", "author": "William Wordsworth", "category": "celebration", "difficulty": 2},
    {"quote": "Each moment is a fresh beginning.", "author": "T.S. Eliot", "category": "celebration", "difficulty": 2},
    {"quote": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt", "category": "celebration", "difficulty": 2},

    {"quote": "A gentle answer turns away wrath.", "author": "Biblical Proverb", "category": "anger", "difficulty": 2},
    {"quote": "The fire you kindle for your enemy often burns yourself more than them.", "author": "Chinese Proverb", "category": "anger", "difficulty": 2},
    {"quote": "Holding onto anger is like drinking poison and expecting the other person to die.", "author": "Buddha", "category": "anger", "difficulty": 2},
    {"quote": "Where there is anger, there is always pain underneath.", "author": "Eckhart Tolle", "category": "anger", "difficulty": 2},
    {"quote": "The best fighter is never angry.", "author": "Lao Tzu", "category": "anger", "difficulty": 2},

    {"quote": "The candle burns until it is no more.", "author": "Japanese Proverb", "category": "exhaustion", "difficulty": 2},
    {"quote": "Time flows like a river, and we cannot hold back its tide.", "author": "Unknown", "category": "exhaustion", "difficulty": 2},
    {"quote": "The bow that is always bent will break.", "author": "Greek Proverb", "category": "exhaustion", "difficulty": 2},
    {"quote": "Even the strongest blade of grass bends in the wind.", "author": "Unknown", "category": "exhaustion", "difficulty": 2},
    {"quote": "The deeper the well, the cooler the water.", "author": "Unknown", "category": "exhaustion", "difficulty": 2},

    # Level 3 (Hard) - Subtle or ambiguous emotional tones
    {"quote": "The butterfly counts not months but moments.", "author": "Rabindranath Tagore", "category": "hardship", "difficulty": 3},
    {"quote": "The reed that grows slowly endures.", "author": "Chinese Proverb", "category": "hardship", "difficulty": 3},
    {"quote": "Time is the wisest counselor.", "author": "Pericles", "category": "hardship", "difficulty": 3},
    {"quote": "The deeper the roots, the stronger the tree.", "author": "Unknown", "category": "hardship", "difficulty": 3},
    {"quote": "Silence is sometimes the best answer.", "author": "Dalai Lama", "category": "hardship", "difficulty": 3},

    {"quote": "Dawn comes after the darkness.", "author": "Unknown", "category": "celebration", "difficulty": 3},
    {"quote": "Every flower must grow through dirt.", "author": "Unknown", "category": "celebration", "difficulty": 3},
    {"quote": "The morning breeze has secrets to tell you.", "author": "Rumi", "category": "celebration", "difficulty": 3},
    {"quote": "Time unfolds beauty, wonder, and mystery.", "author": "Unknown", "category": "celebration", "difficulty": 3},
    {"quote": "Each sunset brings the promise of a new dawn.", "author": "Ralph Waldo Emerson", "category": "celebration", "difficulty": 3},

    {"quote": "Still waters run deep.", "author": "Latin Proverb", "category": "anger", "difficulty": 3},
    {"quote": "The sharper the blade, the sooner it dulls.", "author": "Unknown", "category": "anger", "difficulty": 3},
    {"quote": "Thunder follows lightning.", "author": "Unknown", "category": "anger", "difficulty": 3},
    {"quote": "A closed mouth gathers no feet.", "author": "Unknown", "category": "anger", "difficulty": 3},
    {"quote": "The higher the mountain, the stronger the wind.", "author": "Chinese Proverb", "category": "anger", "difficulty": 3},

    {"quote": "Even the longest day has its evening.", "author": "Unknown", "category": "exhaustion", "difficulty": 3},
    {"quote": "The river carves its path.", "author": "Unknown", "category": "exhaustion", "difficulty": 3},
    {"quote": "Time is the great healer.", "author": "Unknown", "category": "exhaustion", "difficulty": 3},
    {"quote": "The moon has its phases.", "author": "Unknown", "category": "exhaustion", "difficulty": 3},
    {"quote": "Every wave has its ebb.", "author": "Unknown", "category": "exhaustion", "difficulty": 3}
]

class QuoteHandler(SimpleHTTPRequestHandler):
    # Initialize class variables as instance variables in __init__
    def __init__(self, *args, **kwargs):
        self.used_quotes = set()
        self.current_level = 1
        self.quotes_in_level = 0
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/quote':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                print(f"\nCurrent state - Level: {self.current_level}, Quotes in level: {self.quotes_in_level}, Used quotes: {len(self.used_quotes)}")
                
                # Get unused quotes for current level
                unused_quotes = [q for i, q in enumerate(quotes) 
                               if i not in self.used_quotes and 
                               q['difficulty'] == self.current_level]
                
                print(f"Found {len(unused_quotes)} unused quotes for level {self.current_level}")
                
                # Check if we need to level up (every 5 quotes)
                if self.quotes_in_level >= 5:
                    print("Reached 5 quotes, triggering level up")
                    if self.current_level < 3:
                        self.current_level += 1
                        self.quotes_in_level = 0
                        response = {
                            "levelUp": True,
                            "newLevel": self.current_level
                        }
                        print(f"Leveling up to {self.current_level}")
                        self.wfile.write(json.dumps(response).encode())
                        return
                
                if not unused_quotes:
                    print("No more unused quotes for current level")
                    if self.current_level < 3:
                        # Level up
                        self.current_level += 1
                        self.quotes_in_level = 0
                        unused_quotes = [q for i, q in enumerate(quotes) 
                                       if i not in self.used_quotes and 
                                       q['difficulty'] == self.current_level]
                        response = {
                            "levelUp": True,
                            "newLevel": self.current_level
                        }
                        print(f"Leveling up to {self.current_level} due to no more quotes")
                    else:
                        # Game over
                        print("Game Over - No more quotes and at max level")
                        response = {
                            "gameOver": True,
                            "total": len(quotes)
                        }
                    self.wfile.write(json.dumps(response).encode())
                    return
                
                # Get a random unused quote for current level
                quote = random.choice(unused_quotes)
                quote_index = quotes.index(quote)
                self.used_quotes.add(quote_index)
                self.quotes_in_level += 1
                
                # Add metadata to response
                response = {
                    **quote,
                    "remaining": len(quotes) - len(self.used_quotes),
                    "total": len(quotes),
                    "currentLevel": self.current_level,
                    "quotesInLevel": self.quotes_in_level,
                    "quotesUntilNextLevel": 5 - (self.quotes_in_level % 5)
                }
                
                print(f"Serving quote {quote_index}, Level {self.current_level}, Quotes in level: {self.quotes_in_level}, Until next: {5 - (self.quotes_in_level % 5)}")
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"Error serving quote: {str(e)}")
                self.send_error(500, f"Internal server error: {str(e)}")
            return
        
        # Serve static files
        return SimpleHTTPRequestHandler.do_GET(self)

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, QuoteHandler)
    print("Server running on http://localhost:8000")
    httpd.serve_forever()
