from pydantic import BaseModel
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager


class PlayingMedia(BaseModel):
    application: str
    position: str
    start: str
    end: str
    playing: bool
    title: str
    artist: str


async def get_media_info() -> PlayingMedia:
    sessions = await GlobalSystemMediaTransportControlsSessionManager.request_async()

    current_session = sessions.get_current_session()
    if current_session:
        timeline = current_session.get_timeline_properties()
        playback_info = current_session.get_playback_info()
        app_name = current_session.source_app_user_model_id

        info = await current_session.try_get_media_properties_async()

        return PlayingMedia(
            application=app_name,
            position=timeline.position,
            start=timeline.start_time,
            end=timeline.end_time,
            title=info.title,
            artist=info.artist,
            playing=playback_info.playback_status == 4,
        )
    else:
        raise RuntimeError("No media session is currently active.")
