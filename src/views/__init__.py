from .base import View
from .iconless import IconLessView
from .with_icon import WithIconView

__views = [
    WithIconView(),
    IconLessView()
]

views: dict[str, View] = {view.name: view for view in __views}
