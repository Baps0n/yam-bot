import sys
import time
from distest import TestCollector
from distest import run_dtest_bot

test_collector = TestCollector()
created_channel = None
# python .\tests.py 899248710444281876 OTIxMDA5ODIxMDUyOTY0OTA1.YbsrPA.LdxRgv-Ll70Njp8gqxxH29mkiZk -c 904323058293174272 -r all


@test_collector()
async def test_help(interface):
    await interface.assert_reply_contains("]h", "]p")


@test_collector()
async def test_silent_join(interface):
    await interface.connect(899248550070853663)
    await interface.send_message("]silent_join")
    await interface.wait_for_event("voice_state_update")
    await interface.disconnect()


@test_collector()
async def test_join(interface):
    await interface.connect(904323112332558396)
    await interface.send_message("]join")
    await interface.wait_for_event("voice_state_update")
    await interface.wait_for_message_in_channel('Подключен к каналу 111', 904323058293174272)
    await interface.disconnect()


@test_collector()
async def test_leave(interface):
    await interface.connect(904323112332558396)
    await interface.send_message("]l")
    await interface.wait_for_event("voice_state_update")
    await interface.wait_for_message_in_channel('Отключен от канала 111', 904323058293174272)
    await interface.disconnect()


@test_collector()
async def test_play(interface):
    await interface.connect(904323112332558396)
    await interface.assert_reply_contains("]p Clock Bell", "Выберите трек, написав его номер в списке:")
    await interface.send_message("1")
    await interface.send_message("]l")
    await interface.disconnect()


@test_collector()
async def test_play_artist(interface):
    await interface.connect(904323112332558396)
    await interface.assert_reply_contains("]pa Tzad", "Выберите альбом, написав его номер в списке:")
    await interface.send_message("1")
    await interface.send_message("]l")
    await interface.disconnect()

@test_collector()
async def test_play_track(interface):
    await interface.connect(904323112332558396)
    track_data = "{'route':'test\\9RSF7ONM2Y.mp3','name':'#1','author':'А4'}"
    await interface.send_message("]j")
    time.sleep(1)
    await interface.assert_reply_contains(f"]play_track {str(track_data)}", "Воспроизведение")
    await interface.send_message("]l")
    await interface.disconnect()


@test_collector()
async def test_show_playlist(interface):
    await interface.connect(904323112332558396)
    await interface.assert_reply_contains("]pl", "Треков в очереди ")
    await interface.send_message("]l")
    await interface.disconnect()


@test_collector()
async def test_skip(interface):
    await interface.connect(904323112332558396)
    await interface.assert_reply_contains("]s", "Трек пропущен")
    await interface.send_message("]l")
    await interface.disconnect()


@test_collector()
async def test_skip_n(interface):
    n = 5
    await interface.connect(904323112332558396)
    await interface.assert_reply_contains(f"]s {n}", f"Из плейлиста удалено {n} треков")
    await interface.send_message("]l")
    await interface.disconnect()

if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector)
