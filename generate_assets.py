import json
import random

assets = []

vibes = [
    {"vibe": "Cozy Mornings", "color": "eab308", "desc": "Coffee, blankets, soft morning light"},
    {"vibe": "Neon Nights", "color": "d946ef", "desc": "Cyberpunk cityscapes, glowing signs, dark contrast"},
    {"vibe": "Golden Hour", "color": "f97316", "desc": "Sunsets, warm skin tones, long shadows"},
    {"vibe": "Minimalist Zen", "color": "9ca3af", "desc": "Clean lines, negative space, monochromatic"},
    {"vibe": "Cinematic Moody", "color": "0ea5e9", "desc": "Teal and orange, dramatic lighting, film look"}
]

for i in range(1, 41):
    chosen_vibe = random.choice(vibes)
    
    assets.append({
        "id": f"img_{i:03d}",
        "vibe": chosen_vibe["vibe"],
        "description": chosen_vibe["desc"],
        # Using placehold.co to generate aesthetically colored placeholder images
        "url": f"https://placehold.co/600x800/{chosen_vibe['color']}/ffffff?text={chosen_vibe['vibe'].replace(' ', '+')}+{i}"
    })

with open('vibe_assets.json', 'w') as f:
    json.dump(assets, f, indent=4)
print("vibe_assets.json created successfully.")
