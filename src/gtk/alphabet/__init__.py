from .digits import digits
from .english import english_letters
from .russian import russian_letters
from .special import special_letters

bitmap_font = {}
bitmap_font.update(digits)
bitmap_font.update(english_letters)
bitmap_font.update(russian_letters)
bitmap_font.update(special_letters)
