from datetime import timedelta, datetime
from io import BytesIO

from PIL import Image
from PIL.Image import Dither, Palette
from pydantic import BaseModel
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager
from winsdk.windows.storage.streams import Buffer, InputStreamOptions


class PlayingMedia(BaseModel):
    application: str
    position: timedelta
    calculated_position: timedelta
    end: timedelta
    playing: bool
    title: str
    artist: str


last_position: timedelta | None = None
last_position_updated: datetime | None = None
latest_media: PlayingMedia | None = None
latest_event: str | None = None
latest_icon = None


async def get_media_info() -> None:
    global last_position, last_position_updated, latest_media, latest_event, latest_icon

    sessions = await GlobalSystemMediaTransportControlsSessionManager.request_async()

    current_session = sessions.get_current_session()
    if current_session:
        timeline = current_session.get_timeline_properties()
        playback_info = current_session.get_playback_info()
        app_name = current_session.source_app_user_model_id

        info = await current_session.try_get_media_properties_async()

        media = PlayingMedia(
            application=app_name,
            position=timeline.position,
            end=timeline.end_time,
            title=info.title,
            artist=info.artist,
            playing=playback_info.playback_status == 4,
            calculated_position=((
                                         datetime.now() - last_position_updated) + last_position) if last_position and last_position_updated else timeline.position
        )

        if timeline.position != last_position:
            last_position = timeline.position
            last_position_updated = datetime.now()

        if not media.playing:
            last_position_updated = datetime.now()

        if latest_media:
            is_new_song = latest_media.title != media.title or latest_media.artist != media.artist
            if is_new_song:
                latest_event = 'new_song'
            else:
                if latest_media.playing != media.playing:
                    if media.playing:
                        latest_event = 'resumed'
                    else:
                        latest_event = 'paused'
        else:
            stream = await info.thumbnail.open_read_async()

            buffer = Buffer(stream.size)
            await stream.read_async(buffer, stream.size, InputStreamOptions.NONE)

            bytes_arr = buffer.__buffer__(0).tobytes()

            stream.close()

            image = Image.open(BytesIO(bytes_arr))
            image.thumbnail((40, 40))
            bmp = image.convert("1", palette=Palette.ADAPTIVE, dither=Dither.FLOYDSTEINBERG)

            bmp.show()

            latest_icon = list(bmp.getdata())
            bmp.close()
            image.close()

        latest_media = media
