import media
from config import config, ViewName
from gtk import BasicGTK
from gtk.manager import DrawMode
from utils import format_seconds
from .base import View


class IconLessView(View):

    @property
    def name(self) -> ViewName:
        return 'icon_less'

    def draw(self, gtk: BasicGTK) -> None:
        gtk.draw_big_text(0, 0, media.latest_media.title, config.text_speed)
        gtk.draw_big_text(0, 7 + config.row_gap, media.latest_media.artist, config.text_speed)

        gtk.draw_progress(2, 14 + config.row_gap * 2, gtk.screen.size[0] - 4, 10, media.latest_media.position_progress)
        gtk.draw_center_text(14 + config.row_gap * 2 + 2,
                             f'{format_seconds(media.latest_media.calculated_position.total_seconds())} - {format_seconds(media.latest_media.end.total_seconds())}',
                             DrawMode.FLIP)
