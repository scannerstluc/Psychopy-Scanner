def hex_to_rgb(hex_color):
    # Convertir le hexadécimal en RGB
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def convert_rgb_to_psychopy(rgb):
    # Convertir chaque composant RGB avec une précision élevée
    return [(x / 255.0) * 2 - 1for x in rgb]

# Couleur Hexadécimale donnée
hex_color = "7D807D"
# Conversion de Hex à RGB
rgb_color = hex_to_rgb(hex_color)
# Conversion de RGB à PsychoPy
psychopy_color = convert_rgb_to_psychopy(rgb_color)

print("Couleur PsychoPy précise pour #7C7E7B :", psychopy_color)